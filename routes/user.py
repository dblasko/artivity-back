from flask import Blueprint, request, abort, jsonify
from flask_httpauth import HTTPBasicAuth

from auth import auth, generate_token, check_token
from repositories import UserRepository

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route('/hello')
@auth.login_required()
def hello_user():
    return 'Hello User!'


@user_blueprint.route("/auth/login", methods=('POST',))
def user_auth_route():
    body = request.json   # returns 400 if malformed / not json
    if "username" not in body or "password" not in body:
        abort(400)

    username = body["username"]
    password = body["password"]

    user_repo = UserRepository()
    user = user_repo.authenticate(username, password)
    if user is None:
        abort(401)

    token = generate_token(user.pseudo)

    return jsonify({
        "token": token
    })
