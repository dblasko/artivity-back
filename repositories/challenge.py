from datetime import datetime
from app import db
from models import Challenge


class ChallengeRepository:

    def create(self, subject, title, type, end_datetime, timelimit_seconds):
        challenge = Challenge(
            subject=subject, title=title, 
            type=type, start_datetime=datetime.now(),
            end_datetime=end_datetime, timelimit_seconds=timelimit_seconds
        )
        db.session.add(challenge)
        db.session.commit()
        return challenge

    def get(self, challenge_id):
        """
        Get a challenge from its id
        :param challenge_id: the challenge id
        :return: a Challenge instance if it exists, otherwise None
        """
        return Challenge.query.get(challenge_id)

    def update(self, challenge):
        db.session.merge(challenge)
        db.session.commit()
        return challenge
