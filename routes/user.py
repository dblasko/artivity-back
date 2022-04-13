from flask import Blueprint
from flask_httpauth import HTTPBasicAuth

auth = HTTPBasicAuth()
user_blueprint = Blueprint("user", __name__)


@user_blueprint.route('/user')
@auth.login_required()
def hello_user():
    return 'Hello User!'


@auth.verify_password
def verify_passwd(user, passwd):
    return True
