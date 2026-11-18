"""
Publication-Grade Excel Exporter using openpyxl.
Features:
- Live dynamic Excel formulas (=C*D, =SUM(), arithmetic recalculations)
- Executive status badge pills
- Auto-fit columns with intelligent padding
- Single invoice export and Master Batch Register generation with KPI metrics
"""

from pathlib import Path
from typing import List, Union
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from .schema import InvoiceData

# Design System Colors
COLOR_PRIMARY_NAVY = "1B365D"   # Corporate Deep Navy
COLOR_HEADER_TEXT  = "FFFFFF"
COLOR_ACCENT_ROW   = "F7F9FC"   # Ultra-light slate for zebra rows
COLOR_TOTAL_GREEN  = "E2EFDA"   # Accounting soft green
COLOR_BORDER_LIGHT = "D9D9D9"
COLOR_PILL_BG      = "FFF2CC"   # Soft warm amber for Pending/Due
COLOR_PILL_TEXT    = "7F6000"


def _get_borders():
    thin = Side(style="thin", color=COLOR_BORDER_LIGHT)
    return Border(left=thin, right=thin, top=thin, bottom=thin)


def populate_invoice_sheet(ws, invoice: InvoiceData):
    """Fills a single worksheet with an executive-formatted invoice layout."""
    ws.views.sheetView[0].showGridLines = True

    title_font = Font(name="Calibri", size=15, bold=True, color=COLOR_PRIMARY_NAVY)
    section_font = Font(name="Calibri", size=10, bold=True, color=COLOR_PRIMARY_NAVY)
    bold_font = Font(name="Calibri", size=10, bold=True)
    normal_font = Font(name="Calibri", size=10)
    italic_font = Font(name="Calibri", size=9, italic=True, color="595959")

    header_fill = PatternFill(start_color=COLOR_PRIMARY_NAVY, end_color=COLOR_PRIMARY_NAVY, fill_type="solid")
    header_font = Font(name="Calibri", size=10, bold=True, color=COLOR_HEADER_TEXT)
    accent_fill = PatternFill(start_color=COLOR_ACCENT_ROW, end_color=COLOR_ACCENT_ROW, fill_type="solid")
    total_fill  = PatternFill(start_color=COLOR_TOTAL_GREEN, end_color=COLOR_TOTAL_GREEN, fill_type="solid")
    pill_fill   = PatternFill(start_color=COLOR_PILL_BG, end_color=COLOR_PILL_BG, fill_type="solid")
    pill_font   = Font(name="Calibri", size=9, bold=True, color=COLOR_PILL_TEXT)

    thin_border = _get_borders()
    double_bottom_border = Border(
        top=Side(style="thin", color="000000"),
        bottom=Side(style="double", color="000000"),
        left=Side(style="thin", color=COLOR_BORDER_LIGHT),
        right=Side(style="thin", color=COLOR_BORDER_LIGHT),
    )

    # 1. Header Banner
    ws.merge_cells("A1:D1")
    ws["A1"] = f"INVOICE STATEMENT — #{invoice.invoice_number}"
    ws["A1"].font = title_font
    ws["A1"].alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 28

    # Status Pill in E1
    status_label = "PAYMENT DUE" if "due" in (invoice.payment_terms or "").lower() or not invoice.payment_terms else "PENDING REVIEW"
    ws["E1"] = status_label
    ws["E1"].font = pill_font
    ws["E1"].fill = pill_fill
    ws["E1"].alignment = Alignment(horizontal="center", vertical="center")

    # 2. Parties Info Grid
    ws["A3"] = "ISSUED BY (VENDOR)"
    ws["A3"].font = section_font
    ws["A4"] = invoice.vendor_name
    ws["A4"].font = bold_font
    ws["A5"] = invoice.vendor_address or ""
    ws["A5"].font = normal_font
    ws["A6"] = invoice.vendor_email or ""
    ws["A6"].font = italic_font

    ws["D3"] = "BILLED TO (CUSTOMER)"
    ws["D3"].font = section_font
    ws["D4"] = invoice.customer_name
    ws["D4"].font = bold_font
    ws["D5"] = invoice.customer_address or ""
    ws["D5"].font = normal_font
    ws["D6"] = invoice.customer_email or ""
    ws["D6"].font = italic_font

    # Metadata Row (Dates & Terms)
    ws["A8"] = "Issue Date:"
    ws["A8"].font = bold_font
    ws["B8"] = invoice.issue_date or "N/A"
    ws["B8"].font = normal_font

    ws["D8"] = "Due Date:"
    ws["D8"].font = bold_font
    ws["E8"] = invoice.due_date or "N/A"
    ws["E8"].font = normal_font

    ws["A9"] = "Payment Terms:"
    ws["A9"].font = bold_font
    ws["B9"] = invoice.payment_terms or "Net 30"
    ws["B9"].font = normal_font

    ws["D9"] = "Currency:"
    ws["D9"].font = bold_font
    ws["E9"] = invoice.currency or "USD"
    ws["E9"].font = normal_font

    # 3. Itemized Table
    start_row = 12
    headers = ["#", "Item Description", "Qty / Hours", "Unit Price", "Total Price"]
    for col_idx, h in enumerate(headers, start=1):
        cell = ws.cell(row=start_row, column=col_idx, value=h)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(
            horizontal="center" if col_idx in (1, 3) else ("right" if col_idx in (4, 5) else "left"),
            vertical="center"
        )
    ws.row_dimensions[start_row].height = 22

    item_start_row = start_row + 1
    current_row = item_start_row

    for i, item in enumerate(invoice.line_items, start=1):
        ws.cell(row=current_row, column=1, value=i).alignment = Alignment(horizontal="center")
        ws.cell(row=current_row, column=2, value=item.description).alignment = Alignment(horizontal="left")

        # Qty
        qty_cell = ws.cell(row=current_row, column=3, value=item.quantity)
        qty_cell.number_format = "#,##0.00"
        qty_cell.alignment = Alignment(horizontal="center")

        # Unit Price
        unit_cell = ws.cell(row=current_row, column=4, value=item.unit_price)
        unit_cell.number_format = "$#,##0.00"
        unit_cell.alignment = Alignment(horizontal="right")

        # Dynamic Formula for line total: =C[row]*D[row]
        total_cell = ws.cell(row=current_row, column=5, value=f"=C{current_row}*D{current_row}")
        total_cell.number_format = "$#,##0.00"
        total_cell.alignment = Alignment(horizontal="right")

        for col_idx in range(1, 6):
            c = ws.cell(row=current_row, column=col_idx)
            c.font = normal_font
            c.border = thin_border
            if i % 2 == 0:
                c.fill = accent_fill

        ws.row_dimensions[current_row].height = 19
        current_row += 1

    item_end_row = max(current_row - 1, item_start_row)

    # 4. Summary Calculation Section with Dynamic Excel Formulas
    summary_start = current_row + 1
    subtotal_row = summary_start
    discount_row = summary_start + 1
    tax_row      = summary_start + 2
    final_row    = summary_start + 3

    # Subtotal formula: =SUM(E[start]:E[end])
    ws.cell(row=subtotal_row, column=4, value="Subtotal:").font = bold_font
    ws.cell(row=subtotal_row, column=4).alignment = Alignment(horizontal="right")
    subtotal_cell = ws.cell(row=subtotal_row, column=5, value=f"=SUM(E{item_start_row}:E{item_end_row})")
    subtotal_cell.number_format = "$#,##0.00"
    subtotal_cell.font = bold_font
    subtotal_cell.alignment = Alignment(horizontal="right")

    # Discount
    ws.cell(row=discount_row, column=4, value="Discounts:").font = bold_font
    ws.cell(row=discount_row, column=4).alignment = Alignment(horizontal="right")
    disc_val = -abs(invoice.discounts) if invoice.discounts else 0.0
    disc_cell = ws.cell(row=discount_row, column=5, value=disc_val)
    disc_cell.number_format = "$#,##0.00"
    disc_cell.font = bold_font
    disc_cell.alignment = Alignment(horizontal="right")

    # Tax
    ws.cell(row=tax_row, column=4, value="Tax / Surcharges:").font = bold_font
    ws.cell(row=tax_row, column=4).alignment = Alignment(horizontal="right")
    tax_cell = ws.cell(row=tax_row, column=5, value=invoice.tax_amount or 0.0)
    tax_cell.number_format = "$#,##0.00"
    tax_cell.font = bold_font
    tax_cell.alignment = Alignment(horizontal="right")

    # Final Total Formula: =E[subtotal]+E[discount]+E[tax]
    ws.cell(row=final_row, column=4, value="FINAL BALANCE DUE:").font = bold_font
    ws.cell(row=final_row, column=4).alignment = Alignment(horizontal="right")
    ws.cell(row=final_row, column=4).fill = total_fill
    ws.cell(row=final_row, column=4).border = double_bottom_border

    final_cell = ws.cell(row=final_row, column=5, value=f"=E{subtotal_row}+E{discount_row}+E{tax_row}")
    final_cell.number_format = "$#,##0.00"
    final_cell.font = bold_font
    final_cell.alignment = Alignment(horizontal="right")
    final_cell.fill = total_fill
    final_cell.border = double_bottom_border
    ws.row_dimensions[final_row].height = 24

    # Auto-adjust column widths
    for col in ws.columns:
        max_len = 0
        col_letter = get_column_letter(col[0].column)
        for cell in col:
            if cell.row == 1:
                continue
            val_str = str(cell.value or "")
            if len(val_str) > max_len:
                max_len = len(val_str)
        ws.column_dimensions[col_letter].width = max(max_len + 4, 12)

    ws.column_dimensions["B"].width = max(ws.column_dimensions["B"].width, 42)


