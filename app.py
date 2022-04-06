# Author: Chi Zhang z5211214
# Date: 22/02/2022

from flask import Flask, render_template
from utils import init_db, mk_route_struct
from routes import register_routes

app = Flask(__name__)
register_routes(app)

ROUTE_CONFIG = {
    **mk_route_struct(
        'Credential Stuffing',
        'Attackers collect leaked credentials and use them to access '
        'the user\'s other accounts in case they use the same passwords',
    ),
    **mk_route_struct(
        'Template Injection',
        'If the the website uses template to render content, '
        'attackers can inject code wchich will be executed on the server.',
    ),
    **mk_route_struct(
        'XSS Attack',
        'Attackers can send a web app malicious code, which allows '
        'the attacker gain access to sensitive information',
    ),
    **mk_route_struct(
        'CSRF Attack',
        'Attackers force anthenticated users to send unwanted request'
        'to web applications',
    ),
    **mk_route_struct(
        'SQL Injection',
        "Attackers access the database by injecting SQL statements into"
        "a vulnerable input field",
    )
}


@app.route('/')
def index():
    return render_template('index.html', attack_types=ROUTE_CONFIG.values())


if __name__ == '__main__':
    init_db()
    print(app.url_map)
    app.run("0.0.0.0", debug=True)
