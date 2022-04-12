from dotenv import load_dotenv
from flask import Flask
from routes import user_blueprint

load_dotenv()

app = Flask(__name__)
app.register_blueprint(user_blueprint)

@app.route('/')
def hello_world():
    return 'Hello World!'


if __name__ == '__main__':
    app.run()
