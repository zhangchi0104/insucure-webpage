from os.path import join as join_path
from flask import Blueprint, render_template

routes = Blueprint('/', __name__, template_folder='templates')


def _get_source_code(path: str, base_dir='demo'):
    fp = join_path(base_dir, path)
    f = open(fp, 'r')
    lines = f.readlines()
    f.close()
    return ''.join(lines)


def _mk_route_struct(name: str, desc):
    route = name.lower().strip().replace(' ', '-')
    template_name = route.replace('-', '_')
    return {
        'name': name,
        'route': route,
        'description': desc,
        'template': f'{template_name}.html',
    }


ROUTE_CONFIG = [
    _mk_route_struct(
        'Credential Stuffing',
        'Attackers collect leaked credentials and use them to access '
        'the user\'s other accounts in case they use the same passwords',
    )
]

for attack in ROUTE_CONFIG:
    routes.add_url_rule(
        f'/{attack["route"]}',
        view_func=lambda: render_template(
            attack['template'],
            source=attack.get('source', None),
        ),
    )


@routes.route('/')
def index():
    return render_template('index.html', attack_types=ROUTE_CONFIG)
