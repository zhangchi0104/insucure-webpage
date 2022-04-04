import sqlite3

from flask import request, render_template, Blueprint
from utils import get_source_code


blueprint = Blueprint("sql-injection", __name__, template_folder="./templates", url_prefix="/sql-injection")


@blueprint.route('/')
def sql_injection_view():
    query = request.args.get('query', None)
    if query is not None:
        select_statement = f"SELECT name, description, url FROM sqli_table " + f"WHERE name LIKE '%{query}%';"
        db_conn = sqlite3.connect("./database.sqlite3")
        cursor = db_conn.execute(select_statement)
        results = cursor.fetchall()
    else:
        results = None

    return render_template(
        "sql_injection.html",
        results=results,
        query=query,
        sources={
            "SQL Injection Demo":
            get_source_code('./templates/sql_injection.html', (79, 110)),
            "Flask route for this page":
            get_source_code('./routes/__init__.py', (264, 285))
        },
    )