import random
from datetime import datetime

from sqlalchemy import func, null

from app import db
from models import Challenge, ChallengeAnswer, ChallengeInvite, User


class ChallengeRepository:

    def create(self, subject, title, ch_type, start_datetime, end_datetime, timelimit_seconds, user_created):
        challenge = Challenge(
            subject=subject, title=title, 
            type=ch_type, start_datetime=start_datetime,
            end_datetime=end_datetime, timelimit_seconds=timelimit_seconds,
            user_created=user_created
        )
        db.session.add(challenge)
        db.session.commit()
        return challenge

    def create_collaborative_challenge(self, subject, title, ch_type, start_datetime, end_datetime, timelimit_seconds, user_created):
        challenge = Challenge(
            subject=subject, title=title,
            type=ch_type, start_datetime=start_datetime,
            end_datetime=end_datetime, timelimit_seconds=timelimit_seconds,
            user_created=user_created,
            is_collab=True, whos_turn=user_created, is_public=False
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

    def create_answer(self, challenge_id, user_id, is_public):
        challenge_answer = ChallengeAnswer(
            user_id=user_id,
            challenge_id=challenge_id,
            is_public=is_public,
            start_time=datetime.now()
        )
        db.session.add(challenge_answer)
        db.session.commit()
        return challenge_answer

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

    def was_invited(self, invitee_id, challenge_id):
        """
        Returns true if the invitee user has an invite for the specified challenge
        :param invitee_id: the invited user's id
        :param challenge_id: the challenge id
        :return: a boolean
        """
        return ChallengeInvite.query.filter_by(invitee_id=invitee_id, challenge_id=challenge_id).count() > 0

    def pick_random(self):
        max_id = db.session.query(func.max(Challenge.id)).scalar()

        selected_challenge = None
        while selected_challenge is None:
            selected_id = random.randint(0, max_id)
            selected_challenge = self.get(selected_id)

        return selected_challenge

    def pick_n_random(self, n):
        challenges = set()
        max_challenges = Challenge.query.count()

        while len(challenges) < min(max_challenges, n):
            challenges.add(self.pick_random())

        return challenges

    def pick_random_answers(self, n):
        answers = set()
        max_answers = ChallengeAnswer.query.count()

        while len(answers) < min(max_answers, n):
            max_ch_id = db.session.query(func.max(ChallengeAnswer.challenge_id)).scalar()
            max_us_id = db.session.query(func.max(ChallengeAnswer.user_id)).scalar()

            selected_answer = None
            while selected_answer is None:
                sel_ch_id = random.randint(0, max_ch_id)
                sel_us_id = random.randint(0, max_us_id)
                selected_answer = self.get_answer(sel_us_id, sel_ch_id)

            answers.add(selected_answer)

        return answers

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

    def start_challenge(self, challenge_id, user_id, is_public):
        answer = self.get_answer(challenge_id=challenge_id, user_id=user_id)
        if answer:
            answer.end_time = None
            answer.start_time = datetime.now()
            answer.answer = None
            answer.is_public = is_public
            self.update_answer(answer)
        else:
            answer = self.create_answer(challenge_id, user_id, is_public)
        return answer

    def get_user_public_created_challenges(self, user_id):
        challenges = Challenge.query.filter_by(user_created_id=user_id, is_public=True).all()
        return challenges

    def get_user_public_challenge_answers(self, user_id):
        answers = ChallengeAnswer.query.filter_by(user_id=user_id, is_public=True).all()
        return answers

    def collab_get_available_next_users(self, challenge_id):
        # user must have been invited
        # user should not have a completed answer
        # user should not be current whos_turn
        users = db.session.query(User)\
            .select_from(ChallengeInvite) \
            .filter(ChallengeInvite.challenge_id == challenge_id) \
            .join(User, User.id == ChallengeInvite.invitee_id)\
            .join(Challenge, Challenge.id == ChallengeInvite.challenge_id)\
            .filter(Challenge.whos_turn_id != User.id)\
            .outerjoin(ChallengeAnswer, User.id == ChallengeAnswer.user_id)\
            .filter(ChallengeAnswer.end_time == None)

        return users

    def get_public_challenge_answers(self, challenge_id):
        return ChallengeAnswer.query.filter_by(is_public=True, challenge_id=challenge_id).all()

    def search(self, query):
        return Challenge.query.filter(Challenge.title.ilike(query+'%')).limit(3).all()

    def get_all_user_answers(self, user_id):
        return ChallengeAnswer.query.filter_by(user_id=user_id).all()
