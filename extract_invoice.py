#!/usr/bin/env python3
"""
Production-Grade Invoice & Financial Document Extractor
Features:
- Supports .txt and native .pdf files
- Single-document extraction with live dynamic Excel formulas
- Batch extraction (--batch) generating an Executive Master Register with KPIs
"""

import sys
import argparse
from pathlib import Path
from typing import List, Optional
from pydantic import ValidationError

from core.client import CloudAIClient
from core.schema import InvoiceData
from core.exporter import export_invoice_to_excel, export_batch_summary_to_excel


def read_document_text(file_path: Path) -> str:
    """Reads raw text from either .txt or native .pdf files."""
    if not file_path.exists():
        raise FileNotFoundError(f"Input file not found: {file_path}")

    suffix = file_path.suffix.lower()

    if suffix == ".pdf":
        try:
            import pypdf
            reader = pypdf.PdfReader(str(file_path))
            pages_text = [page.extract_text() or "" for page in reader.pages]
            full_text = "\n".join(pages_text).strip()
            if not full_text:
                raise ValueError("PDF contains no extractable text (may be scanned image).")
            return full_text
        except Exception as e:
            raise RuntimeError(f"Failed to read PDF file {file_path.name}: {e}")

    # Default to text
    return file_path.read_text(encoding="utf-8").strip()


def extract_single_invoice(file_path: Path, client: Optional[CloudAIClient] = None) -> InvoiceData:
    """Extracts structured InvoiceData from a single file using Cloud AI."""
    raw_content = read_document_text(file_path)
    if not raw_content:
        raise ValueError(f"File {file_path.name} is empty!")

    if client is None:
        client = CloudAIClient()

    sample_target = '''{
  "invoice_number": "INV-12345",
  "issue_date": "YYYY-MM-DD",
  "due_date": "YYYY-MM-DD",
  "payment_terms": "Net 30",
  "vendor_name": "Company Name",
  "vendor_address": "Street, City, State ZIP",
  "vendor_email": "billing@company.com",
  "customer_name": "Client Name",
  "customer_address": "Street, City, State ZIP",
  "customer_email": "client@email.com",
  "line_items": [
    {
      "description": "Item description",
      "quantity": 1.0,
      "unit_price": 100.0,
      "total_price": 100.0
    }
  ],
  "subtotal": 100.0,
  "discounts": 0.0,
  "tax_amount": 0.0,
  "total_amount": 100.0,
  "currency": "USD"
}'''

    system_prompt = (
        "You are an expert financial document extractor. "
        "Extract invoice metadata and itemized line items from the document into valid JSON. "
        "Output ONLY the JSON object matching this exact structure, with no markdown explanation:\n"
        f"{sample_target}"
    )

    user_prompt = (
        f"Extract all invoice details and itemized rows from this document into JSON:\n\n"
        f"{raw_content}\n\n"
        "Return ONLY the raw JSON object."
    )

    raw_json = client.complete(
        prompt=user_prompt,
        system_prompt=system_prompt,
        as_json=True
    )

    try:
        return InvoiceData.model_validate(raw_json)
    except ValidationError as e:
        print(f"⚠️ Validation warning on {file_path.name}: {e}")
        raise


