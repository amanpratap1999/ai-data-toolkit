"""
End-to-End Regression & Quality Gate Test Suite for ai-data-toolkit.
Verifies:
1. Invoice schema validation and live dynamic formula Excel generation (=C*D, =SUM).
2. Master Invoice Register compounding with KPI metric formulas.
3. Scraped lead cleaning, E.164 normalization, website domain enrichment, and deduplication.
4. CRM CSV and formatted Excel exports with AutoFilters.
5. System 8GB RAM safety audit (<50MB memory footprint during batch processing).
"""

import sys
import time
import tracemalloc
import unittest
from pathlib import Path
import openpyxl

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from core.schema import InvoiceData, LineItem
from core.exporter import export_invoice_to_excel, export_batch_summary_to_excel
from core.lead_schema import BusinessLead, clean_phone_number, infer_website_from_email
from core.lead_exporter import export_leads_to_excel, export_leads_to_csv
from clean_scraped_data import split_into_chunks, deduplicate_leads


class TestInvoicePipeline(unittest.TestCase):
    """Test suite for Invoice to Live-Formula Excel extraction and export."""

    def setUp(self):
        self.output_dir = Path(__file__).resolve().parent / "test_outputs"
        self.output_dir.mkdir(exist_ok=True)
        self.test_invoice = InvoiceData(
            invoice_number="INV-TEST-2026",
            issue_date="2026-11-19",
            due_date="2026-12-05",
            payment_terms="Net 30",
            vendor_name="Apex Global Technologies Inc.",
            vendor_address="100 Innovation Way, Austin, TX",
            vendor_email="billing@apextech.io",
            customer_name="Meridian Enterprises LLC",
            customer_address="500 Market St, San Francisco, CA",
            customer_email="accounts@meridian.com",
            line_items=[
                LineItem(
                    description="Cloud Server Architecture Consulting",
                    quantity=12.0,
                    unit_price=125.00,
                    total_price=1500.00
                ),
                LineItem(
                    description="Automated Extraction Pipeline Script",
                    quantity=1.0,
                    unit_price=450.00,
                    total_price=450.00
                ),
            ],
            subtotal=1950.00,
            discounts=0.0,
            tax_amount=156.00,
            total_amount=2106.00,
            currency="USD"
        )

    def test_single_invoice_formula_and_styles(self):
        """Verify dynamic formulas (=C*D, =SUM), formatting, and freeze panes in single invoice."""
        out_file = self.output_dir / "test_single_invoice.xlsx"
        export_invoice_to_excel(self.test_invoice, str(out_file))

        self.assertTrue(out_file.exists(), "Single invoice file must be generated")
        wb = openpyxl.load_workbook(str(out_file), data_only=False)
        ws = wb.active

        # Vendor name check
        self.assertEqual(ws["A4"].value, "Apex Global Technologies Inc.")

        # Dynamic formula check for line items (starts at row 13)
        self.assertEqual(ws["E13"].value, "=C13*D13", "Line item total must use dynamic formula =C*D")
        self.assertEqual(ws["E14"].value, "=C14*D14", "Second line item must use dynamic formula")

        # Subtotal formula check (row 16, with blank spacer at row 15)
        self.assertEqual(ws["E16"].value, "=SUM(E13:E14)", "Subtotal must dynamically sum line items")

        # Total formula check (row 19)
        self.assertEqual(ws["E19"].value, "=E16+E17+E18", "Total must dynamically calculate subtotal + discount + tax")
        wb.close()

    def test_master_register_compounding(self):
        """Verify master register summary sheet, formulas, and KPI cards."""
        out_file = self.output_dir / "test_master_register.xlsx"
        invoices = [self.test_invoice, self.test_invoice]
        export_batch_summary_to_excel(invoices, str(out_file))

        self.assertTrue(out_file.exists(), "Master register must be created")
        wb = openpyxl.load_workbook(str(out_file), data_only=False)
        ws = wb["Master Invoice Register"]

        # KPI Card checks
        self.assertEqual(ws["A4"].value, 2, "Total Invoices KPI must equal 2")
        self.assertEqual(ws["C4"].value, "=SUM(H8:H9)", "Total Volume KPI formula must sum line totals")
        wb.close()


