import os
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

class GoogleSheetFetcher:
    def __init__(self, google_app_cred, sheet_id, range_name):
        self.google_app_cred = google_app_cred
        self.sheet_id = sheet_id
        self.range_name = range_name

    def parse_list(self, sheet_id, range_name):
        sheet_id = sheet_id if sheet_id  is not None else self.sheet_id
        range_name = range_name if range_name is not None else self.range_name

        key_file_name = self.google_app_cred
        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_name, scope)
        h = httplib2.Http()
        h = credentials.authorize(h)
        service = build('sheets', 'v4', http=h)
        sheet = service.spreadsheets()
        result = sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()

        values = result.get('values', [])
        contents = []
        for value in values:
            contents.append(value[0])
        return contents

def main():
    SPREADSHEET_ID = '1zBHhKvdz5sv2HZFWGcbsvAVFspQAvm_yEYtY9ZffSZc'
    RANGE_NAME = 'total images!B2:B'

    fetcher = GoogleSheetFetcher(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'), SPREADSHEET_ID, RANGE_NAME)

    print(fetcher.parse_list())
    # print(fetcher.parse_list())

if __name__ == '__main__':
    main()
