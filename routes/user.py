from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

from auth import auth

user_blueprint = Blueprint("user", __name__)


@user_blueprint.route('/hello')
@auth.login_required()
def hello_user():
    return 'Hello User!'


