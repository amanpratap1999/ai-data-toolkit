#!/usr/bin/env python3
"""
Human-Like Automated Screen Walkthrough for Recordly.dev.
Simulates a human developer performing the live demo with:
- Natural smooth mouse curves (easing acceleration/deceleration)
- Humanized keystroke typing cadence (varying delays between keys)
- Strategic pauses & clicks to trigger Recordly's cinematic auto-zooms
- Automatic opening of messy input file, terminal command run, and Excel formula inspection
"""

import os
import sys
import time
import random
import subprocess
from pathlib import Path

try:
    import pyautogui
except ImportError:
    print("❌ pyautogui is not installed. Run: pip install pyautogui")
    sys.exit(1)

# Configure PyAutoGUI safety
pyautogui.FAILSAFE = True
pyautogui.PAUSE = 0.05

SCREEN_W, SCREEN_H = pyautogui.size()


def human_move(x, y, duration=1.2):
    """Moves mouse with human-like acceleration and deceleration curve."""
    pyautogui.moveTo(x, y, duration=duration, tween=pyautogui.easeInOutQuad)


def human_type(text: str, base_delay=0.07):
    """Types text with natural human micro-delays between keystrokes."""
    for char in text:
        pyautogui.write(char)
        delay = random.uniform(0.035, 0.09) if char != " " else random.uniform(0.12, 0.20)
        time.sleep(delay)


def run_countdown(seconds=5):
    print("\n" + "=" * 65)
    print("🎬 RECORDLY HUMAN-LIKE DEMO AUTOMATION")
    print("=" * 65)
    print(f"👉 PREPARATION: Open Recordly and get ready to click START RECORDING.")
    print("=" * 65)
    for i in range(seconds, 0, -1):
        print(f"⏱️ Starting in {i}... (Hit Record in Recordly now!)")
        time.sleep(1.0)
    print("🚀 AUTOMATION RUNNING! Hands off keyboard & mouse...\n")
    time.sleep(0.5)


def scene_1_show_messy_input():
    print("📍 [Scene 1] Showing messy invoice input...")
    sample_file = Path("samples") / "raw_invoice_1.txt"
    if not sample_file.exists():
        print("⚠️ Sample file missing, skipping scene 1.")
        return

    # Open in Notepad
    proc = subprocess.Popen(["notepad.exe", str(sample_file.resolve())])
    time.sleep(1.5)

    # Human smoothly moves cursor across the messy text
    human_move(SCREEN_W // 2, SCREEN_H // 3, duration=1.0)
    time.sleep(0.8)
    # Glide cursor over line items
    human_move(SCREEN_W // 2 - 100, SCREEN_H // 2, duration=1.2)
    time.sleep(0.8)
    human_move(SCREEN_W // 2 + 80, SCREEN_H // 2 + 60, duration=1.0)
    time.sleep(2.0)

    # Close notepad cleanly (Alt + F4)
    pyautogui.hotkey("alt", "f4")
    time.sleep(1.0)


def scene_2_type_command_and_run():
    print("📍 [Scene 2] Typing and running extraction command in terminal...")
    # Center mouse in terminal window
    human_move(SCREEN_W // 2, SCREEN_H // 2 + 100, duration=0.8)
    pyautogui.click()
    time.sleep(0.5)

    # Human types command
    command = "python extract_invoice.py samples/ --batch"
    human_type(command)
    time.sleep(0.6)

    # Hit Enter
    pyautogui.press("enter")
    print("  ⏳ Waiting for batch extraction pipeline to finish...")
    time.sleep(6.5)


def scene_3_inspect_excel_deliverable():
    print("📍 [Scene 3] Opening Excel and inspecting live dynamic formulas...")
    excel_file = Path("output") / "Master_Invoice_Register.xlsx"
    if not excel_file.exists():
        print("⚠️ Excel file missing, cannot show.")
        return

    # Launch Excel
    if sys.platform == "win32":
        os.startfile(str(excel_file.resolve()))
    else:
        subprocess.run(["xdg-open", str(excel_file.resolve())])

    time.sleep(3.5)  # Wait for Excel window to open

    # Maximize active window (Win + Up Arrow)
    pyautogui.hotkey("win", "up")
    time.sleep(1.0)

    # Move to KPI Card at top ($18,879.89 Cumulative Spend)
    print("  🔍 Hovering over Executive KPI Summary Cards...")
    kpi_x = int(SCREEN_W * 0.28)
    kpi_y = int(SCREEN_H * 0.26)
    human_move(kpi_x, kpi_y, duration=1.2)
    time.sleep(2.0)

    # Move down to Table Line Item (cell E13 - $4,300.00)
    print("  🔍 Clicking Cell E13 to show formula =C13*D13...")
    cell_e13_x = int(SCREEN_W * 0.35)
    cell_e13_y = int(SCREEN_H * 0.44)
    human_move(cell_e13_x, cell_e13_y, duration=1.1)
    pyautogui.click()  # Click triggers Recordly's auto-zoom on the formula!
    time.sleep(2.5)

    # Move down to Subtotal (cell E18 - $4,905.00)
    print("  🔍 Clicking Cell E18 to show formula =SUM(E13:E15)...")
    cell_e18_x = int(SCREEN_W * 0.35)
    cell_e18_y = int(SCREEN_H * 0.54)
    human_move(cell_e18_x, cell_e18_y, duration=1.0)
    pyautogui.click()
    time.sleep(2.5)

    # Smoothly move to bottom sheet tabs (individual invoices)
    print("  🔍 Hovering over dedicated sheet tabs...")
    tab_x = int(SCREEN_W * 0.15)
    tab_y = int(SCREEN_H * 0.94)
    human_move(tab_x, tab_y, duration=1.2)
    time.sleep(2.0)


def main():
    run_countdown(seconds=5)
    scene_1_show_messy_input()
    scene_2_type_command_and_run()
    scene_3_inspect_excel_deliverable()

    print("\n" + "=" * 65)
    print("✅ DEMO WALKTHROUGH COMPLETE!")
    print("👉 Click 'Stop Recording' in Recordly now to generate your video.")
    print("=" * 65)


if __name__ == "__main__":
    main()
