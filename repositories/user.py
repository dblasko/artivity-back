from sqlalchemy.exc import IntegrityError
from werkzeug.security import generate_password_hash, check_password_hash

from app import db
from models import User, friendship


class UserRepository:

    def create(self, pseudo, email, password):
        try:
            user = User(
                pseudo=pseudo, email=email,
                password_hash=generate_password_hash(password)
            )
            db.session.add(user)
            db.session.commit()
        except IntegrityError:
            return None
        return user

    def get(self, user_id):
        """
        Get a user from its id
        :param user_id: the user id
        :return: a User instance if it exists, otherwise None
        """
        return User.query.get(user_id)

    def get_by_email(self, email):
        """
        Get a user by email
        :param email: the user email
        :return: a User instance if found, otherwise None
        """
        return User.query.filter_by(email=email).first()

    def get_by_pseudo(self, pseudo):
        """
        Get a user by pseudo
        :param pseudo: the user pseudo
        :return: a User instance if found, otherwise None
        """
        return User.query.filter_by(pseudo=pseudo).first()

    def authenticate(self, username, password):
        user = User.query.filter_by(email=username).first()
        if user is None:
            user = User.query.filter_by(pseudo=username).first()

        if user is not None:
            if not check_password_hash(user.password_hash, password):
                user = None

        return user   # None if not authenticated

    def update(self, user):
        db.session.merge(user)
        db.session.commit()
        return user

    def search(self, query):
        return User.query.filter(User.pseudo.ilike(query+'%')).limit(3).all()

