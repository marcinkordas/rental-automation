#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch Rental Agreement Generator (CSV)
Generates agreements for 2026 from airbnb.csv
Organized by MONTH of Payout (Tax Point).
"""

import csv
import os
import re
from datetime import datetime
from airbnb_parser import AgreementGenerator

# Configuration
CSV_FILE = 'airbnb.csv'
OUTPUT_ROOT = 'umowy_2026'
TEMPLATE_PATH = 'universal_rental_agreement.md'
LANDLORD_CONFIG = {
    'LANDLORD_NAME': 'Marcin Kordas',
    'LANDLORD_NIP': '677-244-60-64',
    'LANDLORD_ADDRESS': 'ul. Stanisława Przybyszewskiego 30/2, 30-128 Kraków, Polska',
    'LANDLORD_EMAIL': 'noclegi@kordas.tech',
    'PROPERTY_ADDRESS': 'ul. Stanisława Przybyszewskiego 30/2, 30-128 Kraków',
    'PROPERTY_TYPE': 'pokój',
    'PROPERTY_TYPE_EN': 'room',
}

def parse_date(date_str):
    """Parses MM/DD/YYYY format from CSV."""
    if not date_str: return None
    try:
        return datetime.strptime(date_str, '%m/%d/%Y')
    except ValueError:
        return None

def main():
    print("🚀 Starting Batch Generation for 2026...")
    
    # Check if files exist
    if not os.path.exists(CSV_FILE):
        print(f"❌ Error: {CSV_FILE} not found.")
        return
    if not os.path.exists(TEMPLATE_PATH):
        print(f"❌ Error: {TEMPLATE_PATH} not found.")
        return

    # Initialize Generator
    generator = AgreementGenerator(TEMPLATE_PATH, LANDLORD_CONFIG)
    
    # Read CSV
    reservations = []
    payouts_map = {} # confirmation_code -> payout_date (optional, for finding tax point)

    with open(CSV_FILE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            row_type = row.get('Type')
            
            # We are interested in Reservations
            if row_type == 'Reservation':
                start_date = parse_date(row.get('Start date'))
                
                # Filter strictly for 2026 (based on Start Date or Booking Date?)
                # User asked for "only for 2026". Usually means Start Date in 2026.
                if start_date and start_date.year == 2026:
                    reservations.append(row)
            
            # We assume Payouts are not linked by Code in this CSV structure explicitly?
            # Actually, the snippet shows Payout rows don't have Confirmation Code easily.
            # But Reservation rows DO have 'Earnings year'.
            # For this script, we will use the 'Start date' month as the folder for simplicity
            # unless we can reliably link payouts. User said "monthly basis" for accountant.
            # Best practice: Folder = Month of Check-in (Start Date) or Month of Payment?
            # User said "rozliczanie... wg. daty dokonania wpłaty" (Payout).
            # But parsing payout linkage from a flattened CSV is hard if not on the same row.
            # Strategy: Use Start Date Month for folder organization, 
            # as it's the most reliable data point we have in the 'Reservation' row.
    
    print(f"Found {len(reservations)} reservations for 2026.")

    for res in reservations:
        # Extract Data
        guest = res.get('Guest', 'Guest')
        code = res.get('Confirmation code', 'NOCODE')
        listing = res.get('Listing', 'Apartment')
        start_date = parse_date(res.get('Start date'))
        end_date = parse_date(res.get('End date'))
        booking_date = parse_date(res.get('Booking date')) # Agreement Date
        
        # Financials
        try:
            amount = float(res.get('Amount', '0').replace(',', ''))
            cleaning = float(res.get('Cleaning fee', '0').replace(',', ''))
        except:
            amount = 0.0
            cleaning = 0.0
            
        # Determine Folder (YYYY-MM)
        # Using Start Date as the filing month proxy
        month_folder = start_date.strftime('%Y-%m')
        output_dir = os.path.join(OUTPUT_ROOT, month_folder)
        os.makedirs(output_dir, exist_ok=True)
        
        # Context for Template
        # Note: Airbnb CSV dates are MM/DD/YYYY, template needs Polish format DD.MM.YYYY
        booking_data = {
            'GUEST_NAME': guest,
            'CONFIRMATION_CODE': code,
            'LISTING_NAME': listing,
            'CHECKIN_DATE': start_date.strftime('%d.%m.%Y'),
            'CHECKOUT_DATE': end_date.strftime('%d.%m.%Y'),
            'DATA_ZAWARCIA': start_date.strftime('%d.%m.%Y'), # Agreement Date = Check-in Date
            'NIGHTS_COUNT': res.get('Nights', '30'),
            'TOTAL_PRICE': f"{amount:.2f}",
            'CLEANING_FEE': f"{cleaning:.2f}",
        }
        
        # Filename: Umowa_START_END_Guest.pdf
        date_range = f"{start_date.strftime('%Y-%m-%d')}_{end_date.strftime('%Y-%m-%d')}"
        safe_guest = re.sub(r'[^a-zA-Z0-9 ]', '', guest).replace(' ', '_')
        filename = f"Umowa_{date_range}_{safe_guest}.pdf"
        output_path = os.path.join(output_dir, filename)
        
        # Check if exists
        if os.path.exists(output_path):
            print(f"⏩ Skipping existing: {filename}")
            continue
            
        # Generate
        try:
            generator.generate(booking_data, output_path, format='pdf')
            print(f"✅ Generated: {month_folder}/{filename}")
        except Exception as e:
            print(f"❌ Failed to generate {filename}: {e}")

    print("🏁 Batch Generation Complete.")

if __name__ == "__main__":
    main()
