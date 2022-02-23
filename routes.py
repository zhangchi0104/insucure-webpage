from flask import Blueprint, render_template

routes = Blueprint('/', __name__, template_folder='templates')


def _mk_attack_struct(name: str, desc):
    route = name.lower().strip().replace(' ', '-')
    return {
        'name': name,
        'route': route,
        'description': desc,
        'template': f'{route}.html'
    }


ATTACKS = [
    _mk_attack_struct(
        'Crendential Stuffing',
        'Attackers collect leaked credentials and use them to access '
        'the user\'s other accounts in case they use the same passwords',
    )
]


@routes.route('/')
def index():
    return render_template('index.html', attack_types=ATTACKS)
