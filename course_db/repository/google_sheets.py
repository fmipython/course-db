from google.oauth2.service_account import Credentials
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from course_db.models.exceptions import GoogleSheetsError
from course_db.services.big_table import BigTable
from course_db.services.grading import components_2025, grading_2025

SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]
SERVICE_ACCOUNT_FILE = "service_account.json"

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1NTZ26M6tKWzb5g7t0B83i4J-dQrqh7O-TnlAPxd4gsw"
SAMPLE_RANGE_NAME = "Test sheet"


def load(spreadsheet_id: str) -> BigTable:
    creds = setup_auth()

    raw = load_raw(creds, SAMPLE_SPREADSHEET_ID)

    return _to_structured(raw)


def save(table: BigTable):
    pass


def setup_auth():
    return Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)


def load_raw(creds, spreadsheet_id, spreadsheet_range) -> list[list[str]]:
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=spreadsheet_id, range=spreadsheet_range)
            .execute()
        )
        values = result.get("values", [])

        if not values:
            raise GoogleSheetsError("No data found in the spreadsheet.")

        return values
    except HttpError as err:
        raise GoogleSheetsError(f"An error occurred: {err}") from err


def _to_structured(raw: list[list[str]]) -> BigTable:
    table = BigTable(components_2025, grading_2025)
    actual_columns = raw[0]

    expected_columns = table.columns

    if actual_columns != expected_columns:
        raise GoogleSheetsError(
            "Spreadsheet columns do not match expected format. "
            f"Expected: {expected_columns}, got: {actual_columns}"
        )

    semi_structured = [_to_structured_row(row, actual_columns) for row in raw[1:]]

    for row in semi_structured:
        student_id = row[expected_columns[2]]
        # Main info
        table.add_student(
            row[expected_columns[0]], row[expected_columns[1]], student_id
        )

        # Bonus points
        table.set_bonus(student_id, int(row["Бонус"]))

        # Components
        for component in expected_columns[3:-3]:
            points = row[component]
            if points != "":
                table.set_points(
                    student_id, component, float(row[component].replace(",", "."))
                )

    return table


def _to_structured_row(row: list[str], columns: list[str]) -> dict[str, str]:
    result = {}
    for i, column in enumerate(columns):
        result[column] = row[i]

    return result
