from io import BytesIO
from datetime import datetime
import pandas as pd


# =====================================================
# ============= FULL DATABASE BACKUP ==================
# =====================================================

def create_full_backup(supabase):

    tables = [
        "members",
        "collections",
        "collection_rates",
        "loans",
        "loan_payments",
        "donations",
        "expenses",
        "reminders",
        "users"
    ]

    backup_buffer = BytesIO()

    with pd.ExcelWriter(
        backup_buffer,
        engine="openpyxl"
    ) as writer:

        for table_name in tables:

            try:

                response = (
                    supabase.table(table_name)
                    .select("*")
                    .execute()
                )

                df = pd.DataFrame(response.data)

                if df.empty:
                    df = pd.DataFrame(
                        {"Message": ["No Data Found"]}
                    )

                # Excel sheet names max 31 chars
                sheet_name = table_name[:31]

                df.to_excel(
                    writer,
                    sheet_name=sheet_name,
                    index=False
                )

            except Exception as e:

                error_df = pd.DataFrame({
                    "Error": [str(e)]
                })

                error_df.to_excel(
                    writer,
                    sheet_name=table_name[:31],
                    index=False
                )

    backup_buffer.seek(0)

    filename = (
        f"meeting_backup_"
        f"{datetime.now().strftime('%d-%m-%Y_%I-%M-%p')}.xlsx"
    )

    return backup_buffer, filename
