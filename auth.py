import base64

from flask_httpauth import HTTPTokenAuth
from itsdangerous import Serializer

auth = HTTPTokenAuth("Bearer")
token_serializer = None


def init_auth(app):
    global token_serializer
    token_serializer = Serializer(app.config["SECRET_KEY"])


def generate_token(user_pseudo):
    token = base64.b64encode(token_serializer.dumps({'pseudo': user_pseudo}).encode("utf-8")).decode("utf-8")
    return token


def check_token(token):
    decoded_token = base64.b64decode(token.encode("utf-8")).decode("utf-8")
    try:
        data = token_serializer.loads(decoded_token)
    except:
        return None
    return data


@auth.verify_token
def verify_token(token):
    data = check_token(token)
    if data is None:
        return False

    return data["pseudo"]
