import random
from datetime import datetime

from sqlalchemy import func, null

from app import db
from models import Challenge, ChallengeAnswer, ChallengeInvite


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

    def create_invite(self, inviter_user_id, invitee_user_id, challenge_id):
        challenge_invite = ChallengeInvite(
            inviter_id=inviter_user_id,
            invitee_id=invitee_user_id,
            challenge_id=challenge_id,
            invite_time=datetime.now()
        )
        db.session.add(challenge_invite)
        db.session.commit()
        return challenge_invite

    def get(self, challenge_id):
        """
        Get a challenge from its id
        :param challenge_id: the challenge id
        :return: a Challenge instance if it exists, otherwise None
        """
        return Challenge.query.get(challenge_id)

    def get_invite(self, inviter_user_id, invitee_user_id, challenge_id):
        """
        Get a challenge invite from its challenge id, inviter id and invitee id
        :return: a ChallengeInvite instance if it exists, otherwise None
        """
        invite = ChallengeInvite.query.filter_by(
            inviter_id=inviter_user_id, invitee_id=invitee_user_id, challenge_id=challenge_id
        ).first()
        return invite

    def pick_random(self):
        max_id = db.session.query(func.max(Challenge.id)).scalar()

        selected_challenge = None
        while selected_challenge is None:
            selected_id = random.randint(0, max_id)
            selected_challenge = self.get(selected_id)

        return selected_challenge

    def get_pending_challenge_invites(self, user_id):
        """
        Get all challenges to which a user is invited (not yet answered)
        :param user_id: the invited user's id
        :return: a list of challenges if there are any, otherwise None
        """
        # todo remove completed invites
        return ChallengeInvite.query.filter_by(invitee_id=user_id).all()

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

