from app import db 

import enum
class ChallengeType(enum.Enum):
    text=1
    video = 2
    drawing = 3
    sound = 4
    photo = 5

class Challenge(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    subject = db.Column(db.String(50), nullable=False)
    title = db.Column(db.String(320), nullable=False)
    type = db.Column(enum.Enum(ChallengeType), nullable=False)
    start_datetime = db.Column(db.Time, nullable=False)    
    end_datetime = db.Column(db.Time, nullable=True)
    timelimit_seconds = db.Column(db.Integer, nullable=True)