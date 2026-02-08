#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Monthly Financial Summary Generator
Generates tax summaries and accountant emails for complete months
"""

import csv
import os
import subprocess
from datetime import datetime
from pathlib import Path
from collections import defaultdict

def parse_date(date_str):
    """Parse MM/DD/YYYY format"""
    if not date_str:
        return None
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        return None

def calculate_tax(revenue):
    """Calculate 8.5% ryczałt tax with proper rounding"""
    tax = revenue * 0.085
    # Standard mathematical rounding (0.5 rounds up)
    return round(tax)

def generate_monthly_summary(csv_file, year, month, output_dir='umowy_2026'):
    """Generate financial summary for a specific month"""
    
    month_str = f"{year}-{month:02d}"
    print(f"📊 Generating summary for {month_str}...")
    
    # Read CSV and collect data for the month
    reservations = []
    total_revenue = 0.0
    
    with open(csv_file, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row.get('Type') != 'Reservation':
                continue
            
            start_date = parse_date(row.get('Start date'))
            if not start_date:
                continue
            
            # Filter by month (based on check-in date for folder organization)
            if start_date.year == year and start_date.month == month:
                try:
                    amount = float(row.get('Amount', '0').replace(',', ''))
                    reservations.append({
                        'guest': row.get('Guest', 'Unknown'),
                        'code': row.get('Confirmation code', 'N/A'),
                        'start': start_date,
                        'end': parse_date(row.get('End date')),
                        'amount': amount,
                        'nights': row.get('Nights', '0'),
                        'listing': row.get('Listing', 'Unknown')
                    })
                    total_revenue += amount
                except ValueError:
                    continue
    
    if not reservations:
        print(f"⚠️  No reservations found for {month_str}")
        return None
    
    # Calculate tax
    tax_amount = calculate_tax(total_revenue)
    
    # Generate summary document
    summary_md = generate_summary_markdown(
        year, month, reservations, total_revenue, tax_amount
    )
    
    # Save summary
    summary_path = Path(output_dir) / month_str / f"Podsumowanie_{month_str}.md"
    summary_path.parent.mkdir(parents=True, exist_ok=True)
    
    with open(summary_path, 'w', encoding='utf-8') as f:
        f.write(summary_md)
    
    print(f"✅ Summary saved: {summary_path}")
    
    # Generate PDF using Puppeteer
    try:
        script_dir = Path(__file__).parent
        node_script = script_dir / 'md_to_pdf.js'
        
        if node_script.exists():
            result = subprocess.run(
                ['node', str(node_script), str(summary_path)],
                capture_output=True,
                timeout=30
            )
            if result.returncode == 0:
                print(f"✅ PDF created: {summary_path.with_suffix('.pdf')}")
    except Exception as e:
        print(f"⚠️  PDF generation skipped: {e}")
    
    # Generate email template
    email_template = generate_email_template(
        year, month, reservations, total_revenue, tax_amount
    )
    
    email_path = summary_path.parent / f"Email_ksiegowa_{month_str}.txt"
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(email_template)
    
    print(f"✅ Email template: {email_path}")
    
    return {
        'month': month_str,
        'count': len(reservations),
        'revenue': total_revenue,
        'tax': tax_amount,
        'summary_path': summary_path
    }

def generate_summary_markdown(year, month, reservations, total_revenue, tax_amount):
    """Generate Markdown summary document"""
    
    month_names_pl = [
        'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
        'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
    ]
    
    month_name = month_names_pl[month - 1]
    
    md = f"""# Podsumowanie Finansowe - {month_name} {year}

---

## 💰 Przychody

- **Liczba umów najmu:** {len(reservations)}
- **Łączny przychód (netto do Wynajmującego):** {total_revenue:,.2f} PLN

---

## 📊 Podatek (Ryczałt od najmu prywatnego - 8.5%)

- **Podstawa opodatkowania:** {total_revenue:,.2f} PLN
- **Stawka:** 8.5%
- **Podatek do zapłaty:** **{tax_amount} PLN**

---

## 📋 Szczegółowa Lista Umów

| Lp. | Gość | Kod rezerwacji | Check-in | Check-out | Noce | Kwota (PLN) |
|-----|------|----------------|----------|-----------|------|-------------|
"""
    
    for i, res in enumerate(reservations, 1):
        md += f"| {i} | {res['guest']} | {res['code']} | {res['start'].strftime('%d.%m.%Y')} | {res['end'].strftime('%d.%m.%Y')} | {res['nights']} | {res['amount']:,.2f} |\n"
    
    md += f"""
