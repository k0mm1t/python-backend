import sqlite3

conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

cursor.execute("UPDATE users SET password = ? WHERE username = ?", ("$argon2id$v=19$m=65536,t=3,p=4$txt7nb/X6hTvR1f3AeR9Mw$1oLbJOUf/WNZWQSwxaR4VBQuhVDtIV6f4oLU5yTkQvs", "Charlie"))
conn.commit()
conn.close()