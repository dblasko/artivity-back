from flask import Blueprint

user_blueprint = Blueprint("user", __name__)

@user_blueprint.route('/user')
def hello_user():
    return 'Hello User!'
