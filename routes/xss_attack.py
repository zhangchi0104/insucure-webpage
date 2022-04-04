import sqlite3

from flask import request, render_template, Blueprint
from utils import get_source_code

blueprint = Blueprint('xss_attack', __name__, template_folder='./templates', url_prefix='/xss-attack')


@blueprint.route('/', methods=['POST', 'GET', 'DELETE'])
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
    return render_template(
        'xss_attack.html',
        query=query,
        posts=posts,
        sources={
            "Flask Route":
            get_source_code('./routes/xss_attack.py'),
            "Live Demo Code":
            get_source_code('./templates/xss_attack.html', (88, 134))
        },
    )