"""
Lead Exporter module for ai-data-toolkit.
Exports structured business leads into:
1. Executive Excel Workbook with KPI cards, clickable mailto/web links, and quality badges.
2. UTF-8 CSV file ready for CRM / Apollo / HubSpot import.
"""

import csv
from pathlib import Path
from typing import List, Union
import openpyxl
from openpyxl.styles import Font, Alignment, PatternFill, Border, Side
from openpyxl.utils import get_column_letter

from .lead_schema import BusinessLead


# Design Colors
COLOR_NAVY_HEADER  = "1B365D"
COLOR_WHITE        = "FFFFFF"
COLOR_ZEBRA_ROW    = "F8FAFC"
COLOR_BORDER       = "D9D9D9"
COLOR_CARD_BG      = "F1F5F9"

# Tier Colors
COLOR_TIER_HIGH_BG   = "E2EFDA"   # Soft green
COLOR_TIER_HIGH_TXT  = "375623"
COLOR_TIER_MED_BG    = "FFF2CC"   # Soft yellow
COLOR_TIER_MED_TXT   = "7F6000"
COLOR_TIER_LOW_BG    = "FCE4D6"   # Soft red
COLOR_TIER_LOW_TXT   = "C65911"


def export_leads_to_csv(leads: List[BusinessLead], output_path: Union[str, Path]) -> Path:
    """Exports leads into a standard CRM-importable CSV file (UTF-8 with BOM)."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    headers = [
        "Company Name",
        "Contact Name",
        "Title / Role",
        "Primary Email",
        "Secondary Email",
        "Phone",
        "Website",
        "Street Address",
        "City",
        "State",
        "Postal Code",
        "Specialties",
        "Notes",
        "Completeness Score",
        "Quality Tier",
    ]

    with open(output_path, mode="w", newline="", encoding="utf-8-sig") as f:
        writer = csv.writer(f)
        writer.writerow(headers)
        for lead in leads:
            writer.writerow([
                lead.company_name,
                lead.contact_name or "",
                lead.title_or_role or "",
                lead.primary_email or "",
                lead.secondary_email or "",
                lead.phone or "",
                lead.website or "",
                lead.street_address or "",
                lead.city or "",
                lead.state or "",
                lead.postal_code or "",
                ", ".join(lead.specialties),
                lead.notes or "",
                f"{lead.completeness_score}%",
                lead.quality_tier,
            ])

    return output_path


def export_leads_to_excel(leads: List[BusinessLead], output_path: Union[str, Path]) -> Path:
    """Exports leads into a publication-grade Excel sheet with live KPIs and hyperlinks."""
    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    wb = openpyxl.Workbook()
    ws = wb.active
    ws.title = "Verified Leads Directory"
    ws.views.sheetView[0].showGridLines = True

    title_font = Font(name="Calibri", size=15, bold=True, color=COLOR_NAVY_HEADER)
    kpi_title_font = Font(name="Calibri", size=9, bold=True, color="595959")
    kpi_num_font = Font(name="Calibri", size=15, bold=True, color=COLOR_NAVY_HEADER)
    header_font = Font(name="Calibri", size=10, bold=True, color=COLOR_WHITE)
    bold_font = Font(name="Calibri", size=10, bold=True)
    normal_font = Font(name="Calibri", size=10)
    link_font = Font(name="Calibri", size=10, color="0563C1", underline="single")

    header_fill = PatternFill(start_color=COLOR_NAVY_HEADER, end_color=COLOR_NAVY_HEADER, fill_type="solid")
    accent_fill = PatternFill(start_color=COLOR_ZEBRA_ROW, end_color=COLOR_ZEBRA_ROW, fill_type="solid")
    card_fill = PatternFill(start_color=COLOR_CARD_BG, end_color=COLOR_CARD_BG, fill_type="solid")

    thin_side = Side(style="thin", color=COLOR_BORDER)
    thin_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    # 1. Title Banner
    ws["A1"] = "🎯 ENRICHED B2B LEAD DIRECTORY & AUDIT REPORT"
    ws["A1"].font = title_font
    ws["A1"].alignment = Alignment(vertical="center")
    ws.row_dimensions[1].height = 28

    # 2. Executive KPI Cards (Row 3 to 4)
    total_leads = len(leads)
    emails_count = sum(1 for l in leads if l.primary_email)
    phones_count = sum(1 for l in leads if l.phone)
    avg_score = round(sum(l.completeness_score for l in leads) / total_leads, 1) if total_leads else 0

    kpis = [
        ("TOTAL LEADS", total_leads, "A", "B"),
        ("VERIFIED EMAILS", f"{emails_count} ({round(emails_count/total_leads*100)}%)" if total_leads else "0", "C", "D"),
        ("PHONE NUMBERS", f"{phones_count} ({round(phones_count/total_leads*100)}%)" if total_leads else "0", "E", "F"),
        ("AVG QUALITY SCORE", f"{avg_score}%", "G", "H"),
    ]

    for label, val, c_start, c_end in kpis:
        ws.merge_cells(f"{c_start}3:{c_end}3")
        top_cell = ws[f"{c_start}3"]
        top_cell.value = label
        top_cell.font = kpi_title_font
        top_cell.alignment = Alignment(horizontal="center", vertical="center")

        ws.merge_cells(f"{c_start}4:{c_end}4")
        val_cell = ws[f"{c_start}4"]
        val_cell.value = val
        val_cell.font = kpi_num_font
        val_cell.alignment = Alignment(horizontal="center", vertical="center")

        for col_letter in [c_start, c_end]:
            for r in (3, 4):
                ws[f"{col_letter}{r}"].fill = card_fill
                ws[f"{col_letter}{r}"].border = thin_border

    ws.row_dimensions[3].height = 18
    ws.row_dimensions[4].height = 24

    # 3. Table Headers (Row 7)
    start_row = 7
    headers = [
        ("#", 5),
        ("Company Name", 28),
        ("Contact & Title", 24),
        ("Primary Email", 28),
        ("Phone", 18),
        ("Website", 26),
        ("Location", 20),
        ("Specialties / Services", 32),
        ("Quality Tier", 16),
        ("Score", 10),
    ]

    for col_idx, (h_text, width) in enumerate(headers, start=1):
        cell = ws.cell(row=start_row, column=col_idx, value=h_text)
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = Alignment(
            horizontal="center" if col_idx in (1, 5, 7, 9, 10) else "left",
            vertical="center"
        )
        ws.column_dimensions[get_column_letter(col_idx)].width = width

    ws.row_dimensions[start_row].height = 24

    # 4. Populate Lead Rows
    current_row = start_row + 1
    for idx, lead in enumerate(leads, start=1):
        ws.cell(row=current_row, column=1, value=idx).alignment = Alignment(horizontal="center")
        
        # Company
        comp_cell = ws.cell(row=current_row, column=2, value=lead.company_name)
        comp_cell.font = bold_font

        # Contact & Role
        contact_display = lead.contact_name or ""
        if lead.title_or_role:
            contact_display += f" ({lead.title_or_role})" if contact_display else lead.title_or_role
        ws.cell(row=current_row, column=3, value=contact_display or "N/A")

        # Email with clickable mailto: hyperlink
        email_cell = ws.cell(row=current_row, column=4, value=lead.primary_email or "N/A")
        if lead.primary_email and "@" in lead.primary_email:
            email_cell.hyperlink = f"mailto:{lead.primary_email}"
            email_cell.font = link_font
        else:
            email_cell.font = normal_font

        # Phone
        ws.cell(row=current_row, column=5, value=lead.phone or "N/A").alignment = Alignment(horizontal="center")

        # Website with clickable hyperlink
        web_cell = ws.cell(row=current_row, column=6, value=lead.website or "N/A")
        if lead.website and lead.website.startswith("http"):
            web_cell.hyperlink = lead.website
            web_cell.font = link_font
        else:
            web_cell.font = normal_font

        # Location (City, State)
        loc = ", ".join(filter(None, [lead.city, lead.state]))
        ws.cell(row=current_row, column=7, value=loc or "N/A").alignment = Alignment(horizontal="center")

        # Specialties
        specs = ", ".join(lead.specialties) if lead.specialties else "General"
        ws.cell(row=current_row, column=8, value=specs)

        # Quality Tier Badge Pill
        tier = lead.quality_tier
        tier_cell = ws.cell(row=current_row, column=9, value=tier)
        tier_cell.alignment = Alignment(horizontal="center", vertical="center")
        if tier == "HIGH QUALITY":
            tier_cell.fill = PatternFill(start_color=COLOR_TIER_HIGH_BG, end_color=COLOR_TIER_HIGH_BG, fill_type="solid")
            tier_cell.font = Font(name="Calibri", size=9, bold=True, color=COLOR_TIER_HIGH_TXT)
        elif tier == "MEDIUM":
            tier_cell.fill = PatternFill(start_color=COLOR_TIER_MED_BG, end_color=COLOR_TIER_MED_BG, fill_type="solid")
            tier_cell.font = Font(name="Calibri", size=9, bold=True, color=COLOR_TIER_MED_TXT)
        else:
            tier_cell.fill = PatternFill(start_color=COLOR_TIER_LOW_BG, end_color=COLOR_TIER_LOW_BG, fill_type="solid")
            tier_cell.font = Font(name="Calibri", size=9, bold=True, color=COLOR_TIER_LOW_TXT)

        # Completeness %
        score_cell = ws.cell(row=current_row, column=10, value=f"{lead.completeness_score}%")
        score_cell.alignment = Alignment(horizontal="center", vertical="center")
        score_cell.font = bold_font

        for col_idx in range(1, 11):
            c = ws.cell(row=current_row, column=col_idx)
            c.border = thin_border
            if idx % 2 == 0 and col_idx != 9:
                c.fill = accent_fill

        ws.row_dimensions[current_row].height = 20
        current_row += 1

    # 5. Enterprise Usability: Freeze Panes and AutoFilter
    if leads:
        ws.auto_filter.ref = f"A{start_row}:J{current_row - 1}"
    ws.freeze_panes = "A8"

    wb.save(output_path)
    return output_path
