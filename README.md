# Rental Automation Toolkit

Automated tools for managing medium/long-term residential rentals in Poland via Airbnb.

## Features

- **Agreement Generation**: Automatically generate bilingual (PL/EN) rental agreements from Airbnb booking data
- **PDF Conversion**: Convert Markdown agreements to PDF using Puppeteer (headless Chrome)
- **Batch Processing**: Generate agreements for entire months from CSV exports
- **Monthly Summaries**: Automatic financial summaries with tax calculations (8.5% ryczałt)
- **Accountant Reports**: Ready-to-send email templates with attachment lists

## Requirements

- Python 3.8+
- Node.js 16+ (for PDF generation)
- npm packages: `puppeteer`, `marked`

## Installation

```powershell
# Install Python dependencies
pip install beautifulsoup4 jinja2

# Install Node.js dependencies
npm install
```

## Usage

### Generate Agreements from CSV

```powershell
# Generate all 2026 agreements
python csv_generator.py

# Agreements will be created in umowy_2026/YYYY-MM/ folders
```

### Convert Markdown to PDF

```powershell
# Convert all .md files in a folder
python batch_pdf.py "umowy_2026/2026-01"

# Convert entire year
python batch_pdf.py "umowy_2026"
```

### Generate Monthly Summary

```powershell
# Create financial summary for January 2026
python monthly_summary.py 2026-01

# Generates:
# - Podsumowanie_2026-01.pdf (summary document)
# - Email_ksiegowa_2026-01.txt (accountant email template)
```

## File Structure

```
.
├── airbnb_parser.py          # Core parsing logic
├── csv_generator.py           # Batch agreement generator
├── batch_pdf.py               # PDF conversion tool
├── monthly_summary.py         # Financial summary generator
├── md_to_pdf.js              # Node.js PDF converter (Puppeteer)
├── universal_rental_agreement.md  # Agreement template
├── guest_email_template.html # Email template for guests
└── package.json              # Node.js dependencies
```

## Tax Compliance

- **VAT Exemption**: Art. 43 ust. 1 pkt 36 (residential rental)
- **PKWiU Code**: 68.20.11.0 (Residential real estate rental)
- **Tax Rate**: 8.5% ryczałt (flat tax for private rental)
- **Agreement Date**: Set to check-in date for consistency

## Legal Notes

This toolkit is designed for Polish residential rental compliance:

- Distinguishes between private room and common area maintenance
- Avoids hotel service classification
- Implements implied consent mechanism (_per facta concludentia_)
- GDPR-compliant data handling

## License

MIT License - See LICENSE file for details

## Author

Marcin Kordas  
NIP: 677-244-60-64
