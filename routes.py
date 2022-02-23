from flask import Blueprint, render_template

routes = Blueprint('/', __name__, template_folder='templates')


@routes.route('/')
def index():
    return render_template('index.html')
