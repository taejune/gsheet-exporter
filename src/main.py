from http.server import HTTPServer
from functools import partial
import os
import sys
import server
import gsheet
import skopeo_util
import shellrunner

if __name__ == '__main__':
    default_sheet = os.environ.get('SHEET_URL')
    default_num = os.environ.get('SHEET_IDX')
    default_col = os.environ.get('COL_NUM')
    default_row = os.environ.get('ROW_FROM')
    default_registry = os.environ.get('REGISTRY_URL')
    default_archive_path = os.environ.get('ARCHIVE_PATH')
    default_scp_dest = os.environ.get('SCP_DEST')
    default_scp_pass = os.environ.get('SCP_PASS')

    for v in [default_sheet, default_num, default_col, default_row, default_registry,
              default_archive_path, default_scp_dest, default_scp_pass]:
        if v is None:
            sys.exit('[FATAL]: no specified necessary envs')

    fetcher = gsheet.GoogleSheetFetcher(default_sheet,
                                        default_num,
                                        default_col,
                                        default_row)

    skopeo = skopeo_util.SkopeoUtil(os.environ.get('DOCKER_CRED'),
                                    os.environ.get('QUAY_CRED'),
                                    os.environ.get('GCR_CRED'),
                                    default_registry)

    archiver = shellrunner.Command('tar --create --file=/tmp/images.tar {SRC}'.format(SRC=default_archive_path))
    uploader = shellrunner.Command('sshpass -p{PASSWORD} scp -o StrictHostKeyChecking=no '
                                   '/tmp/images.tar {DEST}'.format(PASSWORD=default_scp_pass, DEST=default_scp_dest))

    print('Default sync: {sheet}'.format(sheet=default_sheet, reg=default_registry))
    print('Listening on 8080...')
    handler = partial(server.myHandler, fetcher, skopeo, archiver, uploader)
    httpd = HTTPServer(('', 8080), handler)
    httpd.serve_forever()
