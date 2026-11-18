# ⚡ AI Data Extraction & Cleaning Toolkit
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)
[![RAM Footprint](https://img.shields.io/badge/RAM%20Footprint-%3C50MB-success.svg)](https://github.com)
[![Excel Output](https://img.shields.io/badge/Spreadsheets-Live%20Formulas-brightgreen.svg)](https://github.com)
[![CRM Ready](https://img.shields.io/badge/CRM%20Export-HubSpot%20%7C%20Apollo%20%7C%20Salesforce-orange.svg)](https://github.com)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

> **Enterprise-grade, cloud-accelerated parsing engine that transforms unstructured business documents (PDFs, invoices, receipts, messy text, dirty directory scrapes) into publication-grade Excel workbooks and CRM-ready CSVs.**

Built with an ultra-lightweight architecture optimized for standard workstations (8GB RAM laptops) with **0 local VRAM / heavy GPU dependencies**.

---

## 💼 Why Business Clients Use This Service

Manual data entry and dirty web scrapes cost operations teams dozens of wasted hours every week. This toolkit delivers automated, high-precision structured data pipelines:

- **⚡ 24-Hour Turnaround:** Custom extraction scripts tailored to your specific file formats.
- **📊 Live Excel Formulas:** We write native formulas (`=C13*D13`, `=SUM(...)`, `=E18+E19+E20`) — not static numbers. If you adjust a rate, your spreadsheet recalculates automatically.
- **🎯 B2B Data Enrichment:** Automatic phone number formatting (+1 E.164), email cleaning, and corporate website domain derivation.
- **🛡️ Enterprise Reliability:** Automatic exponential backoff handles API queuing with zero data loss.
- **💰 Budget Friendly:** Runs on lightweight cloud inference (NVIDIA NIM / OpenAI-compatible); no expensive dedicated servers required.

---

## 🌟 Core Modules

### 1. Invoice & Financial Extractor (`extract_invoice.py`)
Turn raw PDF and text invoices into structured executive financial sheets.
- **Live Dynamic Excel Formulas:** Generates line-item multiplications, subtotals, and net balances.
- **Status Pills & Styling:** Visual indicators (`PAYMENT DUE`, `PENDING REVIEW`) with navy executive styling and zebra striping.
- **Master Batch Register Mode (`--batch`):** Processes an entire folder of invoices into a consolidated register with KPI metric cards (`Total Spend`, `Average Invoice Value`) plus dedicated sheet tabs per invoice.
- **Native PDF Ingestion:** Reads text directly from `.pdf` and `.txt` files.

### 2. Scraped Directory & Lead Cleaner (`clean_scraped_data.py`)
Transform messy web scraped dumps into clean, verified sales directories.
- **Smart Auto-Chunking:** Automatically recognizes listing boundaries (`---`, headers, line blocks) to eliminate timeouts on bulk dumps.
- **Multi-Format Ingestion:** Ingests raw `.txt`, `.csv`, and `.json` scrape dumps seamlessly.
- **Automated Multi-Key Deduplication:** Merges overlapping listings across Company Name, Primary Email, and Phone digits, keeping the highest quality record.
- **Completeness & Quality Scoring:** Computes a 0–100% CRM health score and tags records as `HIGH QUALITY`, `MEDIUM`, or `INCOMPLETE`.
- **Freeze Panes & AutoFilter:** Pins executive KPI cards and table headers (`A8`) and enables instant column filtering (`A7:J10`).
- **Dual Export:** Outputs both an executive Excel workbook (`.xlsx`) with clickable `mailto:` / web hyperlinks and a UTF-8 BOM CSV ready for HubSpot, Apollo, or Salesforce.

---

## 📸 Visual Before & After Showcase

| Raw Unstructured Input | Clean Structured Deliverable |
|:---|:---|
| **Messy Freight & POS Invoices**<br>Scattered text, unaligned prices, inconsistent tax lines. | **Executive Excel Workbook**<br>Live formulas (`=SUM(...)`), navy headers, line item breakdowns, and master KPI register. |
| **Dirty Directory Scrapes**<br>Mangled phone numbers, bundled emails, missing company websites. | **Enriched Lead Directory**<br>Normalized `+1 (XXX) XXX-XXXX` phones, clickable links, auto-inferred websites, freeze panes, and AutoFilters. |

👉 **[Read the Full Before & After Report with Formula Breakdowns →](docs/BEFORE_AFTER.md)**

---

## 📁 Repository Structure

```
ai-data-toolkit/
├── core/
│   ├── client.py               # Cloud inference client with exponential backoff retry
│   ├── schema.py               # Pydantic invoice models & financial line item validation
│   ├── exporter.py             # OpenPyXL engine with live dynamic formulas & batch KPI register
│   ├── lead_schema.py          # Pydantic lead models with auto phone & domain enrichment
│   └── lead_exporter.py        # Excel lead directory with AutoFilter, freeze panes & CRM CSV
├── samples/
│   ├── raw_invoice_1.txt       # B2B Freight logistics invoice ($5,130.14)
│   ├── raw_invoice_2.txt       # Tech cybersecurity invoice ($13,725.00)
│   ├── raw_receipt_2.txt       # Restaurant POS receipt
│   └── raw_business_leads_3.txt # Dirty directory scrape with 3 business listings
├── portfolio_showcase/         # Ready-to-inspect pre-generated deliverable files
│   ├── invoice_INV-2026-8819B.xlsx
│   ├── Master_Invoice_Register.xlsx
│   ├── clean_leads_raw_business_leads_3.xlsx
│   └── clean_leads_raw_business_leads_3.csv
├── docs/
│   └── BEFORE_AFTER.md         # Detailed visual transformation guide
├── requirements.txt            # Minimal dependencies (<50MB RAM footprint)
├── .env.example                # Configuration template
├── extract_invoice.py          # Invoice extraction CLI
└── clean_scraped_data.py       # Scraped data & lead cleaning CLI
```

---

## 🚀 60-Second Quickstart

### 1. Clone & Install Dependencies
```bash
git clone https://github.com/yourusername/ai-data-toolkit.git
cd ai-data-toolkit
pip install -r requirements.txt
```
*Memory footprint is under 50MB RAM — no PyTorch, no CUDA, no local models.*

### 2. Set Up API Credentials
Copy `.env.example` to `.env` and add your free NVIDIA NIM API key:
```bash
cp .env.example .env
```
Edit `.env`:
```ini
NVIDIA_API_KEY=nvapi-your-key-here
NVIDIA_BASE_URL=https://integrate.api.nvidia.com/v1
MODEL_NAME=minimaxai/minimax-m3.1-flash
```

### 3. Run the Demos

**Extract a Single Invoice into Formula-Backed Excel:**
```bash
python extract_invoice.py samples/raw_invoice_1.txt
```

**Process a Batch of Invoices into a Master KPI Register:**
```bash
python extract_invoice.py samples/ --batch
```

**Clean & Enrich Dirty Web Scrapes into Excel & CRM CSV:**
```bash
python clean_scraped_data.py samples/raw_business_leads_3.txt
```

All generated files are saved into the `output/` directory immediately.

---

## 🛠️ Architecture & 8GB RAM Guarantee

Most modern AI solutions require heavy local models (Ollama, PyTorch) that consume 6GB–16GB of system memory, causing standard laptops to lag or crash.

This toolkit follows a **hybrid cloud-stream architecture**:
1. **Lightweight Streaming Ingestion:** Files are parsed as plain text streams using standard Python and `pypdf` (<30MB RAM).
2. **Cloud AI Normalization:** Data extraction and structuring are performed via high-speed cloud inference (`minimaxai/minimax-m3.1-flash` via NVIDIA NIM).
3. **Resilient Network Layer:** Exponential backoff retries transient 429 / queue bottlenecks automatically.
4. **Deterministic Post-Processing:** Phone formatting, website domain derivation, and deduplication run via zero-overhead regex and Pydantic validators.
5. **Direct Spreadsheet Synthesis:** Workbooks are compiled directly in memory via `openpyxl` with native formula injection.

**Total local RAM during execution: ~42MB.**

---

## 🤝 Commercial Inquiries & Custom Automation

Need custom extraction or scraping automation for your business?

- **Custom Document Parsers:** Invoices, purchase orders, medical bills, utility statements.
- **Scraper Normalization:** Web directories, Google Maps scrapes, real estate listings.
- **Automated CRM Sync:** Direct export to HubSpot, Apollo, Airtable, or PostgreSQL.
- **Fixed-Price Delivery:** Small batch scripts start at **$25 – $50** with a **24-hour turnaround**.
- **Payment & Guarantee:** Invoiced securely via **PayPal**. Free 1-sample test verification before you pay.

📬 **Get in touch:**
- **Email:** amanpratapsingh1999@gmail.com
- **Upwork / Freelance:** Available upon request
- **PayPal:** Ready for instant business invoicing
