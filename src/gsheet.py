from bs4 import BeautifulSoup
import requests

class GoogleSheetFetcher:
    def __init__(self, sheet_url, sheet_number, column, row_from):
        self.url = sheet_url
        self.sheet_number = int(sheet_number)
        self.column = int(column)
        self.row_from = int(row_from)

    def parse_list(self, sheet_url, sheet_number, column, row_from):
        sheet_url = sheet_url if sheet_url != None else self.url
        sheet_number = int(sheet_number) if sheet_number != None else self.sheet_number
        column = int(column) if column != None else self.column
        row_from = int(row_from) if row_from != None else self.row_from

        sheets = BeautifulSoup(requests.get(sheet_url).text, "lxml").find_all("table")
        table = ([[td.text for td in tr.find_all("td")] for tr in sheets[sheet_number].find_all("tr")])
        return [row[column] for row in table[row_from:] if len(row[column]) > 0]