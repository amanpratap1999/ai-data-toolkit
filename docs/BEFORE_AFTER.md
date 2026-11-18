# 📊 Visual Before & After Showcase

This document illustrates how the **AI Data Extraction & Cleaning Toolkit** converts messy, unformatted, and fragmented real-world business data into structured, formula-backed, executive deliverables.

---

## ⚡ Showcase 1: Unstructured B2B Invoice to Dynamic Formula Excel

### 🔴 The Problem: Raw, Inconsistent Invoice Text
Business invoices arrive in irregular layouts with non-standard line formatting, unformatted numbers, and disconnected discount notes:

```text
======================================================================
                  GLOBAL PACIFIC LOGISTICS & FREIGHT
                      1044 Harbor View Blvd, Ste 400
                            Long Beach, CA 90802
----------------------------------------------------------------------
INVOICE NUMBER: INV-2026-8819B
ISSUED: 14-Nov-2026                     DUE: 14-Dec-2026
CURRENCY: USD

BILLED TO:
Apex Commercial Retailers Inc.
Attn: Accounts Payable
742 Industrial Pkwy, Bldg C
Dallas, TX 75201
VAT / TAX ID: US-TX-9948201

LINE ITEMS:
1. Ocean Freight Container 40ft (Shanghai -> LA)
   Qty: 2 | Unit Price: 2,150.00 | Total: 4,300.00
2. Customs Clearance & Harbor Drayage Fee
   Qty: 1 | Unit Price: 420.00   | Total: 420.00
3. Chassis Inspection & Terminal Handling (LFD Dec 2)
   Qty: 1 | Unit Price: 185.00   | Total: 185.00

FINANCIAL SUMMARY:
Subtotal: $4,905.00
Fuel Surcharge (4.5%): $220.73
California State Logistics Tax (1.5%): $73.58
Discount Applied: -$69.17 (Early booking credit)
----------------------------------------------------------------------
TOTAL BALANCE DUE: $5,130.14
Payment Terms: Net 30 days. Wire transfer or ACH accepted.
======================================================================
```

---

### 🟢 The Solution: Clean Executive Workbook with Live Excel Formulas

Unlike naive scripts that hardcode static text into spreadsheets, our extraction engine writes **live Excel formulas**. When an accountant modifies a line item quantity, the entire sheet recalculates automatically.

#### 1. Formatted Spreadsheet View
| Line # | Description | Quantity | Unit Price | Total Amount | Status / Notes |
|:---:|:---|:---:|:---:|:---:|:---|
| **1** | Ocean Freight Container 40ft (Shanghai -> LA) | 2 | \$2,150.00 | **\$4,300.00** | Standard 40ft |
| **2** | Customs Clearance & Harbor Drayage Fee | 1 | \$420.00 | **\$420.00** | Port processing |
| **3** | Chassis Inspection & Terminal Handling | 1 | \$185.00 | **\$185.00** | LFD Dec 2 |
| | | | **Subtotal:** | **\$4,905.00** | *(Formula-driven)* |
| | | | **Tax & Surcharge:** | **\$294.31** | *(Formula-driven)* |
| | | | **Discount:** | **-\$69.17** | *(Applied)* |
| | | | **TOTAL DUE:** | **\$5,130.14** | `PAYMENT DUE` *(Navy Header)* |

#### 2. Underlying Excel Formula Architecture
- **Row Total Formula:** `=C13*D13` (Quantity $\times$ Unit Price)
- **Subtotal Formula:** `=SUM(E13:E15)`
- **Net Balance Due Formula:** `=E18+E19+E20`

#### 3. Multi-Invoice Executive Register (`--batch`)
When scanning a batch of documents, the engine builds a **Master Register** with executive KPI metric cards:
- **Total Invoices Processed:** 3
- **Cumulative Spend Balance:** \$18,879.89
- **Average Spend per Invoice:** \$6,293.30
- **Dedicated Sheet Tabs:** One tab for each individual invoice for detailed line audits.

---

## ⚡ Showcase 2: Dirty Web Scrapes to Verified B2B Lead Directory

### 🔴 The Problem: Fragmented, Incomplete Web Scrape Dumps
Scraped web listings frequently have mangled phone formatting, multiple emails bundled together, missing websites, and zero data quality visibility:

```text
[ITEM_1]
Clinic: Peak Performance Physio Clinic
Specialties: Sports rehab, dry needling, post-op mobility
Primary: Dr. Marcus Vance, PT, DPT (Clinical Director)
Address: 1420 Walnut St, Suite 310, Philadelphia, Pennsylvania 19102
Contact: frontdesk@peakphysiophilly.com; marcus@peakphysiophilly.com
Telephone: (215) 555-7821 / alt: (215) 555-7822
Website: 
Hours: Mon-Fri 7am - 7pm. Accepts BlueCross, Aetna, Medicare.
```

---

### 🟢 The Solution: Clean Directory with Hyperlinks, Enriched Domains & Freeze Panes

Our cleaner normalizes phone strings, splits emails, infers missing website URLs from corporate email domains, and scores the lead for sales team efficiency.

#### 1. Extracted & Enriched Record
- **Company:** Peak Performance Physio Clinic
- **Contact & Title:** Dr. Marcus Vance, PT, DPT (Clinical Director)
- **Sanitized Phone:** `+1 (215) 555-7821` *(E.164 compliant)*
- **Primary Email:** `frontdesk@peakphysiophilly.com` *(Clickable `mailto:` link)*
- **Enriched Website:** `https://www.peakphysiophilly.com` *(Automatically derived from email domain)*
- **Location:** Philadelphia, PA
- **Completeness Score:** `100%`
- **Quality Tier:** `HIGH QUALITY` *(Styled in soft green pill badge)*

#### 2. Production Enterprise Features
- **Freeze Panes (`A8`):** Executive KPI cards and table column headers remain visible while scrolling through thousands of leads.
- **AutoFilter (`A7:J10`):** Instant Excel filtering by Quality Tier, Location, or Specialty.
- **Dual Export:** Generates both an Excel Workbook (`.xlsx`) and a UTF-8 BOM CSV ready for direct upload into HubSpot, Apollo, or Salesforce.

---

## ⚡ Showcase 3: Automated Multi-Key Deduplication

Scraped datasets often contain repeated listings from multi-page crawls. The toolkit includes an intelligent multi-key deduplicator:

```python
# Automatic duplicate detection across:
# 1. Normalized Company Name (case-insensitive alphanumeric)
# 2. Primary Email Address
# 3. Normalized Phone Digits (E.164)
```

If duplicate listings are detected, the cleaner **merges the records and keeps the one with the highest completeness score**, ensuring your CRM import contains zero redundant entries.
