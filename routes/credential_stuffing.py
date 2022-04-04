from flask import Blueprint, render_template

blueprint = Blueprint('CredentialStuffing', __name__, url_prefix='/credential-stuffing', template_folder='./templates')


@blueprint.route('/')
def credential_stuffing_view():
    return render_template('credential_stuffing.html')
