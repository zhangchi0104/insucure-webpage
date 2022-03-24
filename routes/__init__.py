from os.path import join as join_path
import sqlite3
from flask import Blueprint, render_template
from flask import request

routes = Blueprint('/', __name__, template_folder='templates')

db_conn = sqlite3.connect('./databse.sqlite3')
db_conn.execute("""CREATE TABLE IF NOT EXISTS xss_posts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                post TEXT NOT NULL);""")
db_conn.commit()
db_conn.close()


def _get_source_code(path: str):
    fp = join_path(path)
    f = open(fp, 'r')
    lines = f.readlines()
    f.close()
    return ''.join(lines)


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
        ''
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
        source={
            "template_injection.html.jinja":
            _get_source_code('templates/template_injection.html')
        },
    )


@routes.route('/xss-attack', methods=['POST', 'GET', 'DELETE'])
def xss_attack_view():
    db_conn = sqlite3.connect('./databse.sqlite3')
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

@routes.route('/csrf-attack', methods = ['POST', 'GET'])
def csrf_attack_view():
    pass

