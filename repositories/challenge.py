import random
from datetime import datetime

from sqlalchemy import func, null

from app import db
from models import Challenge, ChallengeAnswer


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

    def get_all_pending_challenges(self, user_id):
        """
        Get all challenges to which a user is invited (not yet answered)
        :param user_id: the invited user's id
        :return: a list of challenges if there are any, otherwise None
        """
        return Challenge.query.filter(user_invitee=user_id) #i am STILL unsure of this


    def update(self, challenge):
        db.session.merge(challenge)
        db.session.commit()
        return challenge

    def get_answer(self, user_id, challenge_id):
        return ChallengeAnswer.query.filter_by(user_id=user_id, challenge_id=challenge_id).first()

    def update_answer(self, challenge_answer):
        db.session.merge(challenge_answer)
        db.session.commit()
        return challenge_answer

