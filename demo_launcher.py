#!/usr/bin/env python3
"""
1-Take Video Demo Launcher for ai-data-toolkit.
Automates running the demo commands and immediately opening the resulting
Excel spreadsheets so you can record your 90-second Loom/OBS demo without fumbling!
"""

import os
import sys
import subprocess
from pathlib import Path


def print_banner():
    print("=" * 65)
    print("🎬 AI DATA TOOLKIT — 1-TAKE VIDEO DEMO LAUNCHER")
    print("=" * 65)
    print("Choose a demo mode to record:")
    print("  [1] Invoice Batch Register (Recommended for 90s Demo)")
    print("      -> Runs extract_invoice.py on samples/ --batch")
    print("      -> Auto-opens Master_Invoice_Register.xlsx")
    print("  [2] B2B Lead Cleaner & Normalizer")
    print("      -> Runs clean_scraped_data.py on samples/raw_business_leads_3.txt")
    print("      -> Auto-opens clean_leads_raw_business_leads_3.xlsx")
    print("=" * 65)


def open_file_in_os(file_path: Path):
    """Opens the generated file using the OS default application."""
    try:
        if sys.platform == "win32":
            os.startfile(str(file_path))
        elif sys.platform == "darwin":
            subprocess.run(["open", str(file_path)])
        else:
            subprocess.run(["xdg-open", str(file_path)])
        print(f"\n📂 Auto-opened: {file_path.name}")
    except Exception as e:
        print(f"\n⚠️ Could not auto-open {file_path}: {e}")
        print(f"👉 Please open manually from: {file_path.resolve()}")


def run_invoice_demo():
    print("\n🚀 [Scene 2] Running Batch Invoice Extraction...")
    cmd = [sys.executable, "extract_invoice.py", "samples/", "--batch"]
    res = subprocess.run(cmd)
    if res.returncode == 0:
        target = Path("output") / "Master_Invoice_Register.xlsx"
        if target.exists():
            print("\n" + "-" * 65)
            print("🟢 CUE: Switch to Excel now and point to cell E13 (Formula =C13*D13)!")
            print("-" * 65)
            open_file_in_os(target)
    else:
        print("❌ Demo run failed. Check terminal logs.")


def run_lead_demo():
    print("\n🚀 [Scene 2] Running Scraped Lead Cleaning...")
    cmd = [sys.executable, "clean_scraped_data.py", "samples/raw_business_leads_3.txt"]
    res = subprocess.run(cmd)
    if res.returncode == 0:
        target = Path("output") / "clean_leads_raw_business_leads_3.xlsx"
        if target.exists():
            print("\n" + "-" * 65)
            print("🟢 CUE: Point to Freeze Panes at row 8 and clickable mailto: links!")
            print("-" * 65)
            open_file_in_os(target)
    else:
        print("❌ Demo run failed. Check terminal logs.")


def main():
    print_banner()
    choice = input("\nEnter choice [1 or 2] (Default: 1): ").strip()
    if choice == "2":
        run_lead_demo()
    else:
        run_invoice_demo()


if __name__ == "__main__":
    main()
