import time
import os
import json
import cgi
from http.server import BaseHTTPRequestHandler
import urllib.parse as urlparse

class myHandler(BaseHTTPRequestHandler):
    def __init__(self, fetcher, skopeo, runner, *args, **kargs):
        self.fetcher = fetcher
        self.skopeo = skopeo
        self.runner = runner
        super().__init__(*args, **kargs)

    def __get_Parameter(self, key):
        if hasattr(self, "_myHandler__param") == False:
            if "?" in self.path:
                self.__param = dict(urlparse.parse_qsl(self.path.split("?")[1], True))
            else:
                self.__param = {}
        if key in self.__param:
            return self.__param[key]
        return None

    def __set_Header(self, code):
        self.send_response(code)
        self.send_header('Content-type', 'text/html')
        self.end_headers()

    def __set_Body(self, data):
        self.wfile.write(data.encode())

    def __get_Post_Parameter(self, key):
        if hasattr(self, "_myHandler__post_param") == False:
            data = self.rfile.read(int(self.headers['Content-Length']))
        if data is not None:
            self.__post_param = dict(urlparse.parse_qs(data.decode()))
        else:
            self.__post_param = {}

        if key in self.__post_param:
            return self.__post_param[key][0]
        return None

    def do_POST(self):
        print('{request} from {client}...'.format(request=self.requestline, client=self.client_address))
        ctype, pdict = cgi.parse_header(self.headers['Content-Type'])
        if ctype != 'application/json':
            self.send_response(400)
            self.end_headers()
            return
        length = int(self.headers['Content-Length'])
        message = json.loads(self.rfile.read(length))
        targets = self.fetcher.parse_list(message.get('url'),
                                          message.get('num'),
                                          message.get('col'),
                                          message.get('row'))
        copied = []
        failed = []
        for name in targets:
            img, ok, reason = self.skopeo.copy(name)
            if ok:
                print('Copying {img} success'.format(img=img))
                copied.append(img)
            else:
                print('[WARN] Copying {img} failed... (reason: {reason})'.format(img=img, reason=reason))
                failed.append({img: reason})
        results = {'sync': {}}
        results['sync']['success'] = copied
        results['sync']['failed'] = failed
        tar_name = time.strftime('%Y%m%d-%H%M%S', time.localtime(time.time())) + '.tar'
        print('Archiving', tar_name, os.environ.get('ARCHIVE_PATH'), '...')
        archive = {}
        ok, reason = self.runner.run('tar --create --file={TAR} {SRC}'
                                     .format(TAR=tar_name, SRC=os.environ.get('ARCHIVE_PATH')))
        if ok:
            archive['status'] = 'success'
        else:
            archive['status'] = 'fail'
            archive['reason'] = reason

        print('Uploading', tar_name, 'to', os.environ.get('SCP_DEST'), '...')
        upload = {}
        ok, reason = self.runner.run('sshpass -p{PASSWORD} scp -o StrictHostKeyChecking=no {TAR} {DEST}'
                                     .format(TAR=tar_name, PASSWORD=os.environ.get('SCP_PASS'),DEST=os.environ.get('SCP_DEST')))
        if ok:
            upload['status'] = 'success'
        else:
            upload['status'] = 'fail'
            upload['reason'] = reason

        results['archive'] = archive
        results['upload'] = upload

        if archive['status'] == 'success':
            ok, reason = self.runner.run('rm -rf {TAR}'.format(TAR=tar_name))
            if not ok:
                print('failed to delete tar:', reason)

        self.__set_Header(200)
        self.wfile.write(bytes(json.dumps(results), 'utf-8'))

    def do_GET(self):
        self.__set_Header(200)
