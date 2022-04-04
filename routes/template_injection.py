from flask import Blueprint, render_template, request
from utils import get_source_code

blueprint = Blueprint('template-injection', __name__, template_folder='./templates', url_prefix="/template-injection")


@blueprint.route('/', methods=['POST', 'GET'])
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
            "template_injection.html":
                get_source_code('templates/template_injection.html')
        },
    )
