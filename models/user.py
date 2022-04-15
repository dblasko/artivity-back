from app import db


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pseudo = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    bio = db.Column(db.String(250))

    challenges_answers = db.relationship("ChallengeAnswer", back_populates="user", lazy=True)
    challenges_created = db.relationship("Challenge", back_populates="user_created", lazy=True)

    def json_preview(self):
        return {
            "id": self.id,
            "pseudo": self.pseudo
        }
