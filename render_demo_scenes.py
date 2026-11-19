#!/usr/bin/env python3
"""
Renders 4 ultra-crisp 1080p (1920x1080) visual scene frames for the AI Data Toolkit demo video:
- Scene 1: Dark-mode text editor with messy invoice & highlighted problem areas
- Scene 2: Sleek terminal window with animated batch command & streaming logs
- Scene 3: High-resolution Excel register with live formula callouts & KPI cards
- Scene 4: Commercial offer & risk-free guarantee outro slide
"""

import os
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

OUTPUT_DIR = Path("temp_frames")
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

# Colors
BG_DARK = (11, 15, 25)
CARD_BG = (15, 23, 42)
CARD_BORDER = (51, 65, 85)
TEXT_WHITE = (248, 250, 252)
TEXT_MUTED = (148, 163, 184)
TEXT_CYAN = (56, 189, 248)
TEXT_GREEN = (0, 200, 117)
TEXT_AMBER = (245, 158, 11)
TEXT_NAVY = (27, 54, 93)

FONT_CODE_LG = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 26)
FONT_CODE_MD = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 20)
FONT_CODE_SM = ImageFont.truetype(r"C:\Windows\Fonts\consola.ttf", 16)
FONT_UI_TITLE = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 44)
FONT_UI_SUB = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 24)
FONT_UI_BOLD = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 28)
FONT_UI_SM = ImageFont.truetype(r"C:\Windows\Fonts\segoeui.ttf", 18)


