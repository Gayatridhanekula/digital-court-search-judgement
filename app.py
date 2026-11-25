
import sqlite3
import os

from flask import Flask, request, render_template_string, abort

app = Flask(__name__)

DB_PATH = os.path.join(os.path.dirname(__file__), "judgments.db")


def get_connection():
    return sqlite3.connect(DB_PATH)


HOME_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Digital Court Judgment Search</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f4f9;
            margin: 0;
            color: #26344a;
        }

        header {
            background: #142b4d;
            color: white;
            text-align: center;
            padding: 30px;
        }

        header h1 {
            margin: 0;
        }

        .container {
            max-width: 1050px;
            margin: 35px auto;
            padding: 25px;
            background: white;
            border-radius: 12px;
        }

        .filters {
            display: grid;
            grid-template-columns: 2fr 1fr 1fr auto;
            gap: 12px;
            margin-top: 20px;
        }

        input, select {
            padding: 12px;
            border: 1px solid #ccc;
            border-radius: 6px;
            width: 100%;
            box-sizing: border-box;
        }

        button, .clear {
            padding: 12px 18px;
            border: none;
            border-radius: 6px;
            background: #1761a0;
            color: white;
            cursor: pointer;
            text-decoration: none;
            text-align: center;
        }

        .clear {
            display: inline-block;
            background: #68778a;
            margin-top: 15px;
        }

        .result {
            background: #f8fafc;
            border: 1px solid #dce3ec;
            border-radius: 8px;
            padding: 18px;
            margin-top: 18px;
        }

        .view {
            display: inline-block;
            background: #1761a0;
            color: white;
            padding: 9px 14px;
            text-decoration: none;
            border-radius: 5px;
        }

        .count {
            background: #e8f1fb;
            padding: 12px;
            border-radius: 6px;
            margin-top: 20px;
        }

        footer {
            text-align: center;
            padding: 25px;
            color: #68778a;
        }

        @media(max-width: 700px) {
            .filters {
                grid-template-columns: 1fr;
            }

            .container {
                margin: 15px;
            }
        }
    </style>
</head>

<body>

<header>
    <h1>Digital Court Judgment Search</h1>
    <p>Search and Explore Court Judgments</p>
</header>

<div class="container">

    <h2>Search Court Judgments</h2>

    <form method="GET" action="/">

        <div class="filters">

            <input
                type="text"
                name="query"
                placeholder="Enter keyword..."
                value="{{ search_query }}"
            >

            <select name="court">
                <option value="">All Courts</option>

                {% for c in courts %}
                <option value="{{ c }}"
                    {% if selected_court == c %}selected{% endif %}>
                    {{ c }}
                </option>
                {% endfor %}

            </select>

            <select name="year">
                <option value="">All Years</option>

                {% for y in years %}
                <option value="{{ y }}"
                    {% if selected_year == y|string %}selected{% endif %}>
                    {{ y }}
                </option>
                {% endfor %}

            </select>

            <button type="submit">Search</button>

        </div>

        <a href="/" class="clear">Clear Search</a>

    </form>

    {% if searched %}

        <div class="count">
            <b>Total matching judgments: {{ results|length }}</b>
        </div>

        {% if results %}

            {% for case in results %}

                <div class="result">

                    <h3>{{ case[1] }}</h3>

                    <p><b>Judgment ID:</b> {{ case[0] }}</p>
                    <p><b>Court:</b> {{ case[2] }}</p>
                    <p><b>Year:</b> {{ case[3] }}</p>
                    <p><b>Legal Issue:</b> {{ case[4] }}</p>
                    <p><b>Status:</b> {{ case[5] }}</p>

                    <a class="view"
                       href="{{ url_for('view_judgment', judgment_id=case[0]) }}">
                       View Full Judgment
                    </a>

                </div>

            {% endfor %}

        {% else %}

            <p>No matching judgments found.</p>

        {% endif %}

    {% endif %}

</div>

<footer>
    Digital Court Judgment Search System
</footer>

</body>
</html>
"""


DETAIL_PAGE = """
<!DOCTYPE html>
<html>
<head>
    <title>Full Judgment Details</title>

    <style>
        body {
            font-family: Arial, sans-serif;
            background: #f1f4f9;
            padding: 25px;
        }

        .container {
            max-width: 850px;
            margin: 30px auto;
            padding: 30px;
            background: white;
            border-radius: 10px;
        }

        h1 {
            color: #142b4d;
        }

        .details {
            line-height: 2;
        }

        .text {
            background: #f4f6f9;
            padding: 20px;
            border-radius: 8px;
            line-height: 1.8;
        }

        a {
            display: inline-block;
            background: #1761a0;
            color: white;
            padding: 10px 16px;
            text-decoration: none;
            border-radius: 5px;
        }
    </style>
</head>

<body>

<div class="container">

    <h1>Full Judgment Details</h1>

    <div class="details">

        <p><b>Judgment ID:</b> {{ case[0] }}</p>
        <p><b>Case Title:</b> {{ case[1] }}</p>
        <p><b>Court:</b> {{ case[2] }}</p>
        <p><b>Year:</b> {{ case[3] }}</p>
        <p><b>Legal Issue:</b> {{ case[4] }}</p>
        <p><b>Keywords:</b> {{ case[5] }}</p>
        <p><b>Status:</b> {{ case[6] }}</p>

    </div>

    <h3>Judgment Text</h3>

    <div class="text">
        {{ case[7] }}
    </div>

    <br><br>

    <a href="/">Back to Search</a>

</div>

</body>
</html>
"""


@app.route("/", methods=["GET"])
def home():

    search_query = request.args.get("query", "").strip().lower()
    selected_court = request.args.get("court", "")
    selected_year = request.args.get("year", "")

    searched = bool(search_query or selected_court or selected_year)

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT DISTINCT court FROM judgments ORDER BY court")
    courts = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DISTINCT year FROM judgments ORDER BY year DESC")
    years = [row[0] for row in cursor.fetchall()]

    sql = """
        SELECT judgment_id, case_title, court, year,
               legal_issue, case_status, judgment_text
        FROM judgments
        WHERE 1=1
    """

    params = []

    if search_query:
        sql += """
            AND (
                LOWER(judgment_id) LIKE ?
                OR LOWER(case_title) LIKE ?
                OR LOWER(court) LIKE ?
                OR CAST(year AS TEXT) LIKE ?
                OR LOWER(legal_issue) LIKE ?
                OR LOWER(keywords) LIKE ?
                OR LOWER(case_status) LIKE ?
                OR LOWER(judgment_text) LIKE ?
            )
        """

        term = "%" + search_query + "%"
        params.extend([term] * 8)

    if selected_court:
        sql += " AND court = ?"
        params.append(selected_court)

    if selected_year:
        sql += " AND year = ?"
        params.append(selected_year)

    sql += " ORDER BY year DESC"

    cursor.execute(sql, params)
    results = cursor.fetchall()

    conn.close()

    return render_template_string(
        HOME_PAGE,
        results=results,
        search_query=search_query,
        selected_court=selected_court,
        selected_year=selected_year,
        courts=courts,
        years=years,
        searched=searched
    )


@app.route("/judgment/<judgment_id>")
def view_judgment(judgment_id):

    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("""
        SELECT judgment_id, case_title, court, year,
               legal_issue, keywords, case_status, judgment_text
        FROM judgments
        WHERE judgment_id = ?
    """, (judgment_id,))

    case = cursor.fetchone()

    conn.close()

    if case is None:
        abort(404)

    return render_template_string(DETAIL_PAGE, case=case)


if __name__ == "__main__":
    app.run(debug=True)
