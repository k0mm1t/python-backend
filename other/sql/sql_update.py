import sqlite3

conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

cursor.execute("UPDATE users SET password = ? WHERE username = ?", ("password1", "Alice"))
conn.commit()
conn.close()