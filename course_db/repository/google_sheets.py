import os.path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build
from googleapiclient.errors import HttpError

from course_db.models.exceptions import GoogleSheetsError
from course_db.services.big_table import BigTable
from course_db.services.grading import components_2025, grading_2025

# If modifying these scopes, delete the file token.json.
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]

# The ID and range of a sample spreadsheet.
SAMPLE_SPREADSHEET_ID = "1NTZ26M6tKWzb5g7t0B83i4J-dQrqh7O-TnlAPxd4gsw"
SAMPLE_RANGE_NAME = "Test sheet"


def load(spreadsheet_id: str) -> BigTable:
    creds = _setup_auth()

    raw = _load_raw(creds)

    return _to_structured(raw)


def save(table: BigTable):
    pass


def _setup_auth():
    creds = None
    # The file token.json stores the user's access and refresh tokens, and is
    # created automatically when the authorization flow completes for the first
    # time.

    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    # If there are no (valid) credentials available, let the user log in.
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        # Save the credentials for the next run
        with open("token.json", "w") as token:
            token.write(creds.to_json())

    return creds


def _load_raw(creds) -> list[list[str]]:
    try:
        service = build("sheets", "v4", credentials=creds)

        # Call the Sheets API
        sheet = service.spreadsheets()
        result = (
            sheet.values()
            .get(spreadsheetId=SAMPLE_SPREADSHEET_ID, range=SAMPLE_RANGE_NAME)
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

    print(actual_columns)
    print(expected_columns)

    if actual_columns != expected_columns:
        raise GoogleSheetsError(
            "Spreadsheet columns do not match expected format. "
            f"Expected: {expected_columns}, got: {actual_columns}"
        )
