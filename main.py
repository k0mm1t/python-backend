import http.server
import json
import sys
import socketserver
class Server(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == '/' or self.path == '/ ':
            self.path = '/index.html'

        if self.path == '/d':
            self.path = '/d.html'

        try:
            with open('.' + self.path, 'rb') as f:
                content = f.read()
        except FileNotFoundError:
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(content)
    
            
    
    def do_POST(self):
        if self.headers.get('Content-type') == 'application/json':
            try:
                with open('./d.json', 'r') as f:
                    file_content = f.read()
                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(file_content.encode('utf-8'))
                return
            except FileNotFoundError:
                self.send_response(404)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'status': 'error', "message": "d.json not found"}).encode('utf-8'))
                return
            # except json.JSONDecodeError:
            #      self.send_response(500)
            #      self.send_header('Content-type', 'application/json')
            #      self.end_headers()
            #      self.wfile.write(json.dumps({'status': 'error', "message": "d.json contains invalid JSON"}).encode('utf-8'))
            #      return
        else:
            self.send_response(400)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps({'status': 'error', "message": "invalid Content-type"}).encode('utf-8'))

    def serve_forever(port):
        socketserver.TCPServer(('', port), Server).serve_forever()
if __name__ == "__main__":
    try:
        Server.serve_forever(8000)
    except(KeyboardInterrupt):
        sys.exit(0)
