from email.policy import default
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
    invites = db.relationship("ChallengeInvite", back_populates="challenge")

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
    is_public = db.Column(db.Boolean, nullable=False)

    answer = db.Column(db.LargeBinary, nullable=True)

    def json(self):
        return {
            "user": {
                "id": self.user_id,
                "pseudo": self.user.pseudo
            },
            "challenge": self.challenge.json(),

            "start_time": int(self.start_time.timestamp()),
            "end_time": int(self.end_time.timestamp()) if self.end_time else None,
            "is_public": self.is_public,

            "data": self.answer.decode("utf-8") if self.answer else None
        }


class ChallengeInvite(db.Model):
    inviter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    invitee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    challenge_id = db.Column(db.Integer, db.ForeignKey("challenge.id"), nullable=False, primary_key=True)

    invite_time = db.Column(db.DateTime, nullable=False)

    invitee = db.relationship("User", foreign_keys=invitee_id, backref=db.backref('challenge_invited'))
    inviter = db.relationship("User", foreign_keys=inviter_id, backref=db.backref('challenge_inviter'))
    challenge = db.relationship("Challenge", foreign_keys=challenge_id, back_populates='invites')

    def json(self):
        return {
            "user_inviter": self.inviter.json_preview(),
            "user_invitee": self.invitee.json_preview(),
            "challenge": self.challenge.json(),
            "invite_date": int(self.invite_time.timestamp())
        }
