from http.server import BaseHTTPRequestHandler, HTTPServer
from argon2.exceptions import VerifyMismatchError
from argon2.exceptions import InvalidHashError
from argon2 import PasswordHasher
import subprocess, threading, sys, json, os
from socketserver import ThreadingMixIn



# $argon2id$v=19$m=65536,t=3,p=4$Fhd7NSc6DpTtPRxIFZADCA$o8Tt3Y/bWlLmKnZFXNKq9Bgnz90EohLO/Dk1DZOwCAk is hash of 1234
address = 'localhost:8000'
_dir = '~/Python/backend'
base_dir = '~/Python/backend/base.json'

ph = PasswordHasher()
DIR = os.path.expanduser(os.path.expandvars(_dir))
BASE_DIR = os.path.expanduser(os.path.expandvars(base_dir))
BASE_DIR_HTTP = BASE_DIR.removeprefix(DIR)



verbose_count_v = sys.argv.count('-v')
verbose_count_vv = sys.argv.count('-vv')
verbose_mode = 2 if verbose_count_vv > 0 else (1 if verbose_count_v > 0 else 0)
sys.argv = [arg for arg in sys.argv if arg not in ('-v', '-vv')]

def verbose(text, verbose_value=1): # -vv should be using only for debbuging because it can reveal users passwords
    if verbose_mode >= int(verbose_value):
        print(text)
    else:
        return


def passCheck(username, password):
    try:
        with open(f'{DIR}/base.json', "r", encoding="utf-8") as f:
            _hash = json.dumps(json.load(f)[f'{username}']['hash'])[1:][:-1]
            verbose(_hash, 2)
    except(KeyError):
        # verbose(f'User with username {username} not found in file')
        return(0)
    try:
        ph.verify(_hash, password)
        return(1)
    except VerifyMismatchError:
        # verbose('Invalid password')
        return(0)
    except InvalidHashError:
        # verbose('Invalid hash')
        return(-1)



class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/' or self.path == '/ ':
                self.path = '/index.html'
            
            if self.path == BASE_DIR_HTTP: # without this it will reveal all hashes, users, emails and etc
                self.path = '/404'

            if '..' in self.path:
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'Forbidden')
                return
            
            if self.path == '/LICENSE':
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'Forbidden')
                return
            
            if self.path.startswith('/.git') == '/.git/HEAD':
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'Forbidden')
                return

            if self.path.startswith('/other'):
                self.send_response(403)
                self.end_headers()
                self.wfile.write(b'Forbidden')
                return

            else:
                try: # this can be removed if there wont be any new pages # this makes some security holes if wont be handled properly1
                    with open(DIR + self.path, 'rb') as f:
                        content = f.read()
                except FileNotFoundError:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Not found')
                    return
        except(IsADirectoryError):
            verbose(f'{self.client_address[0]} tried to access directory', 1)
            self.send_response(403)
            self.end_headers()
            self.wfile.write(b'Forbidden')
            return
        except Exception as e:
            self.send_response(500)
            self.end_headers()
            verbose(f'Unexcepted error | POST | {e}')
            self.wfile.write(b'This error should not happen')
            return
        
        self.send_response(200)
        self.send_header('Content-Type', 'text/html')
        self.end_headers()
        self.wfile.write(content)
    
            
    
    def do_POST(self):
        if self.headers.get('Content-type') == 'application/json':
            try:
                content_length = int(self.headers.get('Content-Length', 0))
                post_body = self.rfile.read(content_length).decode('utf-8')
                verbose(f'Length: {content_length}, Body: {post_body}', 2)
                
                try:
                    data = json.loads(post_body)
                    verbose(f'{data}', 2)
                except json.JSONDecodeError:
                    self.send_response(400, 'Invalid JSON') # 
                    self.end_headers()
                    return
                
                # Auth check
                # result = passCheck(data.get('username'), data.get('password'))
                if passCheck(data.get('username'), data.get('password')) == 0: # если passCheck возвращает 1 то оно передает Failed to authorize с кодом ошибки 401
                    self.send_response(401, 'Failed to authorize')
                    verbose(f'{self.client_address[0]} failed to authorize as {data.get('username')}')
                    self.end_headers()
                    return
                elif passCheck(data.get('username'), data.get('password')) == 1: # если passCheck возвращает 1 то оно передает Successfully authorized
                    self.send_response(200, "Successfully authorized")
                    verbose(f'{self.client_address[0]} succesfully authorized as {data.get('username')}')
                    self.end_headers()
                    return
                else:
                    self.send_response(500, 'Failed to authorize')
                    verbose(f'{self.client_address[0]} tried to authorize as {data.get('username')} but there was an issue with hash')
                    self.end_headers()
                    return
            except Exception as e:
                print(f'Unexcepted error | POST | {e}')
                sys.exit(-3)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    '''Handle requests in a separate thread.''' # я низнаю зачем это нужно но пусть будет

if __name__ == '__main__':
    try:
        address1= str(address.split(':')[0]) # Чтобы вверху адресс менять легко (например чтобы в локальной сети тоже вебсайт был)
        address2= int(address.split(':')[1])
        server = ThreadedHTTPServer((f'{address1}', address2), Handler)
        print(f'Starting server on http://{address} use <Ctrl-C> to stop')
        server.serve_forever()
    except(KeyboardInterrupt):
        print('\nStopping server')
        sys.exit(0)