Not “Green Light” yet — there are a few **critical** fixes needed (1 legal consistency issue that can undermine the “no hotel services” narrative, and 2–3 parsing robustness gaps that can break automation on real Airbnb emails). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/3857962f-0947-4d7c-aaf0-c93446ec2ff6/b80ee403.docx)

## Critical corrections

- Legal safety (VAT & residential status): Your draft logic says “no cleaning service / no hotel services”, but the Airbnb email includes a charged “Opłata za sprzątanie 20,00 zł”, which (if not framed correctly) can be used to argue you provide lodging-like services. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/e9318a33-0117-4277-8e3f-566fdc3de101/Rezerwacja-potwierdzona-Octavio-Zacagnino-przyjezdza-27-lut.html)
  Fix: change the clause to “no periodic cleaning during stay” + explicitly allow **only end-of-stay turnover cleaning** (sprzątanie po zdaniu lokalu), which is operational/turnover, not a hotel service.

- Legal safety (VAT & exemption wording): The agreement text should avoid sounding like it “guarantees” VAT exemption; it should state the _intended classification_ and the tenant’s declared purpose (“wyłącznie na cele mieszkaniowe”), not promise the tax outcome. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/3857962f-0947-4d7c-aaf0-c93446ec2ff6/b80ee403.docx)
  Fix: keep the Art. 43 ust. 1 pkt 36 reference, but phrase it as: “Strony oświadczają, że najem jest na cele mieszkaniowe; Wynajmujący zamierza stosować zwolnienie…”.

- Implied consent mechanism: “concluded upon entry/payment” is directionally good, but to be defensible you want **(i)** proof of delivery of terms before check‑in and **(ii)** a clean “moment of conclusion” tied to Airbnb acceptance + access handover, not “entry” alone.  
  Fix: define conclusion as combined facts: confirmed booking + payment via Airbnb + delivery of access (keys/codes). Add: “Treść umowy została udostępniona Najemcy przed check‑in w wiadomości Airbnb/link; brak sprzeciwu i objęcie lokalu w posiadanie = akceptacja”.

- Completeness (placeholders): Your HTML guest email template uses placeholders like `{{ AGREEMENT_LINK }}` and `{{ THREAD_ID }}`, but your parser/generator doesn’t extract or populate them. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/e9318a33-0117-4277-8e3f-566fdc3de101/Rezerwacja-potwierdzona-Octavio-Zacagnino-przyjezdza-27-lut.html)
  Fix: treat them as “injected by orchestration layer” (e.g., your script uploads PDF and returns link; thread id optionally parsed from `hosting/thread...`).

## Parsing / QA issues (Python)

- Month parsing: Your month map covers `lut`, `lip`, etc., which matches the email (“pt., 27 lut”, “wt., 7 lip”). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/e9318a33-0117-4277-8e3f-566fdc3de101/Rezerwacja-potwierdzona-Octavio-Zacagnino-przyjezdza-27-lut.html)
  But you should handle variants like `paź` vs `paz`, and optional trailing dot (`lut.`), because Airbnb/locales sometimes differ.

- Year inference: Airbnb date strings in the email don’t include the year. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/e9318a33-0117-4277-8e3f-566fdc3de101/Rezerwacja-potwierdzona-Octavio-Zacagnino-przyjezdza-27-lut.html)
  Your current “if month < current_month then year+1” heuristic will fail for reservations > 12 months ahead (e.g., email in Feb 2026, booking in Mar 2027).

- Total price extraction: Relying on “Razem PLN” is fragile, and the plain-text view clearly exposes the breakdown that reconstructs the total reliably: 5 331,15 + 20,00 + 580,94 = 5 932,09. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/e9318a33-0117-4277-8e3f-566fdc3de101/Rezerwacja-potwierdzona-Octavio-Zacagnino-przyjezdza-27-lut.html)
  Fix: implement fallback: compute total from the breakdown if “Razem” not found.

## Corrected code snippet (dates + currency + total)

Drop-in replacements you can apply inside your parser:

