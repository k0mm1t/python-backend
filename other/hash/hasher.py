from argon2 import PasswordHasher
import sys

try:
    password = sys.argv[1]
except:
    print("No password entered")
    sys.exit(1)
passwordhash = PasswordHasher().hash(password)
print(passwordhash)