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

    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if not challenge.is_public and challenge.user_created_id != user.id and not ch_repo.was_invited(user.id, challenge_id):
        abort(403)

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
    challenge_ans = ch_repo.start_challenge(challenge_id, user.id, False)
    if challenge_ans is None:
        abort(404)

    challenge = challenge_ans.challenge
    if challenge.is_collab and challenge.whos_turn_id != user.id:
        abort(403)

    if not challenge.is_public and challenge.user_created_id != user.id and not ch_repo.was_invited(user.id, challenge_id):
        abort(403)

    return jsonify({
        "challenge": challenge_ans.json()
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
                               ch_type=ch_type,
                               start_datetime=start,
                               end_datetime=body["end"],
                               timelimit_seconds=body["timelimit"],
                               user_created=creator
                               )

    return jsonify(challenge.json()), 200


@challenge_blueprint.route("/<int:challenge_id>/possible_next_users", methods=("GET",))
@auth.login_required()
def get_collaborative_challenge_available_next_users_route(challenge_id):
    # check challenge exists and collaborative (and not public)
    ch_repo = ChallengeRepository()
    challenge = ch_repo.get(challenge_id)
    if challenge is None or not challenge.is_collab or challenge.is_public:  # collaborative challenges can't be public
        abort(404)

    # check user has access (was invited)
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if not ch_repo.was_invited(user.id, challenge_id) and challenge.user_created_id != user.id:
        abort(403)

    # query repository
    users = ch_repo.collab_get_available_next_users(challenge_id)
    return jsonify(
        [user.json_preview() for user in users]
    ), 200


@challenge_blueprint.route("/<int:challenge_id>/set_next", methods=("POST",))
@auth.login_required()
def set_collab_challenge_next_user_route(challenge_id):
    # check challenge exists and collaborative (and not public)
    ch_repo = ChallengeRepository()
    challenge = ch_repo.get(challenge_id)
    if challenge is None or not challenge.is_collab or challenge.is_public:  # collaborative challenges can't be public
        abort(404)

    # check user has access (is whos_turn user)
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if user.id != challenge.whos_turn_id:
        abort(403)

    # user must have completed its answer (end_time is set)
    answer = ch_repo.get_answer(user.id, challenge_id)
    if answer is None or answer.end_time is None:
        abort(403)

    # designated user must be in available list
    body = request.json
    if "user_id" not in body:
        abort(400)

    designated_user = user_repo.get(body["user_id"])
    available_users = ch_repo.collab_get_available_next_users(challenge_id)
    if designated_user not in available_users:
        abort(403)

    # update challenge
    challenge.whos_turn = designated_user
    ch_repo.update(challenge)

    return jsonify(challenge.json()), 200


@challenge_blueprint.route("/<int:challenge_id>/invite", methods=("PUT",))
@auth.login_required()
def invite_to_challenge_route(challenge_id):
    # check challenge exists
    ch_repo = ChallengeRepository()
    challenge = ch_repo.get(challenge_id)
    if challenge is None:
        abort(404)

    # if challenge private, check user has access to challenge
    user_repo = UserRepository()
    user = user_repo.get_by_pseudo(auth.current_user())
    if not challenge.is_public and challenge.user_created_id != user.id and not ch_repo.was_invited(user.id, challenge_id):
        abort(403)

    # create invite
    body = request.json
    if "user_id" not in body:
        abort(400)

    user_invited = user_repo.get(body["user_id"])
    if user_invited is None:
        abort(404)

    invite = ch_repo.get_invite(user.id, user_invited.id, challenge_id)
    if invite is None:
        invite = ch_repo.create_invite(user.id, user_invited.id, challenge_id)

    return jsonify(invite.json()), 200


@challenge_blueprint.route("/<int:challenge_id>/answers")
@auth.login_required()
def get_challenge_answers_route(challenge_id):
    ch_repo = ChallengeRepository()
    challenge = ch_repo.get(challenge_id)
    if challenge is None:
        abort(404)

    answers = ch_repo.get_public_challenge_answers(challenge_id)

    return jsonify({
        "count": len(answers),
        "challenge": challenge.json(),
        "answers": [answer.json(no_challenge=True) for answer in answers]
    }), 200


@challenge_blueprint.route("/selection")
@auth.login_required()
def get_today_challenge_selection_route():
    ch_repo = ChallengeRepository()

    timestamp = int(datetime.today().timestamp()) // (24 * 3600)
    random.seed(timestamp)
    challenges = ch_repo.pick_n_random(6)

    return jsonify(
        [challenge.json() for challenge in challenges]
    ), 200

