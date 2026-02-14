import sqlite3

conn = sqlite3.connect('test_database.db')
cursor = conn.cursor()

# Insert single record
cursor.execute("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", 
               ("Alice", "$argon2id$v=19$m=65536,t=3,p=4$Iqg3P/TzGDSHg0IOO18d3A$EFQgYAZSHK5vWVkLWS921KhWC+cFHlPoYQF7xRbuTuk", "alice@example.com"))

# Insert multiple records
users = [
    ("Bob", "$argon2id$v=19$m=65536,t=3,p=4$F7432qgG5nCKPtnoyGKS2w$tv/jVjPpZwlpyhF4tLD7vMIJvTbhvQsh+lWYSt9SseI", "bob@example.com"),
    ("Charlie", "$argon2id$v=19$m=65536,t=3,p=4$txt7nb/X6hTvR1f3AeR9Mw$1oLbJOUf/WNZWQSwxaR4VBQuhVDtIV6f4oLU5yTkQvs", "charlie@example.com")
]
cursor.executemany("INSERT INTO users (username, password, email) VALUES (?, ?, ?)", users)

conn.commit()
conn.close()