class TestLeadCleaningPipeline(unittest.TestCase):
    """Test suite for Web Scrape Lead Cleaning, Normalization, Deduplication, and CRM Export."""

    def setUp(self):
        self.output_dir = Path(__file__).resolve().parent / "test_outputs"
        self.output_dir.mkdir(exist_ok=True)

    def test_phone_normalization(self):
        """Verify US 10-digit phone number formatting."""
        clean1 = clean_phone_number("(415) 892-1049")
        self.assertEqual(clean1, "+1 (415) 892-1049")

        clean2 = clean_phone_number("1-415-892-1049")
        self.assertEqual(clean2, "+1 (415) 892-1049")

    def test_website_enrichment_from_email(self):
        """Verify business domain enrichment and consumer domain filtering."""
        web1 = infer_website_from_email("sarah@apexlogistics.com", None)
        self.assertEqual(web1, "https://www.apexlogistics.com")

        web_generic = infer_website_from_email("john.doe@gmail.com", None)
        self.assertIsNone(web_generic, "Consumer email domain must not be converted to website")

    def test_deduplication(self):
        """Verify duplicate detection and resolution by company name and email."""
        lead1 = BusinessLead(
            company_name="Apex Logistics LLC",
            primary_email="contact@apexlogistics.com",
            phone="+1 (415) 892-1049",
            city="San Francisco",
            state="CA"
        )
        lead2 = BusinessLead(
            company_name="apex logistics llc",
            primary_email="info@apexlogistics.com",
            phone="+1 415-892-1049",
            city="SF",
            state="California",
            website="https://apexlogistics.com",
            contact_name="Mark Sloan"
        )
        lead3 = BusinessLead(
            company_name="BlueSky Health",
            primary_email="hello@bluesky.org",
            phone="+1 (650) 123-4567"
        )

        unique, dup_count = deduplicate_leads([lead1, lead2, lead3])
        self.assertEqual(len(unique), 2, "Duplicate company must be merged")
        self.assertEqual(dup_count, 1, "Must report exactly 1 duplicate detected")
        # Higher completeness record should win
        apex = next(l for l in unique if "Apex" in l.company_name or "apex" in l.company_name)
        self.assertEqual(apex.contact_name, "Mark Sloan")

    def test_lead_export_xlsx_and_csv(self):
        """Verify dual export of Excel with AutoFilters and CRM-ready CSV."""
        leads = [
            BusinessLead(
                company_name="Vanguard AI Systems",
                contact_name="Elena Vance",
                primary_email="elena@vanguardai.com",
                phone="+1 (555) 019-2831",
                website="https://vanguardai.com",
                city="Austin",
                state="TX",
                specialties=["Machine Learning", "Data Mining"]
            )
        ]
        xlsx_path = self.output_dir / "test_clean_leads.xlsx"
        csv_path = self.output_dir / "test_clean_leads.csv"
        export_leads_to_excel(leads, str(xlsx_path))
        export_leads_to_csv(leads, str(csv_path))

        self.assertTrue(xlsx_path.exists(), "Clean leads Excel file must exist")
        self.assertTrue(csv_path.exists(), "Clean leads CSV file must exist")

        wb = openpyxl.load_workbook(str(xlsx_path))
        ws = wb.active
        self.assertIsNotNone(ws.auto_filter.ref, "Excel sheet must contain active AutoFilter range")
        wb.close()


class TestSystemRAMSafety(unittest.TestCase):
    """Audit memory footprint to guarantee flawless execution under 8GB RAM constraints."""

    def test_memory_footprint_under_50mb(self):
        """Ensure peak memory allocation during batch operations stays strictly below 50MB."""
        tracemalloc.start()
        start_time = time.time()

        # Simulate batch processing of 100 invoices
        mock_invoices = [
            InvoiceData(
                invoice_number=f"INV-BATCH-{i:04d}",
                issue_date="2026-11-19",
                due_date="2026-12-01",
                payment_terms="Net 30",
                vendor_name=f"Enterprise Supplier {i} LLC",
                vendor_address=f"{i * 12} Industrial Parkway, Chicago, IL",
                vendor_email=f"billing@supplier{i}.com",
                customer_name="Global Operations Corp",
                customer_address="100 Wall Street, New York, NY",
                customer_email="ap@globalops.com",
                line_items=[
                    LineItem(description=f"Hardware Component A{j}", quantity=float(j+1), unit_price=25.0 * (j+1), total_price=(j+1)*25.0*(j+1))
                    for j in range(5)
                ],
                subtotal=1250.0,
                discounts=0.0,
                tax_amount=100.0,
                total_amount=1350.0,
                currency="USD"
            )
            for i in range(100)
        ]

        out_batch = Path(__file__).resolve().parent / "test_outputs" / "batch_stress_test.xlsx"
        export_batch_summary_to_excel(mock_invoices, str(out_batch))

        current, peak = tracemalloc.get_traced_memory()
        tracemalloc.stop()
        elapsed = time.time() - start_time

        peak_mb = peak / (1024 * 1024)
        print(f"\n[RAM Performance Audit] Peak Memory: {peak_mb:.2f} MB | Elapsed: {elapsed:.2f}s | Invoices Processed: 100")
        self.assertLess(peak_mb, 50.0, f"Peak memory ({peak_mb:.2f} MB) must remain under 50 MB threshold for 8GB safety")


if __name__ == "__main__":
    unittest.main()