def export_invoice_to_excel(invoice: InvoiceData, output_path: Union[str, Path]) -> Path:
    """Exports a single invoice to a standalone Excel file."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = f"INV-{invoice.invoice_number[:15]}"
    populate_invoice_sheet(ws, invoice)
    wb.save(output_path)
    return output_path


def export_batch_summary_to_excel(invoices: List[InvoiceData], output_path: Union[str, Path]) -> Path:
    """
    Exports multiple invoices into a single master workbook with:
    1. Executive Summary & KPI Register sheet
    2. An individual itemized sheet for each processed invoice
    """
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    ws_summary = wb.active
    ws_summary.title = "Master Invoice Register"
    ws_summary.views.sheetView[0].showGridLines = True

    title_font = Font(name="Calibri", size=16, bold=True, color=COLOR_PRIMARY_NAVY)
    kpi_title_font = Font(name="Calibri", size=9, bold=True, color="595959")
    kpi_num_font = Font(name="Calibri", size=16, bold=True, color=COLOR_PRIMARY_NAVY)
    bold_font = Font(name="Calibri", size=10, bold=True)
    normal_font = Font(name="Calibri", size=10)
    header_fill = PatternFill(start_color=COLOR_PRIMARY_NAVY, end_color=COLOR_PRIMARY_NAVY, fill_type="solid")
    header_font = Font(name="Calibri", size=10, bold=True, color=COLOR_HEADER_TEXT)
    kpi_fill = PatternFill(start_color="F2F5F9", end_color="F2F5F9", fill_type="solid")
    accent_fill = PatternFill(start_color=COLOR_ACCENT_ROW, end_color=COLOR_ACCENT_ROW, fill_type="solid")
    thin_border = _get_borders()

    # Title
    ws_summary["A1"] = "EXECUTIVE INVOICE REGISTER & AUDIT REPORT"
    ws_summary["A1"].font = title_font
    ws_summary.row_dimensions[1].height = 30

    # KPI Card 1: Total Invoices
    ws_summary.merge_cells("A3:B3")
    ws_summary["A3"] = "TOTAL INVOICES PROCESSED"
    ws_summary["A3"].font = kpi_title_font
    ws_summary["A3"].alignment = Alignment(horizontal="center")
    ws_summary.merge_cells("A4:B4")
    ws_summary["A4"] = len(invoices)
    ws_summary["A4"].font = kpi_num_font
    ws_summary["A4"].alignment = Alignment(horizontal="center")

    # KPI Card 2: Total Net Spend Formula
    ws_summary.merge_cells("C3:E3")
    ws_summary["C3"] = "TOTAL CUMULATIVE BALANCE"
    ws_summary["C3"].font = kpi_title_font
    ws_summary["C3"].alignment = Alignment(horizontal="center")
    ws_summary.merge_cells("C4:E4")
    start_table_row = 8
    end_table_row = start_table_row + len(invoices) - 1
    ws_summary["C4"] = f"=SUM(H{start_table_row}:H{end_table_row})"
    ws_summary["C4"].font = kpi_num_font
    ws_summary["C4"].number_format = "$#,##0.00"
    ws_summary["C4"].alignment = Alignment(horizontal="center")

    # Apply card styling
    for r in range(3, 5):
        for col_idx in range(1, 6):
            cell = ws_summary.cell(row=r, column=col_idx)
            cell.fill = kpi_fill
            cell.border = thin_border

    # Register Table Headers
    cols = [
        ("#", 6),
        ("Invoice Number", 22),
        ("Vendor Name", 30),
        ("Customer Name", 28),
        ("Issue Date", 14),
        ("Due Date", 14),
        ("Items", 8),
        ("Total Amount", 16),
        ("Currency", 10),
    ]

    for col_idx, (header_text, width) in enumerate(cols, start=1):
        cell = ws_summary.cell(row=start_table_row - 1, column=col_idx, value=header_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(horizontal="center" if col_idx in (1, 5, 6, 7, 9) else ("right" if col_idx == 8 else "left"))
        col_letter = get_column_letter(col_idx)
        ws_summary.column_dimensions[col_letter].width = width

    ws_summary.row_dimensions[start_table_row - 1].height = 24

    for idx, inv in enumerate(invoices, start=1):
        row_num = start_table_row + idx - 1
        ws_summary.cell(row=row_num, column=1, value=idx).alignment = Alignment(horizontal="center")
        ws_summary.cell(row=row_num, column=2, value=inv.invoice_number).font = bold_font
        ws_summary.cell(row=row_num, column=3, value=inv.vendor_name)
        ws_summary.cell(row=row_num, column=4, value=inv.customer_name)
        ws_summary.cell(row=row_num, column=5, value=inv.issue_date or "N/A").alignment = Alignment(horizontal="center")
        ws_summary.cell(row=row_num, column=6, value=inv.due_date or "N/A").alignment = Alignment(horizontal="center")
        ws_summary.cell(row=row_num, column=7, value=len(inv.line_items)).alignment = Alignment(horizontal="center")
        
        amt_cell = ws_summary.cell(row=row_num, column=8, value=inv.total_amount)
        amt_cell.number_format = "$#,##0.00"
        amt_cell.font = bold_font
        amt_cell.alignment = Alignment(horizontal="right")

        ws_summary.cell(row=row_num, column=9, value=inv.currency).alignment = Alignment(horizontal="center")

        for c_idx in range(1, 10):
            c = ws_summary.cell(row=row_num, column=c_idx)
            c.font = normal_font if c_idx != 2 and c_idx != 8 else bold_font
            c.border = thin_border
            if idx % 2 == 0:
                c.fill = accent_fill

        ws_summary.row_dimensions[row_num].height = 20

        # Also create a dedicated tab for each invoice in the workbook
        sheet_title = f"{idx}_{inv.invoice_number[:12]}".replace("/", "-")
        inv_sheet = wb.create_sheet(title=sheet_title)
        populate_invoice_sheet(inv_sheet, inv)

    wb.save(output_path)
    return output_path
