from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pseudo = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    mdp_hash = db.Column(db.String(256), nullable=False)

    bio = db.Column(db.String(250))
