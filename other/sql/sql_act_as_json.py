import sqlite3
import sys

conn = sqlite3.connect('test_database.db')
conn.row_factory = sqlite3.Row  # This magic line makes rows behave like dicts!
cursor = conn.cursor()

username = sys.argv[1]

cursor.execute("SELECT * FROM users WHERE username = ?", (username,))
row = cursor.fetchone()

# Convert to dict
user_dict = dict(row)
print(user_dict)
# {'id': 1, 'username': 'Alice', 'password': 25, 'email': 'alice@email.com'}