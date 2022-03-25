import os
import httplib2
from googleapiclient.discovery import build
from oauth2client.service_account import ServiceAccountCredentials

scope = ['https://spreadsheets.google.com/feeds',
         'https://www.googleapis.com/auth/drive']

class GoogleSheetFetcher:
    def __init__(self, key_file_name, default_targets):
        credentials = ServiceAccountCredentials.from_json_keyfile_name(key_file_name, scope)
        self.sheet = build('sheets', 'v4', http=credentials.authorize(httplib2.Http())).spreadsheets()
        self.default_targets = default_targets

    def parse_list(self, targets):
        res = []
        targets = targets if targets is not None else self.default_targets
        for target in targets.split(','):
            [sheet_id, range_name] = target.split(';')
            fetched = self.sheet.values().get(spreadsheetId=sheet_id, range=range_name).execute()
            rows = fetched.get('values', [])
            res = res + [r for r in rows if len(r) > 0]
        return res

def main():
    targetlists = '1zBHhKvdz5sv2HZFWGcbsvAVFspQAvm_yEYtY9ZffSZc;CK1!C2:D,1zBHhKvdz5sv2HZFWGcbsvAVFspQAvm_yEYtY9ZffSZc;CK2!C2:D'
    fetcher = GoogleSheetFetcher(os.environ.get('GOOGLE_APPLICATION_CREDENTIALS'), targetlists)
    res = fetcher.parse_list(os.environ.get('TARGET_SHEETS'))
    print(res)
    print(len(res))

if __name__ == '__main__':
    main()
