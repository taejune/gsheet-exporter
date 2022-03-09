from http.server import HTTPServer
import server

if __name__ == '__main__':
    print('Listening on 8080...')
    httpd = HTTPServer(('', 8080), server.myHandler)
    httpd.serve_forever()
