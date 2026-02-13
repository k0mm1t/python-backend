import sqlite3

conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

cursor.execute("DELETE FROM users WHERE username = ?", ("Charlie",))
conn.commit()
conn.close()