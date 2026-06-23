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

# =====================================================
# ================ RESTORE DATABASE ===================
# =====================================================

def restore_full_backup(uploaded_file, supabase):

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

    excel_file = pd.ExcelFile(uploaded_file)

    restored_tables = []

    for table_name in tables:

        if table_name in excel_file.sheet_names:

            try:

                df = pd.read_excel(
                    excel_file,
                    sheet_name=table_name
                )

                # Skip empty sheets
                if df.empty:
                    continue

                # Skip "No Data Found" sheets
                if "Message" in df.columns:
                    continue

                # Convert dataframe to records
                records = df.to_dict(
                    orient="records"
                )

                # ================= CLEAN DATA =================

                for row in records:

                    for key, value in row.items():

                        # NaN -> None
                        if pd.isna(value):
                            row[key] = None

                        # Empty String -> None
                        elif isinstance(value, str):

                            value = value.strip()

                            if value == "":
                                row[key] = None
                            else:
                                row[key] = value

                # ================= DELETE OLD DATA =================

                try:

                    existing_rows = (
                        supabase.table(table_name)
                        .select("id")
                        .execute()
                    )

                    if existing_rows.data:

                        for item in existing_rows.data:

                            supabase.table(table_name)\
                                .delete()\
                                .eq("id", item["id"])\
                                .execute()

                except Exception as e:

                    print(
                        f"Delete Error ({table_name}): {e}"
                    )

                # ================= INSERT NEW DATA =================

                if records:

                    supabase.table(table_name)\
                        .insert(records)\
                        .execute()

                restored_tables.append(
                    table_name
                )

                print(
                    f"{table_name} restored successfully"
                )

            except Exception as e:

                print(
                    f"ERROR in {table_name}: {str(e)}"
                )

                raise Exception(
                    f"{table_name}: {str(e)}"
                )

    return restored_tables
