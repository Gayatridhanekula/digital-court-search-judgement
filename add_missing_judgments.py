
import sqlite3

conn = sqlite3.connect("judgments.db")
cursor = conn.cursor()

new_judgments = [
    (
        "J006",
        "Sample Criminal Case",
        "High Court",
        2023,
        "Criminal Case",
        "criminal theft fraud investigation",
        "Decided",
        "Sample record about criminal law and investigation"
    ),
    (
        "J007",
        "Sample Divorce Case",
        "Family Court",
        2022,
        "Divorce Case",
        "divorce marriage family separation",
        "Decided",
        "Sample record about divorce and family matters"
    ),
    (
        "J008",
        "Sample Civil Case",
        "District Court",
        2024,
        "Civil Case",
        "civil dispute compensation rights",
        "Pending",
        "Sample record about civil disputes"
    )
]

cursor.executemany("""
    INSERT OR IGNORE INTO judgments
    (judgment_id, case_title, court, year,
     legal_issue, keywords, case_status, judgment_text)
    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
""", new_judgments)

conn.commit()
conn.close()

print("Three new judgments added successfully!")
print("Criminal, Divorce and Civil cases are ready.")
