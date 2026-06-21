from io import BytesIO
import pandas as pd
from datetime import datetime

from openpyxl.drawing.image import Image as ExcelImage
from openpyxl.styles import Font, Alignment, PatternFill


def generate_excel_report(
    df,
    report_title,
    file_name="report.xlsx"
):

    excel_buffer = BytesIO()

    with pd.ExcelWriter(
        excel_buffer,
        engine="openpyxl"
    ) as writer:

        # ================= DATA =================
        df.to_excel(
            writer,
            index=False,
            sheet_name="Report",
            startrow=7
        )

        workbook = writer.book
        worksheet = writer.sheets["Report"]

        # ================= LOGO =================
        try:
            logo = ExcelImage("logo.png")
            logo.width = 90
            logo.height = 90
            worksheet.add_image(logo, "A1")
        except:
            pass

        # ================= HEADER =================
        worksheet.merge_cells("C1:H1")
        worksheet["C1"] = "बाल युवा मंगलदल समिति"
        worksheet["C1"].font = Font(
            size=18,
            bold=True,
            color="F8D568"
        )
        worksheet["C1"].alignment = Alignment(
            horizontal="center"
        )

        worksheet.merge_cells("C2:H2")
        worksheet["C2"] = "मयलगांव"
        worksheet["C2"].font = Font(
            size=14,
            bold=True,
            color="EFD58A"
        )
        worksheet["C2"].alignment = Alignment(
            horizontal="center"
        )

        worksheet.merge_cells("C3:H3")
        worksheet["C3"] = (
            "हमारा गांव • हमारी पहचान • हमारा अभियान"
        )
        worksheet["C3"].font = Font(
            size=12,
            italic=True
        )
        worksheet["C3"].alignment = Alignment(
            horizontal="center"
        )

        worksheet.merge_cells("A5:H5")
        worksheet["A5"] = report_title
        worksheet["A5"].font = Font(
            size=16,
            bold=True
        )
        worksheet["A5"].alignment = Alignment(
            horizontal="center"
        )

        worksheet.merge_cells("A6:H6")
        worksheet["A6"] = (
            f"Generated On : "
            f"{datetime.now().strftime('%d-%m-%Y %I:%M %p')}"
        )
        worksheet["A6"].alignment = Alignment(
            horizontal="center"
        )

        # ================= TABLE HEADER STYLE =================
        for cell in worksheet[8]:
            cell.font = Font(bold=True)
            cell.fill = PatternFill(
                fill_type="solid",
                fgColor="D9D9D9"
            )
            cell.alignment = Alignment(horizontal="center")

        # ================= FIXED COLUMN WIDTH =================
        # Abhi testing ke liye fixed width rakh rahe hain
        for col in ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J"]:
            worksheet.column_dimensions[col].width = 25

    excel_buffer.seek(0)

    return excel_buffer
