from http.server import BaseHTTPRequestHandler, HTTPServer

class MyServer(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        with open('exploit.html', 'r') as f:
            self.send_header('Content-type', 'text/html')
            self.end_headers()
            self.wfile.write(f.read().encode())
        return

    def do_POST(self):
        flag = self.rfile.read(int(self.headers['Content-Length'])).decode('utf-8')
        print(flag)

def run():
    server_address = ('localhost', 8001)
    httpd = HTTPServer(server_address, MyServer)
    httpd.serve_forever()

run()