def draw_window_frame(draw, x, y, w, h, title=""):
    """Draws a macOS / VS Code styled dark window container with traffic light controls."""
    # Main window box
    draw.rounded_rectangle([x, y, x + w, y + h], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
    # Header bar
    draw.rounded_rectangle([x, y, x + w, y + 48], radius=16, fill=(30, 41, 59))
    draw.rectangle([x, y + 32, x + w, y + 48], fill=(30, 41, 59))
    draw.line([x, y + 48, x + w, y + 48], fill=CARD_BORDER, width=1)
    
    # Traffic light dots
    draw.ellipse([x + 20, y + 17, x + 34, y + 31], fill=(239, 68, 68))   # Red
    draw.ellipse([x + 44, y + 17, x + 58, y + 31], fill=(245, 158, 11))  # Amber
    draw.ellipse([x + 68, y + 17, x + 82, y + 31], fill=(16, 185, 129))  # Green

    # Window title
    if title:
        draw.text((x + 110, y + 12), title, font=FONT_CODE_MD, fill=TEXT_MUTED)


def render_scene_1_messy_input():
    img = Image.new("RGB", (1920, 1080), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Top Banner Header
    draw.text((120, 50), "🔴 SCENE 1: THE MANUAL DATA ENTRY HEADACHE", font=FONT_UI_BOLD, fill=TEXT_AMBER)
    draw.text((120, 95), "Raw, inconsistent logistics & freight documents that cost teams 15-20 hours a week", font=FONT_UI_SUB, fill=TEXT_MUTED)

    # Window
    win_x, win_y, win_w, win_h = 120, 150, 1680, 860
    draw_window_frame(draw, win_x, win_y, win_w, win_h, "samples/raw_invoice_1.txt — Plain Text Document")

    # Document contents
    content = [
        ("==========================================================================================", TEXT_MUTED),
        ("                  GLOBAL PACIFIC LOGISTICS & FREIGHT SERVICES                             ", TEXT_WHITE),
        ("                      1044 Harbor View Blvd, Ste 400, Long Beach, CA 90802               ", TEXT_MUTED),
        ("------------------------------------------------------------------------------------------", TEXT_MUTED),
        ("INVOICE NUMBER: INV-2026-8819B           ISSUED: 14-Nov-2026       DUE: 14-Dec-2026       ", TEXT_CYAN),
        ("CURRENCY: USD                            PAYMENT TERMS: Net 30 days                       ", TEXT_MUTED),
        ("", TEXT_MUTED),
        ("BILLED TO: Apex Commercial Retailers Inc. (VAT: US-TX-9948201)                            ", TEXT_WHITE),
        ("ATTN: Accounts Payable, 742 Industrial Pkwy, Bldg C, Dallas, TX                           ", TEXT_MUTED),
        ("", TEXT_MUTED),
        ("LINE ITEMS EXTRACTED:", TEXT_AMBER),
        ("  1. Ocean Freight Container 40ft (Shanghai -> LA)   Qty: 2 | Rate: $2,150.00 | $4,300.00", TEXT_WHITE),
        ("  2. Customs Clearance & Harbor Drayage Fee          Qty: 1 | Rate: $420.00   | $420.00  ", TEXT_WHITE),
        ("  3. Chassis Inspection & Terminal Handling (LFD)    Qty: 1 | Rate: $185.00   | $185.00  ", TEXT_WHITE),
        ("", TEXT_MUTED),
        ("FINANCIAL BREAKDOWN (FRAGMENTED):", TEXT_AMBER),
        ("  Subtotal Amount:                $4,905.00                                               ", TEXT_WHITE),
        ("  Fuel Surcharge (4.5%):          $220.73                                                 ", TEXT_MUTED),
        ("  California State Logistics Tax: $73.58                                                  ", TEXT_MUTED),
        ("  Early Booking Credit:          -$69.17 (Discount)                                       ", TEXT_GREEN),
        ("------------------------------------------------------------------------------------------", TEXT_MUTED),
        ("  TOTAL BALANCE DUE:              $5,130.14 [PAYMENT DUE]                                 ", TEXT_CYAN),
        ("==========================================================================================", TEXT_MUTED),
    ]

    cur_y = win_y + 70
    for line, col in content:
        draw.text((win_x + 50, cur_y), line, font=FONT_CODE_MD, fill=col)
        cur_y += 31

    # Callout Annotation on the side
    callout_x = 1180
    callout_y = 480
    draw.rounded_rectangle([callout_x, callout_y, callout_x + 560, callout_y + 240], radius=12, fill=(30, 41, 59), outline=TEXT_AMBER, width=2)
    draw.text((callout_x + 25, callout_y + 25), "⚠️ The Problem With Manual Entry:", font=FONT_UI_BOLD, fill=TEXT_AMBER)
    draw.text((callout_x + 25, callout_y + 75), "• Copy-pasting line items creates typing errors", font=FONT_UI_SM, fill=TEXT_WHITE)
    draw.text((callout_x + 25, callout_y + 115), "• Disconnected tax & discounts break ledger sums", font=FONT_UI_SM, fill=TEXT_WHITE)
    draw.text((callout_x + 25, callout_y + 155), "• Naive scripts hardcode static numbers", font=FONT_UI_SM, fill=TEXT_WHITE)
    draw.text((callout_x + 25, callout_y + 195), "• Wastes hours of expensive human staff time", font=FONT_UI_SM, fill=TEXT_MUTED)

    path = OUTPUT_DIR / "scene1_messy_invoice.png"
    img.save(path)
    print(f"✓ Rendered: {path}")


def render_scene_2_terminal_run():
    img = Image.new("RGB", (1920, 1080), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Top Banner Header
    draw.text((120, 50), "⚡ SCENE 2: THE 5-SECOND AUTOMATION RUNNER", font=FONT_UI_BOLD, fill=TEXT_CYAN)
    draw.text((120, 95), "Cloud-streamed inference engine with zero local GPU dependencies (<45MB RAM)", font=FONT_UI_SUB, fill=TEXT_MUTED)

    # Terminal Window
    win_x, win_y, win_w, win_h = 120, 150, 1680, 860
    draw_window_frame(draw, win_x, win_y, win_w, win_h, "PowerShell 7.4 — ai-data-toolkit — Cloud AI Batch Extraction")

    logs = [
        ("PS C:\\Users\\Developer\\ai-data-toolkit> python extract_invoice.py samples/ --batch", TEXT_WHITE),
        ("", TEXT_MUTED),
        ("📂 Scanning input directory for business documents: samples/", TEXT_CYAN),
        ("🧩 Auto-detected 3 invoice/receipt file(s) in queue.", TEXT_MUTED),
        ("", TEXT_MUTED),
        ("  [1/3] Normalizing: raw_invoice_1.txt ... ✓ INV-2026-8819B  [$5,130.14] (Ocean Freight)", TEXT_GREEN),
        ("  [2/3] Normalizing: raw_invoice_2.txt ... ✓ INV-CYBER-2026-904 [$13,725.00] (Cybersecurity)", TEXT_GREEN),
        ("  [3/3] Normalizing: raw_receipt_2.txt ... ✓ REC-2026-11-0492  [$24.75] (POS Receipt)", TEXT_GREEN),
        ("", TEXT_MUTED),
        ("📊 Generating Executive Master Register with dynamic Excel formulas...", TEXT_CYAN),
        ("  ✓ Injected row formulas: =C13*D13 (Quantity x Rate)", TEXT_MUTED),
        ("  ✓ Injected subtotal formulas: =SUM(E13:E15)", TEXT_MUTED),
        ("  ✓ Injected balance formulas: =E18+E19+E20", TEXT_MUTED),
        ("  ✓ Created dedicated audit sheet tabs for each invoice", TEXT_MUTED),
        ("", TEXT_MUTED),
        ("==========================================================================", TEXT_MUTED),
        ("✅ BATCH INVOICE EXTRACTION COMPLETE (10/10 PRODUCTION STANDARD)", TEXT_GREEN),
        ("==========================================================================", TEXT_MUTED),
        ("• Total Invoices Extracted:  3", TEXT_WHITE),
        ("• Cumulative Spend Balance:  $18,879.89", TEXT_CYAN),
        ("• Average Spend per Invoice: $6,293.30", TEXT_WHITE),
        ("• System Memory Footprint:   < 45MB RAM (Standard laptop safe)", TEXT_GREEN),
        ("• Output Master Register:    output/Master_Invoice_Register.xlsx", TEXT_AMBER),
    ]

    cur_y = win_y + 70
    for line, col in logs:
        draw.text((win_x + 50, cur_y), line, font=FONT_CODE_MD, fill=col)
        cur_y += 31

    path = OUTPUT_DIR / "scene2_terminal_run.png"
    img.save(path)
    print(f"✓ Rendered: {path}")


def render_scene_3_excel_master():
    img = Image.new("RGB", (1920, 1080), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Top Banner Header
    draw.text((120, 45), "📊 SCENE 3: PUBLICATION-GRADE EXCEL WITH LIVE FORMULAS", font=FONT_UI_BOLD, fill=TEXT_GREEN)
    draw.text((120, 90), "Never hardcode static numbers. Edits to line quantities automatically recalculate the entire workbook.", font=FONT_UI_SUB, fill=TEXT_MUTED)

    # Excel Application Window
    win_x, win_y, win_w, win_h = 120, 140, 1680, 880
    draw_window_frame(draw, win_x, win_y, win_w, win_h, "Microsoft Excel — Master_Invoice_Register.xlsx — Executive Register")

    # Formula Bar Simulation
    draw.rectangle([win_x + 20, win_y + 55, win_x + win_w - 20, win_y + 95], fill=(30, 41, 59), outline=CARD_BORDER)
    draw.text((win_x + 35, win_y + 63), "Cell E13", font=FONT_CODE_MD, fill=TEXT_MUTED)
    draw.line([win_x + 150, win_y + 55, win_x + 150, win_y + 95], fill=CARD_BORDER, width=1)
    draw.text((win_x + 170, win_y + 63), "fx [ =C13*D13 ]   (Dynamic Line Multiplier)", font=FONT_CODE_MD, fill=TEXT_CYAN)

    # 3 Executive KPI Cards
    kpis = [
        ("TOTAL INVOICES", "3", win_x + 50),
        ("CUMULATIVE SPEND", "$18,879.89", win_x + 480),
        ("AVERAGE INVOICE VALUE", "$6,293.30", win_x + 910),
        ("ACTIVE FORMULA ENGINE", "100% DYNAMIC", win_x + 1340)
    ]
    for label, val, k_x in kpis:
        draw.rounded_rectangle([k_x, win_y + 115, k_x + 280, win_y + 205], radius=10, fill=(30, 41, 59), outline=CARD_BORDER, width=1)
        draw.text((k_x + 20, win_y + 128), label, font=FONT_UI_SM, fill=TEXT_MUTED)
        draw.text((k_x + 20, win_y + 155), val, font=FONT_UI_BOLD, fill=TEXT_CYAN if "$" in val else TEXT_GREEN)

    # Table Headers
    t_y = win_y + 230
    draw.rectangle([win_x + 50, t_y, win_x + win_w - 50, t_y + 40], fill=TEXT_NAVY)
    headers = [
        ("INVOICE #", 70), ("SUPPLIER NAME", 280), ("BILLED CLIENT", 640),
        ("DATE ISSUED", 980), ("TOTAL BALANCE", 1200), ("STATUS PILL", 1440)
    ]
    for h_name, h_pos in headers:
        draw.text((win_x + h_pos, t_y + 8), h_name, font=FONT_CODE_MD, fill=TEXT_WHITE)

    # Rows
    rows = [
        ("INV-2026-8819B", "Global Pacific Logistics", "Apex Commercial", "14-Nov-2026", "$5,130.14", "PAYMENT DUE", (239, 68, 68)),
        ("INV-CYBER-2026-904", "Sentinel Core Security", "Vanguard Financial", "10-Nov-2026", "$13,725.00", "APPROVED", (16, 185, 129)),
        ("REC-2026-11-0492", "Bella Italia Trattoria", "Guest Customer", "02-Nov-2026", "$24.75", "PAID CASH", (56, 189, 248)),
    ]

    row_y = t_y + 42
    for inv, supp, client, dt, tot, stat, stat_col in rows:
        draw.rectangle([win_x + 50, row_y, win_x + win_w - 50, row_y + 46], fill=(15, 23, 42) if (row_y // 46) % 2 == 0 else (20, 30, 50))
        draw.line([win_x + 50, row_y + 46, win_x + win_w - 50, row_y + 46], fill=CARD_BORDER)
        draw.text((win_x + 70, row_y + 10), inv, font=FONT_CODE_MD, fill=TEXT_CYAN)
        draw.text((win_x + 280, row_y + 10), supp, font=FONT_CODE_MD, fill=TEXT_WHITE)
        draw.text((win_x + 640, row_y + 10), client, font=FONT_CODE_MD, fill=TEXT_MUTED)
        draw.text((win_x + 980, row_y + 10), dt, font=FONT_CODE_MD, fill=TEXT_MUTED)
        draw.text((win_x + 1200, row_y + 10), tot, font=FONT_CODE_MD, fill=TEXT_GREEN)

        # Status Pill
        draw.rounded_rectangle([win_x + 1430, row_y + 8, win_x + 1600, row_y + 38], radius=6, fill=(30, 41, 59), outline=stat_col, width=1)
        draw.text((win_x + 1445, row_y + 12), stat, font=FONT_CODE_SM, fill=stat_col)
        row_y += 48

    # Formula Callout Banner Box
    callout_y = row_y + 25
    draw.rounded_rectangle([win_x + 50, callout_y, win_x + win_w - 50, callout_y + 140], radius=12, fill=(30, 41, 59), outline=TEXT_GREEN, width=2)
    draw.text((win_x + 80, callout_y + 20), "⚡ Native Formula Engine Breakdown:", font=FONT_UI_BOLD, fill=TEXT_GREEN)
    draw.text((win_x + 80, callout_y + 60), "• Line Item Multiplication:   =C13*D13      (Automatically recalculates if rate or quantity changes)", font=FONT_CODE_MD, fill=TEXT_WHITE)
    draw.text((win_x + 80, callout_y + 95), "• Dynamic Group Subtotals:    =SUM(E13:E15) (Standardized accounting compliance)", font=FONT_CODE_MD, fill=TEXT_CYAN)

    # Bottom Sheet Tabs
    tab_y = win_y + win_h - 45
    draw.rectangle([win_x + 20, tab_y, win_x + win_w - 20, win_y + win_h - 10], fill=(15, 23, 42))
    tabs = ["📁 Master Register", "📄 INV-2026-8819B", "📄 INV-CYBER-904", "📄 REC-0492"]
    cur_tab_x = win_x + 40
    for idx, t_name in enumerate(tabs):
        draw.rounded_rectangle([cur_tab_x, tab_y - 5, cur_tab_x + 200, tab_y + 30], radius=6, fill=TEXT_NAVY if idx == 0 else (30, 41, 59))
        draw.text((cur_tab_x + 15, tab_y + 3), t_name, font=FONT_CODE_SM, fill=TEXT_WHITE)
        cur_tab_x += 215

    path = OUTPUT_DIR / "scene3_excel_master.png"
    img.save(path)
    print(f"✓ Rendered: {path}")


def render_scene_4_commercial_outro():
    img = Image.new("RGB", (1920, 1080), BG_DARK)
    draw = ImageDraw.Draw(img)

    # Brand Title
    draw.text((120, 80), "⚡ AI DATA EXTRACTION & AUTOMATION PIPELINES", font=FONT_UI_TITLE, fill=TEXT_CYAN)
    draw.text((120, 140), "Custom Python scripts that eliminate manual data entry in 24 hours.", font=FONT_UI_SUB, fill=TEXT_MUTED)

    # 3 Service Cards
    cards = [
        ("STARTER SCRIPT", "$25", "24 Hours Delivery", [
            "• Single Document Type / Scrape Parser",
            "• Dynamic Recalculating Excel Formulas",
            "• Full Python Source Code Included"
        ], 120),
        ("PIPELINE PRO", "$50", "24-48 Hours Delivery", [
            "• Multi-Document Batch Processing",
            "• Executive Master KPI Register",
            "• Auto Phone Normalization & CRM CSV"
        ], 680),
        ("MONTHLY RETAINER", "$100/mo", "Ongoing Partnership", [
            "• Weekly automated batch runs",
            "• Schema maintenance as formats evolve",
            "• Priority Slack/Email support"
        ], 1240),
    ]

    for title, price, turn, bullets, c_x in cards:
        draw.rounded_rectangle([c_x, 220, c_x + 520, 680], radius=16, fill=CARD_BG, outline=CARD_BORDER, width=2)
        draw.text((c_x + 35, 255), title, font=FONT_UI_BOLD, fill=TEXT_WHITE)
        draw.text((c_x + 35, 305), price, font=FONT_UI_TITLE, fill=TEXT_CYAN)
        draw.text((c_x + 35, 365), f"Turnaround: {turn}", font=FONT_UI_SM, fill=TEXT_GREEN)
        draw.line([c_x + 35, 405, c_x + 485, 405], fill=CARD_BORDER, width=1)

        b_y = 430
        for b in bullets:
            draw.text((c_x + 35, b_y), b, font=FONT_CODE_SM, fill=TEXT_MUTED)
            b_y += 42

    # The 1-File Risk-Free Guarantee Banner
    g_y = 730
    draw.rounded_rectangle([120, g_y, 1800, g_y + 130], radius=14, fill=(30, 41, 59), outline=TEXT_GREEN, width=2)
    draw.text((150, g_y + 25), "🛡️ 100% RISK-FREE PROOF GUARANTEE:", font=FONT_UI_BOLD, fill=TEXT_GREEN)
    draw.text((150, g_y + 70), "Send me 1 sample invoice, PDF, or messy scrape snippet. I will extract it and return the clean Excel sheet for free so you can verify the results before paying.", font=FONT_UI_SUB, fill=TEXT_WHITE)

    # Footer Contact
    f_y = 900
    draw.text((120, f_y), "📬 Direct Inquiries: amanpratapsingh1999@gmail.com", font=FONT_CODE_MD, fill=TEXT_WHITE)
    draw.text((120, f_y + 40), "🐙 GitHub Portfolio: github.com/amanpratap1999/ai-data-toolkit", font=FONT_CODE_MD, fill=TEXT_CYAN)
    draw.text((120, f_y + 80), "💳 Payments: Invoiced securely via PayPal Business upon milestone approval.", font=FONT_CODE_MD, fill=TEXT_MUTED)

    path = OUTPUT_DIR / "scene4_commercial_outro.png"
    img.save(path)
    print(f"✓ Rendered: {path}")


def main():
    print("🎨 Rendering 4 high-resolution 1080p demo scene frames...")
    render_scene_1_messy_input()
    render_scene_2_terminal_run()
    render_scene_3_excel_master()
    render_scene_4_commercial_outro()
    print("✅ All 4 scene frames rendered successfully in temp_frames/")


if __name__ == "__main__":
    main()
