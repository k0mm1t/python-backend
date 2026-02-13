from http.server import BaseHTTPRequestHandler, HTTPServer

from argon2.exceptions import VerifyMismatchError
from argon2.exceptions import InvalidHashError
from argon2 import PasswordHasher

import json
import sqlite3
import threading, sys, os
from socketserver import ThreadingMixIn



# This script should be started from website directory (python ../sql.py)

# Alice's password = password1
# Bob's password = password2
# Charlie's password = password3
address = 'localhost:8000'
_dir = '~/Python/backend'
base_dir = '~/Python/backend/test_database.db'

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


verbose(DIR, 2)
verbose(BASE_DIR, 2)
verbose(BASE_DIR_HTTP, 2)



def passCheck(username, password):
    try:
        conn = sqlite3.connect(BASE_DIR)
        conn.row_factory = sqlite3.Row
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
        row = cursor.fetchone()
        user_dict = dict(row)
        verbose(user_dict, 2)
        if ph.verify(user_dict['password'], password) == True:
            return 1
    except VerifyMismatchError:
        return 0
    except Exception as e:
        verbose(f"ERROR | POST | {e}")
        return -1



def d_add(username, password, email):
    conn = sqlite3.connect('test_database.db')
    cursor = conn.cursor()
    password = ph.hash(password)
    cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
                (f"{username}", f"{password}", f"{email}"))
    conn.commit
    conn.close

def d_changePass(username, password):
    conn = sqlite3.connect('test_database.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET password = ? WHERE username = ?", (f"{password}", f"{username}"))
    conn.commit()
    conn.close()

def d_changeEmail(username, email):
    if email.find('@') != -1:
        conn = sqlite3.connect('test_database.db')
        cursor = conn.cursor()
        cursor.execute("UPDATE users SET email = ? WHERE username = ?", (f"{email}", f"{username}"))
        conn.commit()
        conn.close()
    else:
        return -2 # Invalid email (no @ sign)





class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        try:
            if self.path == '/' or self.path == '/ ':
                self.path = '/web/index.html'
            
            if self.path == BASE_DIR_HTTP: # without this it can reveal all hashes, users, emails and etc
                self.path = '/404'

            if self.path == '/sql.py': # name of python script
                self.path = '/404'

            if '..' in self.path:
                self.send_response(404)
                self.end_headers()
                self.wfile.write(b'Not found')
                return
            
            # This is not needed if the script is started in /web/ directory

            # if self.path == '/LICENSE':
            #     self.send_response(404)
            #     self.end_headers()
            #     self.wfile.write(b'Not found')
            #     return
            
            # if self.path.startswith('/.git/'):
            #     self.send_response(404)
            #     self.end_headers()
            #     self.wfile.write(b'Not found')
            #     return

            # if self.path.startswith('/other'):
            #     self.send_response(404)
            #     self.end_headers()
            #     self.wfile.write(b'Not found')
            #     return

            else:
                try:
                    with open(DIR + self.path, 'rb') as f:
                        content = f.read()
                except FileNotFoundError:
                    self.send_response(404)
                    self.end_headers()
                    self.wfile.write(b'Not found')
                    return
        except(IsADirectoryError):
            verbose(f'{self.client_address[0]} tried to access directory', 1)
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b'Not found')
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
                    self.send_response(400, 'Invalid JSON')
                    self.end_headers()
                    return
                
                # Auth check
                result = passCheck(data.get('username'), data.get('password'))
                if result == 0: # если passCheck возвращает 0 то оно передает Failed to authorize с кодом ошибки 401
                    self.send_response(401, 'Failed to authorize')
                    verbose(f'{self.client_address[0]} failed to authorize as {data.get('username')}')
                    self.end_headers()
                    return
                elif result == 1: # если passCheck возвращает 1 то оно передает Successfully authorized с кодом 200
                    self.send_response(200, "Successfully authorized")
                    verbose(f'{self.client_address[0]} succesfully authorized as {data.get('username')}')
                    self.end_headers()
                    return
                else: # если passCheck возвращает -1 то оно передает о том что сервер не смог обработать запрос
                    self.send_response(500, 'Failed to authorize')
                    verbose(f'{self.client_address[0]} tried to authorize as {data.get('username')} but there was an issue with server')
                    self.end_headers()
                    return
            except Exception as e:
                print(f'Unexcepted error | POST | {e}')
                sys.exit(-3)

class ThreadedHTTPServer(ThreadingMixIn, HTTPServer):
    ''''''

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