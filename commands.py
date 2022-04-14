from datetime import datetime

from app import app, db
from models import ChallengeType, ChallengeAnswer
from repositories import UserRepository, ChallengeRepository


@app.cli.command("create_db")
def create_db():
    db.create_all()


@app.cli.command("drop_db")
def drop_db():
    db.drop_all()


@app.cli.command("populate_dummy_db")
def populate_dummy_db():
    db.drop_all()
    db.create_all()

    user_repo = UserRepository()
    danny = user_repo.create(pseudo="danny", email="daniel.blasko.dev@gmail.com", password="toto")
    tuthur = user_repo.create(pseudo="tuthur", email="arthur.gardon@gmail.com", password="tata")

    challenge_repo = ChallengeRepository()
    challenge_1 = challenge_repo.create(subject="Dessine-moi un mouton",
                                        title="Balade champêtre",
                                        type=ChallengeType.drawing,
                                        start_datetime=datetime.now(),
                                        end_datetime=None,
                                        timelimit_seconds=None,
                                        user_created=danny)

    challenge_2 = challenge_repo.create(subject="Chofite",
                                        title="Bolopop",
                                        type=ChallengeType.text,
                                        start_datetime=datetime.now(),
                                        end_datetime=None,
                                        timelimit_seconds=None,
                                        user_created=tuthur)

    dummy_answer_1 = ChallengeAnswer(
        user=danny,
        challenge=challenge_1,
        start_time=datetime.now(),
        is_public=True
    )
    db.session.add(dummy_answer_1)
    db.session.commit()

    dummy_answer_2 = ChallengeAnswer(
        user=danny,
        challenge=challenge_2,
        start_time=datetime.now(),
        is_public=True
    )
    db.session.add(dummy_answer_2)
    db.session.commit()

