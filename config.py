import os

DB_HOST = os.environ.get("DB_HOST")
DB_PORT = os.environ.get("DB_PORT")
DB_USER = os.environ.get("DB_USER")
DB_PASS = os.environ.get("DB_PASS")
DB_NAME = os.environ.get("DB_NAME")


def configure(app):
    # SQLAlchemy
    app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql://{0}:{1}@{2}:{3}/{4}".format(DB_USER, DB_PASS, DB_HOST,
                                                                                      str(DB_PORT), DB_NAME)
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