```python
import re
from datetime import datetime

POLISH_MONTHS = {
    "sty": 1, "lut": 2, "mar": 3, "kwi": 4, "maj": 5, "cze": 6,
    "lip": 7, "sie": 8, "wrz": 9, "paz": 10, "paź": 10, "lis": 11, "gru": 12
}

def _clean_text(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip()

def parse_pl_day_month(date_str: str, ref_date: datetime) -> datetime:
    # Examples: "pt., 27 lut", "wt., 7 lip"
    s = _clean_text(date_str).lower()
    s = re.sub(r"^[a-ząćęłńóśźż]{2,3}\.?,?\s*", "", s)  # remove weekday prefix
    s = s.replace(".", "")  # handle "lut." etc.

    m = re.match(r"(\d{1,2})\s+([a-ząćęłńóśźż]{3})", s)
    if not m:
        raise ValueError(f"Cannot parse date: {date_str}")

    day = int(m.group(1))
    mon_abbr = m.group(2)
    month = POLISH_MONTHS.get(mon_abbr)
    if not month:
        raise ValueError(f"Unknown month abbreviation: {mon_abbr}")

    # Year inference: if month is "earlier" than email month, assume next year
    year = ref_date.year + (1 if month < ref_date.month else 0)
    return datetime(year, month, day)

def parse_pln_amount(text: str) -> float:
    # Examples: "5 932,09 zł", "580,94 zł"
    s = _clean_text(text).lower().replace("zł", "").strip()
    s = s.replace(" ", "")          # thousands sep
    s = s.replace(",", ".")         # decimal comma
    s = re.sub(r"[^0-9.\-]", "", s) # safety
    return float(s)

def extract_total_paid_from_breakdown(email_text: str) -> float:
    """
    Uses the visible breakdown present in the email:
    - "5 331,15 zł" (nightly subtotal)
    - "Opłata za sprzątanie" + "20,00 zł"
    - "Opłata serwisowa gościa" + "580,94 zł"
    """
    t = email_text

    def after(label: str):
        i = t.find(label)
        if i < 0:
            return None
        tail = t[i:i+400]  # local window
        m = re.search(r"(\d[\d\s\xa0]*,\d{2})\s*zł", tail)
        return parse_pln_amount(m.group(0)) if m else None

    subtotal = after("zł x")  # grabs "41,01 zł x 130 nocy" -> not amount; so don’t use
    nights_amount = None
    m = re.search(r"\n(\d[\d\s\xa0]*,\d{2})\s*zł\n\nOpłata za sprzątanie", t)
    if m:
        nights_amount = parse_pln_amount(m.group(1) + " zł")

    cleaning = after("Opłata za sprzątanie")
    guest_fee = after("Opłata serwisowa gościa")

    if nights_amount is None or cleaning is None or guest_fee is None:
        raise ValueError("Cannot reconstruct total from breakdown")

    return round(nights_amount + cleaning + guest_fee, 2)
```

And in your `parse()` you should set a reference date from the email itself (best), or at least from file timestamp as a fallback. The email contains the check-in/out strings and the fee breakdown exactly in this format, so the functions above will work on the Octavio sample. [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/e9318a33-0117-4277-8e3f-566fdc3de101/Rezerwacja-potwierdzona-Octavio-Zacagnino-przyjezdza-27-lut.html)

## GDPR compliance (email)

Your GDPR paragraph is _mostly OK_ (purpose + Art. 6(1)(b)/(c) is correctly stated), but it’s missing two practical elements often expected in an Art. 13-style notice:

- Categories of recipients/processors (Airbnb as platform/communication/payment intermediary; hosting/drive provider if you host the agreement link). [ppl-ai-file-upload.s3.amazonaws](https://ppl-ai-file-upload.s3.amazonaws.com/web/direct-files/attachments/75280359/e9318a33-0117-4277-8e3f-566fdc3de101/Rezerwacja-potwierdzona-Octavio-Zacagnino-przyjezdza-27-lut.html)
- Link or pointer to a full privacy notice (even a short URL), so you can keep the Airbnb message short but compliant.

If you want, I can rewrite (1) the “no hotel services” clause to be consistent with the presence of a cleaning fee and (2) the implied-consent clause into a stronger, more litigation-friendly PL/EN version, while keeping the template minimal.
