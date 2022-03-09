from http.server import HTTPServer
from functools import partial
import os
import sys
import server
import gsheet
import skopeoutil

if __name__ == '__main__':
    default_sheet = os.environ.get('SHEET_URL')
    default_num = os.environ.get('SHEET_IDX')
    default_col = os.environ.get('COL_NUM')
    default_row = os.environ.get('ROW_FROM')
    default_registry = os.environ.get('REGISTRY_URL')

    for v in [default_sheet, default_num, default_col, default_row, default_registry]:
        if v is None:
            sys.exit('[FATAL]: no specified necessary envs')

    fetcher = gsheet.GoogleSheetFetcher(default_sheet,
                                        default_num,
                                        default_col,
                                        default_row)

    skopeo = skopeoutil.SkopeoUtil(os.environ.get('DOCKER_CRED'),
                                   os.environ.get('QUAY_CRED'),
                                   os.environ.get('GCR_CRED'),
                                   default_registry)

    print('Default sync: {sheet}'.format(sheet=default_sheet, reg=default_registry))
    print('Listening on 8080...')
    handler = partial(server.myHandler, fetcher, skopeo)
    httpd = HTTPServer(('', 8080), handler)
    httpd.serve_forever()
