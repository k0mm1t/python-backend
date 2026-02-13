import sqlite3

conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# Get all users
cursor.execute("SELECT * FROM users")
all_users = cursor.fetchall()
for user in all_users:
    print(user)

# Get specific columns
cursor.execute("SELECT username, email FROM users WHERE password > ?", (25,))
results = cursor.fetchall()

conn.close()