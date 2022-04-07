import sqlite3
from flask import request, render_template, make_response, redirect, Blueprint
from utils import get_source_code

INSECURE_TOKEN = 'insecure-website-token'
blueprint = Blueprint("CSRFAttack",
                      __name__,
                      url_prefix='/csrf-attack',
                      template_folder='./templates')


@blueprint.route('/', methods=['POST', 'GET'])
def csrf_attack_view():
    db_conn = sqlite3.connect("database.sqlite3")
    cursor = db_conn.execute("SELECT username, password from users;")
    users = cursor.fetchall()
    db_conn.close()
    csrf_attacker_url = "https://csrf-attacker.azurewebsites.net"
    sources = {
        "csrf_attack.html Live Demo":
        get_source_code("templates/csrf_attack.html", (103, 178)),
        "Code for Route":
        get_source_code("routes/csrf_attack.py"),
        "CSRF attcker":
        get_source_code("./csrf_attacker.html")
    }
    if request.method == 'GET':
        return render_template(
            "csrf_attack.html",
            users=users,
            csrf_attacker_url=csrf_attacker_url,
            sources=sources,
        )
    else:
        if _check_csrf_form('login', request.form):
            resp = make_response(redirect('/csrf-attack'))
            resp.set_cookie(
                "insecure_website_token",
                INSECURE_TOKEN,
                max_age=3600,
            )
            return resp
        if _check_csrf_form(
                'modify',
                request.form,
                request.cookies.get("insecure_website_token", ""),
        ):
            db_conn = sqlite3.connect("database.sqlite3")
            sql_stmt = "UPDATE users SET password='{}';".format(
                request.form['password'])
            db_conn.execute(sql_stmt)
            db_conn.commit()
            print("successfully PWNed database")
            db_conn.close()
    return render_template(
        "csrf_attack.html",
        csrf_attacker_url=csrf_attacker_url,
        sources=sources,
        users=users,
    )


def _check_csrf_form(action, form: dict, token=""):
    if action == "login":
        return form.get(
            "username",
            "",
        ) == "admin" and form.get(
            "password", "") == "admin" and form.get("action") == "login"
    if action == "modify":
        return token == INSECURE_TOKEN and form["password"] != ""
    return False
