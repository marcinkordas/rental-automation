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
    """Generate financial summary for a specific month based on PAYOUT DATES"""
    
    month_str = f"{year}-{month:02d}"
    print(f"📊 Generating summary for {month_str}...")
    
    # MANUAL EXCLUSIONS (e.g. legacy private rental payouts)
    EXCLUDED_CODES = ['HM9R3KZ3KY'] # Abbas Ali (Dec 2025 extension)
    
    # Data containers
    payouts = []
    reservations = []
    
    total_revenue_net_airbnb = 0.0 # 'Amount' column (Payout + Deducted Fees)
    total_revenue_gross = 0.0      # 'Gross earnings' (Amount + Service Fee)
    total_service_fees = 0.0       # 'Service fee'
    total_payout_cash = 0.0        # Actual Payouts
    
    excluded_payouts_total = 0.0   # Track excluded amounts for reconciliation
    
    with open(csv_file, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Parse the main Date
            date_str = row.get('Date')
            payout_date = parse_date(date_str)
            
            if not payout_date:
                continue
            
            # Filter by Payout Month
            if payout_date.year == year and payout_date.month == month:
                row_type = row.get('Type')
                conf_code = row.get('Confirmation code', '')
                
                # For Payout rows, value is in 'Paid out' column
                # For Reservations, value is in 'Amount' column
                if row_type == 'Payout':
                    val_str = row.get('Paid out', '0')
                else:
                    val_str = row.get('Amount', '0')
                
                amount_str = val_str.replace(',', '') if val_str else '0'
                
                try:
                    amount = float(amount_str)
                except ValueError:
                    continue

                # 1. Sum up actual Payouts (Money hitting the bank)
                if row_type == 'Payout':
                    total_payout_cash += amount
                    payouts.append({
                        'date': payout_date,
                        'amount': amount,
                        'details': row.get('Details', '')
                    })
                
                # 2. Collect Reservations (Revenue Base)
                elif row_type == 'Reservation' and amount > 0:
                    # Capture Service Fee and Gross Earnings
                    try:
                        service_fee = float(row.get('Service fee', '0').replace(',', ''))
                    except ValueError:
                        service_fee = 0.0
                        
                    try:
                        gross_earn = float(row.get('Gross earnings', '0').replace(',', ''))
                    except ValueError:
                        gross_earn = amount + service_fee # Fallback
                    
                    # CHECK EXCLUSIONS
                    if conf_code in EXCLUDED_CODES:
                        excluded_payouts_total += amount # Net amount received
                        print(f"ℹ️  Excluding legacy reservation: {row.get('Guest')} ({conf_code}) - {amount} PLN")
                        continue

                    reservations.append({
                        'date': payout_date, # Date received
                        'type': row_type,
                        'guest': row.get('Guest', 'System/Airbnb'),
                        'code': row.get('Confirmation code', 'N/A'),
                        'start': parse_date(row.get('Start date')),
                        'end': parse_date(row.get('End date')),
                        'nights': row.get('Nights', '-'),
                        'amount_net': amount,      # 'Amount' col
                        'service_fee': service_fee,
                        'gross_earnings': gross_earn,
                        'listing': row.get('Listing', '')
                    })
                    total_revenue_net_airbnb += amount
                    total_revenue_gross += gross_earn
                    total_service_fees += service_fee

    if not payouts and not reservations:
        print(f"⚠️  No payouts found for {month_str}")
        return None
    
    # Sort reservations by date
    reservations.sort(key=lambda x: x['date'])
    
    # Calculate VAT Import (23%) on Service Fees
    vat_rate = 0.23
    vat_import_amount = round(total_service_fees * vat_rate, 2)
    
    # Calculate Ryczałt Tax Base
    tax_base_ryczalt = total_revenue_gross
    tax_ryczalt_amount = calculate_tax(tax_base_ryczalt)
    
    # Generate summary document
    summary_md = generate_summary_markdown(
        year, month, reservations, 
        total_revenue_gross, total_service_fees, vat_import_amount,
        total_payout_cash, tax_ryczalt_amount, excluded_payouts_total
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
        year, month, reservations, 
        total_revenue_gross, total_service_fees, vat_import_amount,
        tax_ryczalt_amount, excluded_payouts_total
    )
    
    email_path = summary_path.parent / f"Email_ksiegowa_{month_str}.txt"
    with open(email_path, 'w', encoding='utf-8') as f:
        f.write(email_template)
    
    print(f"✅ Email template: {email_path}")
    
    return {
        'month': month_str,
        'count': len(reservations),
        'revenue_gross': total_revenue_gross,
        'service_fees': total_service_fees,
        'vat_import': vat_import_amount,
        'payout': total_payout_cash,
        'tax_ryczalt': tax_ryczalt_amount,
        'excluded': excluded_payouts_total,
        'summary_path': summary_path
    }

def generate_summary_markdown(year, month, reservations, total_revenue_gross, total_service_fees, vat_import_amount, total_payout_cash, tax_ryczalt_amount, excluded_payouts_total=0.0):
    """Generate Markdown summary document"""
    
    month_names_pl = [
        'Styczeń', 'Luty', 'Marzec', 'Kwiecień', 'Maj', 'Czerwiec',
        'Lipiec', 'Sierpień', 'Wrzesień', 'Październik', 'Listopad', 'Grudzień'
    ]
    
    month_name = month_names_pl[month - 1]
    
    deductions = total_revenue_gross - (total_payout_cash - excluded_payouts_total)
    
    md = f"""# Podsumowanie Finansowe Najmu (JDG) - {month_name} {year}

---

## 💰 1. RYCZAŁT: Przychód i Podatek Dochodowy

Podatek dochodowy (PPE) od najmu w ramach działalności gospodarczej.

- **Przychód Brutto (Gross Earnings):** {total_revenue_gross:,.2f} PLN
- *Uwaga: Podstawa opodatkowania ryczałtem obejmuje kwotę brutto (wraz z opłatą serwisową Airbnb), ponieważ koszty są nieodliczalne.*
- **Stawka ryczałtu:** 8.5%
- **Podatek PPE do zapłaty:** **{tax_ryczalt_amount} PLN**

**(Podstawa: Art. 12 ust. 1 pkt 4 lit. a ustawy o ryczałcie)**

---

## 🇪🇺 2. VAT: Import Usług (Art. 28b)

Podatek VAT od usług nabytych od podmiotu zagranicznego (Airbnb Ireland).
Brak prawa do odliczenia (usługa związana ze sprzedażą zwolnioną).

- **Suma Opłat Serwisowych Airbnb (Netto wg faktur Airbnb):** {total_service_fees:,.2f} PLN
- **Stawka VAT (Polska):** 23%
- **VAT Import do zapłaty:** **{vat_import_amount} PLN**

---

## 📉 3. Rozliczenie Wpłat (Saldo)

- **Faktyczny wpływ na konto:** {total_payout_cash:,.2f} PLN
- **Potrącenia i Wyłączenia:**
  - *Opłaty serwisowe Airbnb:* {total_service_fees:,.2f} PLN
  - *Opłaty za sprzątanie/kary (Cancellation):* {(deductions - total_service_fees):,.2f} PLN
"""

    if excluded_payouts_total > 0:
        md += f"  - *Wpłaty z najmu prywatnego (wyłączone z JDG):* {excluded_payouts_total:,.2f} PLN (dotyczy wcześniejszych okresów)\n"
    
    md += f"""
---

## 📋 Szczegółowa Lista Rezerwacji (JDG)

| Lp. | Gość | Data Wypłaty | Kod | Kwota Brutto (Gross) | Service Fee | Kwota Netto (Payout) |
|-----|------|--------------|-----|----------------------|-------------|----------------------|
"""
    
    for i, res in enumerate(reservations, 1):
        date_str = res['date'].strftime('%d.%m.%Y')
        md += f"| {i} | {res['guest']} | {date_str} | {res['code']} | {res['gross_earnings']:,.2f} | {res['service_fee']:,.2f} | {res['amount_net']:,.2f} |\n"
    
    md += f"""
---

## 📎 Załączniki dla Księgowej

1. **Niniejsze podsumowanie**
2. **Umowy najmu** ({len(reservations)} plików)
"""
    
    for item in reservations:
        start_str = item['start'].strftime('%Y-%m-%d')
        end_str = item['end'].strftime('%Y-%m-%d')
        guest_safe = item['guest'].replace(' ', '_')
        filename = f"Umowa_{start_str}_{end_str}_{guest_safe}"
        md += f"   - `{filename}.pdf` (Kwota z umowy: {item['amount_net']:,.2f} PLN)\n"
    
    md += f"""
---

## 📝 Uwagi

- Wszystkie kwoty w PLN
- Stawka podatku: 8.5% (Art. 12 ust. 1 pkt 4 lit. a) ustawy o zryczałtowanym podatku dochodowym)
- Podstawa prawna zwolnienia z VAT: Art. 43 ust. 1 pkt 36 ustawy o VAT
- Klasyfikacja PKWiU: 68.20.11.0 (Wynajem i dzierżawa własnych nieruchomości mieszkalnych)

---

**Wygenerowano:** {datetime.now().strftime('%d.%m.%Y %H:%M')}
"""
    
    return md

def generate_email_template(year, month, reservations, total_revenue_gross, total_service_fees, vat_import_amount, tax_ryczalt_amount, excluded_payouts_total=0.0):
    """Generate email template for accountant"""
    
    month_names_pl = [
        'styczeń', 'luty', 'marzec', 'kwiecień', 'maj', 'czerwiec',
        'lipiec', 'sierpień', 'wrzesień', 'październik', 'listopad', 'grudzień'
    ]
    
    month_name = month_names_pl[month - 1]
    
    template = f"""Temat: Dokumenty księgowe - {month_name.capitalize()} {year} - Najmu + Import Usług

Dzień dobry,

Przesyłam dokumentację księgową za {month_name} {year}:

1. RYCZAŁT (PPE):
- Przychód Brutto (Gross Earnings): {total_revenue_gross:,.2f} PLN
- Podatek Ryczałt (8.5%): {tax_ryczalt_amount} PLN

2. VAT IMPORT USŁUG (Art. 28b):
- Podstawa (Service Fees Airbnb): {total_service_fees:,.2f} PLN
- VAT należny (23%): {vat_import_amount} PLN
*(Usługa związana ze sprzedażą zwolnioną - brak prawa do odliczenia, VAT do zapłaty)*

📎 ZAŁĄCZNIKI:
1. Podsumowanie_{year}-{month:02d}.pdf (szczegóły transakcji i wyliczenia)
2. Umowy najmu ({len(reservations)} plików):
"""
    
    for i, item in enumerate(reservations, 1):
        start_str = item['start'].strftime('%Y-%m-%d')
        end_str = item['end'].strftime('%Y-%m-%d')
        guest_safe = item['guest'].replace(' ', '_')
        filename = f"Umowa_{start_str}_{end_str}_{guest_safe}.pdf"
        template += f"   {i}. {filename} - Kwota z umowy: {item['amount_net']:,.2f} PLN\n"
    
    if excluded_payouts_total > 0:
        template += f"""
❓ PYTANIE / UWAGA DO ROZLICZENIA:
Na konto firmowe wpłynęła dodatkowa kwota: {excluded_payouts_total:,.2f} PLN.
Dotyczy ona dopłaty/rozliczenia rezerwacji z poprzedniego okresu (najem prywatny przed założeniem/włączeniem działalności).
Proszę o informację, jak to ująć w KPiR/Ewidencji - czy doliczyć do przychodu JDG (mimo braku nowej umowy), czy potraktować jako wpływ prywatny?
"""
    
    template += f"""
💼 INFORMACJE DODATKOWE:
- Rodzaj działalności: Wynajem lokali mieszkalnych w ramach JDG
- Zwolnienie z VAT: Art. 43 ust. 1 pkt 36 (cel mieszkaniowy)
- PKWiU: 68.20.11.0
- Forma opodatkowania: Ryczałt 8.5% (Art. 12 ust. 1 pkt 4 lit. a) ustawy o ryczałcie)

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
        print(f"   Revenue (Gross): {result['revenue_gross']:,.2f} PLN")
        print(f"   Service Fees: {result['service_fees']:,.2f} PLN")
        print(f"   VAT Import (23%): {result['vat_import']} PLN")
        print(f"   Ryczalt (8.5%): {result['tax_ryczalt']} PLN")
        print("="*50)

if __name__ == "__main__":
    main()
