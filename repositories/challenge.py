import random
from datetime import datetime

from sqlalchemy import func

from app import db
from models import Challenge


class ChallengeRepository:

    def create(self, subject, title, type, start_datetime, end_datetime, timelimit_seconds, user_created):
        challenge = Challenge(
            subject=subject, title=title, 
            type=type, start_datetime=start_datetime,
            end_datetime=end_datetime, timelimit_seconds=timelimit_seconds,
            user_created=user_created
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

    def pick_random(self):
        max_id = db.session.query(func.max(Challenge.id)).scalar()

        selected_challenge = None
        while selected_challenge is None:
            selected_id = random.randint(0, max_id)
            selected_challenge = self.get(selected_id)

        return selected_challenge

    def update(self, challenge):
        db.session.merge(challenge)
        db.session.commit()
        return challenge
