from http.server import HTTPServer
from functools import partial
import os
import sys
import server
import gsheet
import skopeo
import shellrunner

if __name__ == '__main__':
    for v in [os.environ.get('SHEET_URL'), os.environ.get('SHEET_IDX'),
              os.environ.get('COL_NUM'), os.environ.get('ROW_FROM'), os.environ.get('REGISTRY_URL'),
              os.environ.get('ARCHIVE_PATH'), os.environ.get('SCP_DEST'), os.environ.get('SCP_PASS')]:
        if v is None:
            sys.exit('[FATAL]: no specified necessary envs')

    fetcher = gsheet.GoogleSheetFetcher(os.environ.get('SHEET_URL'),
                                        os.environ.get('SHEET_IDX'),
                                        os.environ.get('COL_NUM'),
                                        os.environ.get('ROW_FROM'))

    skopeo = skopeo.SkopeoUtil(os.environ.get('DOCKER_CRED'),
                                    os.environ.get('QUAY_CRED'),
                                    os.environ.get('GCR_CRED'),
                                    os.environ.get('REGISTRY_URL'))

    runner = shellrunner.Command()

    print('Default sync: {sheet}'.format(sheet=os.environ.get('SHEET_URL'), reg=os.environ.get('REGISTRY_URL')))
    print('Listening on 8080...')
    handler = partial(server.myHandler, fetcher, skopeo, runner)
    httpd = HTTPServer(('', 8080), handler)
    httpd.serve_forever()
