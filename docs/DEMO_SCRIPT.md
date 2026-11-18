# 🎬 90-Second High-Converting Video Demo Script

> **Goal:** Prove technical competence in under 90 seconds, eliminate client hesitation, and drive inbound messages for $25–$50 freelance gigs.
> **Tools Recommended:** Free Loom (browser extension or desktop app) or OBS Studio.
> **Screen Layout:** Left half terminal / VS Code, right half Excel or full screen switching smoothly.

---

## ⏱️ Second-by-Second Breakdown

```
[0:00 - 0:15] ─── Scene 1: The Hook (Show the Messy Problem)
[0:15 - 0:35] ─── Scene 2: The Magic (Run the 1-Line Command)
[0:35 - 1:05] ─── Scene 3: The Proof (Walkthrough Live Formula Excel)
[1:05 - 1:30] ─── Scene 4: The Offer (24h Turnaround + Free 1-Sample Test)
```

---

### 🔴 Scene 1: The Hook (0:00 – 0:15)
**On Screen:** Have `samples/raw_invoice_1.txt` or `samples/raw_business_leads_3.txt` open in a text editor or VS Code. Scroll slightly to show the unaligned columns, messy discount lines, and lack of structure.

**Spoken Transcript (Confident, direct, builder voice):**
> *"If you or your team are still copying and pasting messy PDF invoices or web scrapes into Excel row by row, you're losing hours every week. Here's a real-world messy logistics invoice: scattered freight charges, unformatted dates, and disconnected discount lines. Here is how we turn this into an executive, formula-backed spreadsheet in five seconds."*

---

### 🟡 Scene 2: The Magic (0:15 – 0:35)
**On Screen:** Switch to PowerShell or Terminal. Show the clean 1-line command already typed:
```bash
python extract_invoice.py samples/ --batch
```
*(Or use `python demo_launcher.py` to run it automatically).*
Press Enter. Let the screen capture the fast streaming logs:
```
📂 Scanning directory for invoices: samples/
  [1/3] Parsing: raw_invoice_1.txt... ✓ INV-2026-8819B ($5,130.14)
  [2/3] Parsing: raw_invoice_2.txt... ✓ INV-CYBER-2026-904 ($13,725.00)
  [3/3] Parsing: raw_receipt_2.txt... ✓ REC-2026-11-0492 ($24.75)
📊 Generating Master Executive Register: Master_Invoice_Register.xlsx...
```

**Spoken Transcript:**
> *"I built a lightweight Python extraction engine that streams unstructured text through cloud AI inference. Notice how fast it processes: in under five seconds, it batch-parsed three different document formats, calculated the financial breakdowns, and compiled an executive Master Register without consuming heavy local memory."*

---

### 🟢 Scene 3: The Proof of Quality (0:35 – 1:05)
**On Screen:** Open the generated `output/Master_Invoice_Register.xlsx` (or `output/invoice_INV-2026-8819B.xlsx`).
- Hover your mouse over the **KPI Metric Cards** at the top (`Total Invoices`, `Cumulative Spend Balance: $18,879.89`).
- Click on cell `E13` (Quantity $\times$ Unit Price) and point out the formula bar: `=C13*D13`.
- Click on cell `E18` (Subtotal): `=SUM(E13:E15)`.
- Change a quantity or price live on screen to show the total instantly recalculating!

**Spoken Transcript:**
> *"Now look at the actual output. Most automated scripts dump raw, static numbers into Excel. We write **native live formulas**: quantity times unit price, dynamic sum subtotals, and balance calculations. If an accountant modifies a line item, the entire balance updates automatically. We also have executive styling, auto-fitted widths, freeze panes, and dedicated breakdown tabs for every invoice."*

---

### 🔵 Scene 4: The Commercial Offer & Risk Reversal (1:05 – 1:30)
**On Screen:** Show your GitHub repository or commercial contact info ([README.md Commercial Services](https://github.com/amanpratap1999/ai-data-toolkit#readme)).

**Spoken Transcript:**
> *"I build custom data extraction pipelines and scraping cleaners like this for businesses with a guaranteed **24-hour turnaround**. Fixed-price gigs start at just **$25 to $50**.*
> 
> *Best of all, you take zero risk: send me **one sample document or scrape file**, and I'll extract it and send back the clean Excel sheet for free so you can verify the results before paying.*
> 
> *Check the link in the description or DM me directly, and let's automate your messy data today."*

---

## 💡 Pro Tips for a 10/10 Video Recording

1. **Keep Energy High & Conversational:** Speak like an engineer solving a real headache, not a salesman reading a pitch.
2. **Zoom In (125%–150%):** Viewers often watch on laptops or mobile phones. Make sure terminal font and Excel numbers are crisp and readable.
3. **Keep Loom Webcam Small or Off:** If using Loom, a small circular camera bubble in the lower-left corner adds personal trust. If you prefer not to be on camera, screen + clear audio works equally well.
4. **Target Duration:** Aim for **75 to 95 seconds**. Shorter is always better than longer.
