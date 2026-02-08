#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Batch PDF Generator
Converts all .md files in a folder to PDF using Puppeteer
"""

import os
import sys
import subprocess
from pathlib import Path

def check_node_installed():
    """Check if Node.js is installed"""
    try:
        result = subprocess.run(['node', '--version'], capture_output=True, text=True)
        return result.returncode == 0
    except FileNotFoundError:
        return False

def check_puppeteer_installed():
    """Check if puppeteer and marked are installed locally"""
    script_dir = Path(__file__).parent
    node_modules = script_dir / 'node_modules'
    
    # Check for local installation
    if (node_modules / 'puppeteer').exists() and (node_modules / 'marked').exists():
        return True
    
    # Fallback: check global installation
    try:
        result = subprocess.run(['npm', 'list', '-g', 'puppeteer'], capture_output=True, text=True)
        has_puppeteer = 'puppeteer@' in result.stdout
        
        result = subprocess.run(['npm', 'list', '-g', 'marked'], capture_output=True, text=True)
        has_marked = 'marked@' in result.stdout
        
        return has_puppeteer and has_marked
    except FileNotFoundError:
        return False

def convert_folder_to_pdf(folder_path):
    """Convert all .md files in folder to PDF"""
    
    # Verify Node.js is installed
    if not check_node_installed():
        print("❌ Node.js is not installed. Please install it from https://nodejs.org/")
        print("   After installation, run: npm install -g puppeteer marked")
        return
    
    # Verify Puppeteer is installed
    if not check_puppeteer_installed():
        print("⚠️  Puppeteer or Marked not found. Installing...")
        try:
            subprocess.run(['npm', 'install', '-g', 'puppeteer', 'marked'], check=True)
            print("✅ Puppeteer and Marked installed successfully")
        except subprocess.CalledProcessError:
            print("❌ Failed to install dependencies. Please run manually:")
            print("   npm install -g puppeteer marked")
            return
    
    # Find all .md files
    folder = Path(folder_path)
    if not folder.exists():
        print(f"❌ Folder not found: {folder_path}")
        return
    
    md_files = list(folder.rglob('*.md'))
    
    if not md_files:
        print(f"⚠️  No .md files found in {folder_path}")
        return
    
    print(f"🚀 Found {len(md_files)} Markdown file(s)")
    
    # Get path to md_to_pdf.js script
    script_dir = Path(__file__).parent
    node_script = script_dir / 'md_to_pdf.js'
    
    if not node_script.exists():
        print(f"❌ Node script not found: {node_script}")
        return
    
    # Convert each file
    success_count = 0
    for md_file in md_files:
        pdf_file = md_file.with_suffix('.pdf')
        
        # Skip if PDF already exists and is newer than MD
        if pdf_file.exists() and pdf_file.stat().st_mtime > md_file.stat().st_mtime:
            print(f"⏩ Skipping (PDF up-to-date): {md_file.name}")
            success_count += 1
            continue
        
        try:
            result = subprocess.run(
                ['node', str(node_script), str(md_file)],
                capture_output=True,
                text=True,
                timeout=30
            )
            
            if result.returncode == 0:
                success_count += 1
            else:
                print(f"❌ Failed: {md_file.name}")
                print(f"   Error: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print(f"⏱️  Timeout: {md_file.name}")
        except Exception as e:
            print(f"❌ Error converting {md_file.name}: {e}")
    
    print(f"\n🏁 Conversion complete: {success_count}/{len(md_files)} successful")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python batch_pdf.py <folder_path>")
        print("Example: python batch_pdf.py umowy_2026/2026-01")
        sys.exit(1)
    
    folder_path = sys.argv[1]
    convert_folder_to_pdf(folder_path)
