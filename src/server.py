from http.server import HTTPServer, BaseHTTPRequestHandler
import urllib.parse as urlparse
import os
import re
import json
import cgi
import gsheet
import skopeoutil

class myHandler(BaseHTTPRequestHandler):
  def __init__(self, fetcher, skopeo, *args, **kargs):
    self.fetcher = fetcher
    self.skopeo = skopeo
    super().__init__(*args, **kargs)

  def __get_Parameter(self, key):
    if hasattr(self, "_myHandler__param") == False:
      if "?" in self.path:
        self.__param = dict(urlparse.parse_qsl(self.path.split("?")[1], True))
      else :
        self.__param = {}
    if key in self.__param:
      return self.__param[key]
    return None

  def __set_Header(self, code):
    self.send_response(code)
    self.send_header('Content-type','text/html')
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
    # refuse to receive non-json content
    if ctype != 'application/json':
      self.send_response(400)
      self.end_headers()
      return
    # read the message and convert it into a python dictionary
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

    print('Archiving...')
    print('Uploading...')
    #     response = requests.get(notify_to)
    #     results['uploads'] = { 'status': response.status_code, 'msg': response.text }
    self.__set_Header(200)
    self.wfile.write(bytes(json.dumps(results), 'utf-8'))

  def do_GET(self):
    self.__set_Header(200)