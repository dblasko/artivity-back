import random
from datetime import datetime

from flask import Blueprint, jsonify, abort
from flask_httpauth import HTTPBasicAuth

from repositories import ChallengeRepository

auth = HTTPBasicAuth()
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


@challenge_blueprint.route("/<int:id>")
@auth.login_required()
def get_challenge_route(id):
    ch_repo = ChallengeRepository()

    challenge = ch_repo.get(id)
    if challenge is None:
        abort(404)

    return jsonify({
        "challenge": challenge.json()
    })


@auth.verify_password
def verify_passwd(user, passwd):
    return True
