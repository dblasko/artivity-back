import random
from datetime import datetime

from flask import Blueprint, jsonify, abort, request, Response
from flask_httpauth import HTTPBasicAuth

from auth import auth
from repositories import ChallengeRepository, UserRepository

challenge_blueprint = Blueprint("challenge", __name__)

daily_challenge = None


@challenge_blueprint.route('/daily')
@auth.login_required()
def daily_challenge_route():
    ch_repo = ChallengeRepository()

    timestamp = int(datetime.today().timestamp()) // (24 * 3600)
    random.seed(timestamp)
    challenge = ch_repo.pick_random()

    return jsonify({
        "challenge": challenge.json()
    })


@challenge_blueprint.route("/<int:challenge_id>")
@auth.login_required()
def get_challenge_route(challenge_id):
    ch_repo = ChallengeRepository()

    challenge = ch_repo.get(challenge_id)
    if challenge is None:
        abort(404)

    return jsonify({
        "challenge": challenge.json()
    })


@challenge_blueprint.route("/<int:challenge_id>/submit", methods=("POST",))
@auth.login_required()
def submit_challenge_answer_route(challenge_id):
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if user is None:
        abort(401)

    ch_repo = ChallengeRepository()
    challenge = ch_repo.get(challenge_id)
    challenge_answer = ch_repo.get_answer(user.id, challenge_id)

    print(challenge)
    print(challenge_answer)
    print(user)

    if challenge is None:
        abort(404)
    if challenge_answer is None or challenge_answer.end_time is not None:
        abort(403)

    data = request.json
    if "data" not in data:
        abort(400)

    answer_data = data["data"]
    ans_bytes = answer_data.encode("utf-8")

    challenge_answer.end_time = datetime.now()
    challenge_answer.answer = ans_bytes
    ch_repo.update_answer(challenge_answer)

    return challenge_answer.json()



@auth.verify_password
def verify_passwd(user, passwd):
    return True
