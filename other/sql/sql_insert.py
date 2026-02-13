import sqlite3

conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# Insert single record
cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
               ("Alice", "password1", "alice@email.com"))

# Insert multiple records
users = [
    ("Bob", "password2", "bob@email.com"),
    ("Charlie", "password3", "charlie@email.com")
]
cursor.executemany("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", users)

conn.commit()
conn.close()