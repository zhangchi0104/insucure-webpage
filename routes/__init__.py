from flask import Blueprint, render_template

from routes.csrf_attack import blueprint as csrf_attack
from routes.credential_stuffing import blueprint as credential_stuffing
from routes.xss_attack import blueprint as xss_attack
from routes.sql_injection import blueprint as sql_injection
from routes.template_injection import blueprint as template_injection


def register_routes(routes):
    routes.register_blueprint(credential_stuffing)
    routes.register_blueprint(csrf_attack)
    routes.register_blueprint(xss_attack)
    routes.register_blueprint(sql_injection)
    routes.register_blueprint(template_injection)