def run_single(file_path: Path, output_path: Optional[Path] = None):
    print(f"\n📂 Reading input file: {file_path.name}")
    client = CloudAIClient()
    print("🤖 Extracting structured data via Cloud AI...")
    invoice = extract_single_invoice(file_path, client)

    if not output_path:
        safe_num = "".join(c for c in invoice.invoice_number if c.isalnum() or c in ("-", "_")) or "doc"
        output_path = Path("output") / f"invoice_{safe_num}.xlsx"

    print(f"📊 Generating styled Excel with live formulas: {output_path.name}...")
    saved_path = export_invoice_to_excel(invoice, output_path)

    # Print Summary Card
    print("\n" + "=" * 62)
    print("✅ EXTRACTION SUCCESSFUL (10/10 STANDARD)")
    print("=" * 62)
    print(f"• Invoice #:     {invoice.invoice_number}")
    print(f"• Vendor:        {invoice.vendor_name}")
    print(f"• Customer:      {invoice.customer_name}")
    print(f"• Issue Date:    {invoice.issue_date or 'N/A'} (Due: {invoice.due_date or 'N/A'})")
    print(f"• Line Items:    {len(invoice.line_items)} item(s) parsed with dynamic Excel formulas")
    for idx, item in enumerate(invoice.line_items, start=1):
        print(f"    [{idx}] {item.description:<40} x{item.quantity:<4} ${item.total_price:,.2f}")
    print(f"• Subtotal:      ${(invoice.subtotal or 0.0):,.2f}")
    if invoice.discounts:
        print(f"• Discounts:    -${abs(invoice.discounts):,.2f}")
    if invoice.tax_amount:
        print(f"• Tax/Charges:   ${invoice.tax_amount:,.2f}")
    print(f"• FINAL TOTAL:   ${invoice.total_amount:,.2f} {invoice.currency}")
    print("-" * 62)
    print(f"📁 Excel file:   {saved_path.resolve()}")
    print("=" * 62 + "\n")


def run_batch(directory_or_pattern: Path, output_path: Optional[Path] = None):
    """Processes multiple invoices and outputs a single unified master workbook."""
    if directory_or_pattern.is_dir():
        files = sorted(list(directory_or_pattern.glob("*invoice*.txt")) + list(directory_or_pattern.glob("*.pdf")))
    else:
        files = [directory_or_pattern]

    if not files:
        print(f"❌ No invoice files found in {directory_or_pattern}")
        sys.exit(1)

    print(f"\n📂 Batch Mode: Found {len(files)} invoice document(s) to process.")
    client = CloudAIClient()
    parsed_invoices: List[InvoiceData] = []

    for idx, f in enumerate(files, start=1):
        print(f"  [{idx}/{len(files)}] Processing {f.name}...")
        try:
            inv = extract_single_invoice(f, client)
            parsed_invoices.append(inv)
            print(f"      ✓ Extracted #{inv.invoice_number} | {inv.vendor_name} | ${inv.total_amount:,.2f}")
        except Exception as e:
            print(f"      ✗ Failed to parse {f.name}: {e}")

    if not parsed_invoices:
        print("❌ No invoices were successfully parsed.")
        sys.exit(1)

    if not output_path:
        output_path = Path("output") / "Master_Invoice_Register.xlsx"

    print(f"\n📊 Compiling Executive Master Register with KPIs: {output_path.name}...")
    saved_path = export_batch_summary_to_excel(parsed_invoices, output_path)

    total_spend = sum(inv.total_amount for inv in parsed_invoices)
    print("\n" + "=" * 62)
    print("🏆 BATCH REGISTER GENERATED")
    print("=" * 62)
    print(f"• Total Invoices:      {len(parsed_invoices)}")
    print(f"• Cumulative Spend:    ${total_spend:,.2f} USD")
    print(f"• Individual Sheets:   {len(parsed_invoices)} dedicated breakdown tabs")
    print(f"📁 Master File:        {saved_path.resolve()}")
    print("=" * 62 + "\n")


def main():
    parser = argparse.ArgumentParser(
        description="Production-Grade Invoice Extractor (Cloud AI + OpenPyXL Formulas + Batch Mode)"
    )
    parser.add_argument(
        "target",
        type=Path,
        help="Path to an invoice file (.txt, .pdf) or a folder for batch mode",
    )
    parser.add_argument(
        "--output",
        "-o",
        type=Path,
        default=None,
        help="Custom output .xlsx file path",
    )
    parser.add_argument(
        "--batch",
        action="store_true",
        help="Process all documents in target folder into a Master Register workbook",
    )

    args = parser.parse_args()

    if args.batch or args.target.is_dir():
        run_batch(args.target, args.output)
    else:
        run_single(args.target, args.output)


if __name__ == "__main__":
    main()
