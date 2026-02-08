#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Airbnb Rental Agreement Parser & Generator
Optimized for Polish medium/long-term residential rentals.
"""

import re
from datetime import datetime
import warnings
from bs4 import BeautifulSoup
from jinja2 import Template

# Optional: For PDF generation
try:
    from markdown import markdown
    from xhtml2pdf import pisa
    PDF_AVAILABLE = True
except (ImportError, OSError):
    PDF_AVAILABLE = False

POLISH_MONTHS = {
    'stycznia': 1, 'lutego': 2, 'marca': 3, 'kwietnia': 4, 'maja': 5, 'czerwca': 6,
    'lipca': 7, 'sierpnia': 8, 'września': 9, 'października': 10, 'listopada': 11, 'grudnia': 12
}

def _clean_text(s: str) -> str:
    """Standardizes whitespace and removes NBSP."""
    if not s: return ""
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()

def parse_pl_day_month(date_str: str, ref_date: datetime) -> datetime:
    """
    Parses Polish date strings like 'pt., 27 lut' or 'wt., 7 lip.'.
    Infers the year based on reference date.
    """
    s = _clean_text(date_str).lower()
    # Remove weekday prefix (2-3 chars + optional dot/comma)
    s = re.sub(r"^[a-ząćęłńóśźż]{2,3}\.?,?\s*", "", s)
    s = s.replace(".", "")  # Handle "lut." vs "lut"

    m = re.match(r"(\d{1,2})\s+([a-ząćęłńóśźż]{3})", s)
    if not m:
        raise ValueError(f"Cannot parse date: {date_str}")

    day = int(m.group(1))
    mon_abbr = m.group(2)
    month = POLISH_MONTHS.get(mon_abbr)
    if not month:
        raise ValueError(f"Unknown month abbreviation: {mon_abbr}")

    # Year inference: handles bookings spanning across New Year
    year = ref_date.year
    if month < ref_date.month and (ref_date.month - month) > 6:
        # If we are in Dec and booking is in Jan, it's next year
        year += 1
    elif month < ref_date.month:
        # Fallback heuristic from rewizja.md
        year += 1
        
    return datetime(year, month, day)

def parse_pln_amount(text: str) -> float:
    """Parses currency strings like '5 932,09 zł' into float."""
    s = _clean_text(text).lower().replace("zł", "").strip()
    s = s.replace(" ", "")           # Remove thousands separator
    s = s.replace(",", ".")          # Convert decimal comma to dot
    s = re.sub(r"[^0-9.\-]", "", s)  # Security filter
    return float(s)

class AirbnbParser:
    def __init__(self, html_content: str, ref_date: datetime = None):
        self.soup = BeautifulSoup(html_content, 'html.parser')
        self.text = self.soup.get_text("\n")
        self.ref_date = ref_date or datetime.now()

    def extract_total_from_breakdown(self) -> float:
        """Computes total by summing nightly rate, cleaning, and guest fee."""
        t = self.text
        
        def after(label: str):
            i = t.find(label)
            if i < 0: return 0.0
            tail = t[i:i+400]
            m = re.search(r"(\d[\d\s\xa0]*,\d{2})\s*zł", tail)
            return parse_pln_amount(m.group(0)) if m else 0.0

        # Extracting nightly subtotal (Amount BEFORE 'Opłata za sprzątanie')
        m_nights = re.search(r"\n(\d[\d\s\xa0]*,\d{2})\s*zł\n\nOpłata za sprzątanie", t)
        nights_amount = parse_pln_amount(m_nights.group(1) + " zł") if m_nights else 0.0
        
        cleaning = after("Opłata za sprzątanie")
        guest_fee = after("Opłata serwisowa gościa")
        
        return round(nights_amount + cleaning + guest_fee, 2)

    def extract_booking_data(self):
        cleaning_fee = self._extract_cleaning_fee()
        # Basic fields
        data = {
            "CONFIRMATION_CODE": self._find_next_to("Kod potwierdzenia"),
            "GUEST_NAME": self._extract_guest_name(),
            "LISTING_NAME": self._extract_listing_name(),
            "NIGHTS_COUNT": self._extract_nights(),
            "CLEANING_FEE": cleaning_fee,
            "TOTAL_PRICE": self.extract_total_from_breakdown(),
            "CHECKIN_DATE": self._extract_date("Zameldowanie"),
            "CHECKOUT_DATE": self._extract_date("Wymeldowanie"),
        }
        return data

    def _extract_cleaning_fee(self) -> float:
        """Extracts cleaning fee from breakdown."""
        t = self.text
        i = t.find("Opłata za sprzątanie")
        if i < 0: return 0.0
        tail = t[i:i+200]
        m = re.search(r"(\d[\d\s\xa0]*,\d{2})\s*zł", tail)
        return parse_pln_amount(m.group(0)) if m else 0.0

    def _find_next_to(self, label: str):
        elem = self.soup.find(string=lambda t: t and label in t)
        if elem:
            # Common pattern in Airbnb emails: Label is in a <p>, value is in next <p>
            parent = elem.find_parent()
            if parent:
                nxt = parent.find_next('p')
                if nxt: return _clean_text(nxt.get_text())
        return "N/A"

    def _extract_guest_name(self):
        # Look for the 'Subject' line if present in raw view, otherwise specific greetings
        m = re.search(r"Rezerwacja potwierdzona\s*-\s*([^\s]+)\s+", self.text)
        if m: return m.group(1)
        return "Guest"

    def _extract_listing_name(self):
        h2 = self.soup.find('h2')
        if h2: return _clean_text(h2.get_text())
        return "Apartment"

    def _extract_nights(self):
        m = re.search(r"x\s*(\d+)\s*noc", self.text)
        return int(m.group(1)) if m else 30

    def _extract_date(self, label: str):
        raw = self._find_next_to(label)
        try:
            dt = parse_pl_day_month(raw, self.ref_date)
            return dt.strftime("%d.%m.%Y")
        except:
            return raw

class AgreementGenerator:
    def __init__(self, template_path: str, landlord_config: dict):
        with open(template_path, 'r', encoding='utf-8') as f:
            self.template = Template(f.read())
        self.landlord = landlord_config

    def generate(self, booking_data: dict, output_path: str, format="pdf"):
        context = {**self.landlord, **booking_data}
        if "DATA_ZAWARCIA" not in context:
            context["DATA_ZAWARCIA"] = datetime.now().strftime("%d.%m.%Y")
        
        md_content = self.template.render(**context)
        
        # Always save MD as backup/base
        md_path = output_path.replace('.pdf', '.md')
        with open(md_path, 'w', encoding='utf-8') as f:
            f.write(md_content)
        
        if format == "pdf" and PDF_AVAILABLE:
            try:
                html_text = markdown(md_content, extensions=['tables'])
                # Basic styling for PDF
                styled_html = f"""
                <html>
                <head>
                <style>
                    body {{ font-family: Helvetica, sans-serif; font-size: 10pt; }}
                    h1 {{ font-size: 16pt; text-align: center; margin-bottom: 20px; }}
                    h2 {{ font-size: 12pt; border-bottom: 1px solid #ccc; margin-top: 15px; margin-bottom: 10px; }}
                    p {{ margin-bottom: 5px; }}
                    table {{ width: 100%; border-collapse: collapse; margin-bottom: 10px; }}
                    th, td {{ border: 1px solid #ddd; padding: 5px; text-align: left; }}
                    th {{ background-color: #f9f9f9; }}
                </style>
                </head>
                <body>
                {html_text}
                </body>
                </html>
                """
                
                with open(output_path, "wb") as pdf_file:
                    pisa_status = pisa.CreatePDF(styled_html, dest=pdf_file)

                if pisa_status.err:
                    print(f"⚠️ PDF generation error for {output_path}")
            except Exception as e:
                print(f"⚠️ PDF generation failed for {output_path}: {e}")
                print(f"   (Saved as Markdown only: {md_path})")
        else:
            print(f"ℹ️ PDF libraries missing or format not supported. Saved as MD: {md_path}")

if __name__ == "__main__":
    # Example manual test (adjust filename as needed)
    print("Airbnb Parser initialized.")
