from flask import Blueprint, request, abort, jsonify
from flask_httpauth import HTTPBasicAuth

from auth import auth, generate_token, check_token
from repositories import UserRepository, ChallengeRepository

user_blueprint = Blueprint("users", __name__)


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


@user_blueprint.route("/", methods=('POST',))
def register_user_route():
    body = request.json  # returns 400 if malformed / not json
    fields = {"pseudo", "password", "email"}
    for field in fields:
        if field not in body:
            abort(400)

    user_repo = UserRepository()
    user = user_repo.create(**body)
    if user is None:
        abort(401)

    return jsonify(user.json()), 200


@user_blueprint.route("/<int:user_id>/challenges/invites/received", methods=('GET',))
@auth.login_required()
def user_challenge_invites_received(user_id):
    user_repo = UserRepository()
    user = user_repo.get(user_id)

    if user is None:
        abort(404)

    ch_repo = ChallengeRepository()
    invites = ch_repo.get_pending_challenge_invites(user.id)

    return jsonify(
        [invite.json() for invite in invites]
    )


@user_blueprint.route("/<int:user_id>", methods=('GET',))
@auth.login_required()
def user_public_info_route(user_id):
    user_repo = UserRepository()
    user = user_repo.get(user_id)

    if user is None:
        abort(404)

    ch_repo = ChallengeRepository()

    user_info = user.public_json()
    user_info["challenges_created"] = [ch.json() for ch in ch_repo.get_user_public_created_challenges(user_id)]
    user_info["challenges_answers"] = [ans.json() for ans in ch_repo.get_user_public_challenge_answers(user_id)]

    return jsonify(user_info), 200
