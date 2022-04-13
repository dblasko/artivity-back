
from dotenv import load_dotenv
from flask import Flask
from flask_sqlalchemy import SQLAlchemy

from config import configure
from routes import user_blueprint

load_dotenv()

app = Flask(__name__)
configure(app)
app.register_blueprint(user_blueprint)

db = SQLAlchemy(app)

@app.route('/')
def hello_world():
    return 'Hello World!'


from commands import *
import models


if __name__ == '__main__':
    app.run()
