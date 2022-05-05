from flask import Blueprint, request, abort, jsonify
from flask_httpauth import HTTPBasicAuth

from auth import auth, generate_token, check_token
from repositories import UserRepository, ChallengeRepository

user_blueprint = Blueprint("users", __name__)


@user_blueprint.route("/auth/login", methods=('POST',))
def user_auth_route():
    body = request.json  # returns 400 if malformed / not json
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


@user_blueprint.route("/challenges/invites/received", methods=('GET',))
@auth.login_required()
def user_challenge_invites_received():
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())

    if user is None:
        abort(404)

    ch_repo = ChallengeRepository()
    invites = ch_repo.get_pending_challenge_invites(user.id)

    return jsonify({
        "count": len(invites),
        "invites":
        [invite.json() for invite in invites]
    }), 200


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


@user_blueprint.route("/friends", methods=("GET",))
@auth.login_required()
def user_get_friends():
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if user is None:
        abort(401)

    return jsonify([friend.json() for friend in user.friends]), 200


@user_blueprint.route("/friends", methods=("PUT",))
@auth.login_required()
def user_add_friend():
    # Get current user
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if user is None:
        abort(401)
    # Get user to be added
    data = request.json
    if "id" not in data:
        abort(400)

    friend_id = data["id"]
    friend = user_repo.get(friend_id)

    if friend_id == user.id:
        abort(400)

    if friend not in user.friends:
        user.friends.append(friend)
        friend.friends.append(user)

    user_repo.update(friend)
    user_repo.update(user)

    return jsonify([friend.json() for friend in user.friends]), 200


@user_blueprint.route("/friends", methods=("DELETE",))
@auth.login_required()
def user_remove_friend():
    # Get current user
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if user is None:
        abort(401)
    # Get user to be added
    data = request.json
    if "id" not in data:
        abort(400)

    friend_id = data["id"]
    if friend_id == user.id:
        abort(400)
    friend = user_repo.get(friend_id)

    if friend in user.friends:
        user.friends.remove(friend)
        friend.friends.remove(user)

    user_repo.update(friend)
    user_repo.update(user)

    return jsonify([friend.json() for friend in user.friends]), 200

@user_blueprint.route("/search", methods=("GET",))
@auth.login_required()
def user_search():
    data = request.json
    if "query" not in data:
        abort(400)

    query = data["query"]
    user_repo = UserRepository()
    search = user_repo.search(query)

    return jsonify([u.json() for u in search]), 200


@user_blueprint.route("/gallery", methods=("GET",))
@auth.login_required()
def get_user_gallery_route():
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if user is None:
        abort(404)

    ch_repo = ChallengeRepository()
    answers = ch_repo.get_all_user_answers(user.id)

    return jsonify(
        [ans.json(no_challenge=False) for ans in answers]
    )

