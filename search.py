
import sqlite3

DB_NAME = "judgments.db"


def search_judgments():

    print("DIGITAL COURT JUDGMENT SEARCH")
    print("-----------------------------")

    user_query = input("Enter your legal search query: ").strip().lower()

    if not user_query:
        print("Please enter a search query.")
        return

    try:
        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()

        query = """
        SELECT judgment_id, case_title, court, year,
               legal_issue, case_status, judgment_text
        FROM judgments
        WHERE LOWER(judgment_id) LIKE ?
        OR LOWER(case_title) LIKE ?
        OR LOWER(court) LIKE ?
        OR CAST(year AS TEXT) LIKE ?
        OR LOWER(legal_issue) LIKE ?
        OR LOWER(keywords) LIKE ?
        OR LOWER(case_status) LIKE ?
        OR LOWER(judgment_text) LIKE ?
        """

        search_term = "%" + user_query + "%"

        cursor.execute(query, (search_term,) * 8)

        results = cursor.fetchall()

        if results:
            print("\nSearch Results:\n")

            for row in results:
                print("Judgment ID:", row[0])
                print("Case Title:", row[1])
                print("Court:", row[2])
                print("Year:", row[3])
                print("Legal Issue:", row[4])
                print("Status:", row[5])
                print("Judgment Text:", row[6])
                print("-----------------------------")

        else:
            print("\nNo matching judgments found.")

        conn.close()

    except sqlite3.Error as error:
        print("Database Error:", error)


if __name__ == "__main__":
    search_judgments()


