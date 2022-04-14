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
    subject = db.Column(db.String(320), nullable=False)
    title = db.Column(db.String(50), nullable=False)
    type = db.Column(db.Enum(ChallengeType), nullable=False)
    start_datetime = db.Column(db.DateTime, nullable=False)
    end_datetime = db.Column(db.DateTime, nullable=True)
    timelimit_seconds = db.Column(db.Integer, nullable=True)

    user_created_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False)
    user_created = db.relationship("User", back_populates="challenges_created")

    user_answers = db.relationship("ChallengeAnswer", back_populates="challenge")

    def json(self):
        return {
            "id": self.id,
            "title": self.title,
            "subject": self.subject,
            "type": self.type.name,
            "start": int(self.start_datetime.timestamp()),
            "end": int(self.end_datetime.timestamp()) if self.end_datetime else None,
            "timelimit": self.timelimit_seconds if self.timelimit_seconds else None,
            "user_created": {
                "id": self.user_created_id,
                "pseudo": self.user_created.pseudo
            }
        }


class ChallengeAnswer(db.Model):
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenge.id"), nullable=False, primary_key=True)

    user = db.relationship("User", back_populates="challenges_answers")
    challenge = db.relationship("Challenge", back_populates="user_answers")

    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=True)
    is_public = db.Column(db.Boolean, nullable=True)

    answer = db.Column(db.LargeBinary, nullable=True)