---

## 📎 Załączniki dla Księgowej

1. **Niniejsze podsumowanie** (`Podsumowanie_{year}-{month:02d}.pdf`)
2. **Umowy najmu** ({len(reservations)} plików):
"""
    
    for i, res in enumerate(reservations, 1):
        start_str = res['start'].strftime('%Y-%m-%d')
        end_str = res['end'].strftime('%Y-%m-%d')
        guest_safe = res['guest'].replace(' ', '_')
        filename = f"Umowa_{start_str}_{end_str}_{guest_safe}"
        md += f"   - `{filename}.pdf` ({res['amount']:,.2f} PLN)\n"
    
    md += f"""
---

## 📝 Uwagi

- Wszystkie kwoty w PLN
- Stawka podatku: 8.5% (Art. 30a ust. 1 pkt 2 ustawy o PIT - wynajem prywatny)
- Podstawa prawna zwolnienia z VAT: Art. 43 ust. 1 pkt 36 ustawy o VAT
- Klasyfikacja PKWiU: 68.20.11.0 (Wynajem i dzierżawa własnych nieruchomości mieszkalnych)

---

**Wygenerowano:** {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
    
    return md

def generate_email_template(year, month, reservations, total_revenue, tax_amount):
    """Generate email template for accountant"""
    
    month_names_pl = [
        'styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec',
        'lipiec', 'sierpień', 'wrzesień', 'październik', 'listopad', 'grudzień'
    ]
    
    month_name = month_names_pl[month - 1]
    
    template = f"""Temat: Dokumenty księgowe - {month_name.capitalize()} {year}

Dzień dobry,

Przesyłam dokumentację księgową za {month_name} {year}:

📊 PODSUMOWANIE:
- Przychód (netto): {total_revenue:,.2f} PLN
- Podatek ryczałt (8.5%): {tax_amount} PLN
- Liczba umów najmu: {len(reservations)}

📎 ZAŁĄCZNIKI:
1. Podsumowanie_{year}-{month:02d}.pdf (dokument zbiorczy)
2. Umowy najmu ({len(reservations)} plików):
"""
    
    for i, res in enumerate(reservations, 1):
        start_str = res['start'].strftime('%Y-%m-%d')
        end_str = res['end'].strftime('%Y-%m-%d')
        guest_safe = res['guest'].replace(' ', '_')
        filename = f"Umowa_{start_str}_{end_str}_{guest_safe}.pdf"
        template += f"   {i}. {filename} - {res['amount']:,.2f} PLN\n"
    
    template += f"""
💼 INFORMACJE DODATKOWE:
- Rodzaj działalności: Wynajem lokali mieszkalnych (najem prywatny)
- Zwolnienie z VAT: Art. 43 ust. 1 pkt 36 (cel mieszkaniowy)
- PKWiU: 68.20.11.0
- Forma opodatkowania: Ryczałt 8.5%

Proszę o potwierdzenie otrzymania dokumentów.

Pozdrawiam,
Marcin Kordas
NIP: 677-244-60-64
"""
    
    return template

def main():
    """Main execution"""
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python monthly_summary.py <YYYY-MM> [csv_file]")
        print("Example: python monthly_summary.py 2026-01")
        print("         python monthly_summary.py 2026-01 airbnb.csv")
        sys.exit(1)
    
    # Parse arguments
    month_str = sys.argv[1]
    csv_file = sys.argv[2] if len(sys.argv) > 2 else 'airbnb.csv'
    
    try:
        year, month = map(int, month_str.split('-'))
    except ValueError:
        print("❌ Invalid format. Use YYYY-MM (e.g., 2026-01)")
        sys.exit(1)
    
    if not os.path.exists(csv_file):
        print(f"❌ CSV file not found: {csv_file}")
        sys.exit(1)
    
    # Generate summary
    result = generate_monthly_summary(csv_file, year, month)
    
    if result:
        print("\n" + "="*50)
        print(f"✅ Summary generated for {result['month']}")
        print(f"   Agreements: {result['count']}")
        print(f"   Revenue: {result['revenue']:,.2f} PLN")
        print(f"   Tax (8.5%): {result['tax']} PLN")
        print("="*50)

if __name__ == "__main__":
    main()
