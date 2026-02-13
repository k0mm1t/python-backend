from http.server import BaseHTTPRequestHandler, HTTPServer

from argon2.exceptions import VerifyMismatchError
from argon2.exceptions import InvalidHashError
from argon2 import PasswordHasher

import json
import sqlite3
import threading, sys, os
from socketserver import ThreadingMixIn

ph= PasswordHasher()

try:
    password = input('Password=')
    password2 = input('PasswordCheck=')
    passwordhash = ph.hash(password)
    if ph.verify(passwordhash, password2) == True:
        print('Valid pass')
except(VerifyMismatchError):
    print('Invalid pass')
