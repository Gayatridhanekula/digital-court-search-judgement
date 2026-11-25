
import sqlite3

conn = sqlite3.connect("judgments.db")
cursor = conn.cursor()

cursor.execute("PRAGMA table_info(judgments)")

columns = cursor.fetchall()

print("DATABASE TABLE COLUMNS:")

for column in columns:
    print(column)

conn.close()

import sqlite3

conn = sqlite3.connect("judgments.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM judgments")

records = cursor.fetchall()

print("\nALL STORED JUDGMENTS:")

for record in records:
    print(record)

conn.close()

