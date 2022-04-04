from os.path import join as join_path
from os import getenv
import sqlite3
from flask import Blueprint, render_template
from flask import request, make_response, redirect

USERS = ['admin', 'test']
SEARCH_RESULTS = (
    ('Twitter', 'twitter', 'https://twitter.com'),
    ('Google', 'google', 'https://google.com.au'),
    ('Apple', 'apple website', 'https://apple.com.au'),
)
INSECURE_TOKEN = 'insecure-website-token'

routes = Blueprint('/', __name__, template_folder='templates')

db_conn = sqlite3.connect('./database.sqlite3')
db_conn.execute("""CREATE TABLE IF NOT EXISTS xss_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post TEXT NOT NULL);""")
db_conn.commit()
db_conn.close()

db_conn = sqlite3.connect('./database.sqlite3')
db_conn.execute("""CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                username TEXT NOT NULL,
                password TEXT NOT NULL);""")
db_conn.commit()
db_conn.close()

db_conn = sqlite3.connect('./database.sqlite3')
cursor = db_conn.execute("SELECT count(*) from users;")
res = cursor.fetchall()

if res[0][0] == 0:
    for user in USERS:
        db_conn.execute(
            "INSERT INTO users (username, password) VALUES (?, ?);",
            (user, "password"),
        )
    db_conn.commit()
else:
    db_conn.execute("UPDATE users SET password='password';")
    db_conn.commit()
db_conn.close()

# create simple table for query results
db_conn = sqlite3.connect("./database.sqlite3")
db_conn.execute("""CREATE TABLE IF NOT EXISTS sqli_table (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    url TEXT NOT NULL,
    name TEXT NOT NULL,
    description TEXT NOT NULL);""")
db_conn.commit()
db_conn.execute("DELETE from sqli_table;")
db_conn.commit()

for result in SEARCH_RESULTS:
    db_conn.execute(
        "INSERT INTO sqli_table (name, description, url) VALUES (?, ?, ?);",
        result,
    )
db_conn.commit()
db_conn.close()


def _get_source_code(path: str, _range=None):
    fp = join_path(path)
    f = open(fp, 'r')
    lines = f.readlines()
    f.close()
    if _range is None:
        return ''.join(lines)
    else:
        if len(_range) != 2:
            raise ValueError(f"expect _range to be 2, got {len(_range)}")
        # make range inclusive
        lo = _range[0] - 1
        hi = _range[1] + 1
        return ''.join(lines[lo:hi])


def _mk_route_struct(name: str, desc, **kwargs):
    route = name.lower().strip().replace(' ', '-')
    template_name = route.replace('-', '_')
    return {
        route: {
            'name': name,
            'route': route,
            'description': desc,
            'template': f'{template_name}.html',
            'variables': {
                **kwargs
            },
        }
    }


ROUTE_CONFIG = {
    **_mk_route_struct(
        'Credential Stuffing',
        'Attackers collect leaked credentials and use them to access '
        'the user\'s other accounts in case they use the same passwords',
    ),
    **_mk_route_struct(
        'Template Injection',
        'If the the website uses template to render content, '
        'attackers can inject code wchich will be executed on the server.',
    ),
    **_mk_route_struct(
        'XSS Attack',
        'Attackers can send a web app malicious code, which allows '
        'the attacker gain access to sensitive information',
    ),
    **_mk_route_struct(
        'CSRF Attack',
        'Attackers force anthenticated users to send unwanted request'
        'to web applications',
    ),
    **_mk_route_struct(
        'SQL Injection',
        "Attackers access the database by injecting SQL statements into"
        "a vulnerable input field",
    )
}


@routes.route('/')
def index():
    return render_template('index.html', attack_types=ROUTE_CONFIG.values())


@routes.route('/credential-stuffing')
def detail_page():
    route = ROUTE_CONFIG['credential-stuffing']
    return render_template(route['template'], **route['variables'])


@routes.route('/template-injection', methods=['POST', 'GET'])
def template_injection_view():
    posts = []
    query = request.args.get('query', '')
    print(posts)
    if request.method == 'DELETE':
        posts = []
    elif request.method == 'POST':
        content = request.form['content']
        posts.append(content)
    return render_template(
        'template_injection.html',
        posts=posts,
        query=query,
        sources={
            "template_injection.html.jinja":
            (_get_source_code('templates/template_injection.html'), 'html'),
        },
    )


@routes.route('/xss-attack', methods=['POST', 'GET', 'DELETE'])
def xss_attack_view():
    db_conn = sqlite3.connect('./database.sqlite3')
    if request.method == "POST":
        db_conn.execute("INSERT INTO xss_posts (post) VALUES (?);",
                        (request.form["post"], ))
        db_conn.commit()
    if request.method == "DELETE":
        db_conn.execute("DELETE FROM xss_posts")
        db_conn.commit()
    posts = [row[0] for row in db_conn.execute("SELECT post from xss_posts")]
    db_conn.close()
    query = request.args.get('query', '')
    return render_template('xss_attack.html', query=query, posts=posts)


###########################
#                         #
#       CSRF ATTACK       #
#                         #
###########################


@routes.route('/csrf-attack', methods=['POST', 'GET'])
def csrf_attack_view():
    db_conn = sqlite3.connect("database.sqlite3")
    cursor = db_conn.execute("SELECT username, password from users;")
    users = cursor.fetchall()
    db_conn.close()
    csrf_attacker_url = getenv("CSRF_ATTACKER_URL", "")
    sources = {
        "csrf_attack.html Live Demo":
        (_get_source_code("templates/csrf_attack.html", (103, 178)), 'html'),
        "Code for Route": (_get_source_code("routes/__init__.py",
                                            (149, 197)), 'python'),
        "CSRF attcker": (_get_source_code("./csrf_attacker.html"), 'html')
    }
    print(len(sources))
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


#############################
#                           #
#       SQL INJECTION       #
#                           #
#############################


@routes.route('/sql-injection')
def sql_injection_view():
    query = request.args.get('query', None)
    if query is not None:
        select_statement = f"SELECT name, description, url FROM sqli_table " + f"WHERE name LIKE '%{query}%';"
        print(select_statement)
        db_conn = sqlite3.connect("./database.sqlite3")
        cursor = db_conn.execute(select_statement)
        results = cursor.fetchall()
        print(results)
    else:
        results = None

    return render_template("sql_injection.html", results=results, query=query)
