from app import db 

import enum
class ChallengeType(enum.Enum):
    text = 1
    video = 2
    drawing = 3
    sound = 4
    photo = 5


class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(320), nullable=False)
    type = db.Column(db.Enum(ChallengeType), nullable=False)
    start_datetime = db.Column(db.Time, nullable=False)
    end_datetime = db.Column(db.Time, nullable=True)
    timelimit_seconds = db.Column(db.Integer, nullable=True)

    user_created_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_created = db.relationship("User", back_populates="challenges_created")

    user_answers = db.relationship("ChallengeAnswer", back_populates="challenge")


class ChallengeAnswer(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenge.id"), nullable=False, primary_key=True)

    user = db.relationship("User", back_populates="challenges_answers")
    challenge = db.relationship("Challenge", back_populates="user_answers")

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    is_public = db.Column(db.Boolean, nullable=False)

    answer = db.Column(db.LargeBinary, nullable=True)

