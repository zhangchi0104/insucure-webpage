from os.path import join as join_path
from flask import Blueprint, render_template
from flask import request
from flask.templating import render_template_string

routes = Blueprint('/', __name__, template_folder='templates')


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
        'Template Injection', 'If the the website uses template to render content, '
        'attackers can inject code wchich will be executed on the server.'),
}


@routes.route('/')
def index():
    return render_template('index.html', attack_types=ROUTE_CONFIG.values())


@routes.route('/credential-stuffing')
def detail_page():
    route = ROUTE_CONFIG['credential-stuffing']
    return render_template(route['template'], **route['variables'])


@routes.route('/template-injection', methods=['POST', 'GET', 'DELETE'])
def template_injection_view():
    posts = []
    print(posts)
    if request.method == 'DELETE':
        posts = []
    elif request.method == 'POST':
        content = request.form['content']
        posts.append(content)
    return render_template('template_injection.html', posts=posts)
