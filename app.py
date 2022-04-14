from dotenv import load_dotenv
from flask import Flask
from flask_httpauth import HTTPBasicAuth
from flask_sqlalchemy import SQLAlchemy

from config import configure

load_dotenv()

app = Flask(__name__)
configure(app)

db = SQLAlchemy(app)

from routes import user_blueprint
from routes import challenge_blueprint

app.register_blueprint(user_blueprint, url_prefix="/api/user")
app.register_blueprint(challenge_blueprint, url_prefix="/api/challenge")


@app.route('/')
def hello_world():
    return 'Hello World!'


from commands import *

if __name__ == '__main__':
    app.run()
