import sqlite3

conn = sqlite3.connect('config.db')
cursor = conn.cursor()

# Create table
cursor.execute('''
    CREATE TABLE IF NOT EXISTS users (
        address TEXT NOT NULL,
        dir TEXT NOT NULL,
        base_dir TEXT NOT NULL,
        email TEXT UNIQUE
    )
''')

conn.commit()
conn.close()