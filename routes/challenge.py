import random
from datetime import datetime

from flask import Blueprint, jsonify, abort, request

from auth import auth
from models import get_challenge_type
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

    challenge.user_answers_count += 1
    ch_repo.update(challenge)

    return challenge_answer.json()


@challenge_blueprint.route("/<int:challenge_id>/start", methods=('POST',))
@auth.login_required()
def start_challenge(challenge_id):
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if user is None:
        abort(401)

    ch_repo = ChallengeRepository()
    challenge = ch_repo.start_challenge(challenge_id, user.id, False)
    if challenge is None:
        abort(404)

    return jsonify({
        "challenge": challenge.json()
    }), 200


@challenge_blueprint.route("", methods=("POST",))
@auth.login_required()
def create_challenge_route():
    body = request.json  # returns 400 if malformed / not json
    print(body)
    fields = {"subject", "title", "type", "start", "end", "timelimit", "creator_id"}
    for field in fields:
        if field not in body:
            abort(400)

    start = body["start"] if body["start"] is not None else datetime.now()
    try:
        ch_type = get_challenge_type(body["type"])
    except KeyError:
        abort(400)

    creator_id = body["creator_id"]

    user_repo = UserRepository()
    creator = user_repo.get(creator_id)
    if creator is None:
        abort(404)

    ch_repo = ChallengeRepository()
    challenge = ch_repo.create(subject=body["subject"],
                               title=body["title"],
                               type=ch_type,
                               start_datetime=start,
                               end_datetime=body["end"],
                               timelimit_seconds=body["timelimit"],
                               user_created=creator
                               )

    return jsonify(challenge.json()), 200
