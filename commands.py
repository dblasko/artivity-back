from datetime import datetime

from app import app, db
from models import ChallengeType, ChallengeAnswer, ChallengeInvite
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
    user_a = user_repo.create(pseudo="user_a", email="user_a@gmail.com", password="tata")
    user_b = user_repo.create(pseudo="user_b", email="user_b@gmail.com", password="tata")
    user_c = user_repo.create(pseudo="user_c", email="user_c@gmail.com", password="tata")
    user_d = user_repo.create(pseudo="user_d", email="user_d@gmail.com", password="tata")
    user_e = user_repo.create(pseudo="user_e", email="user_e@gmail.com", password="tata")
    user_f = user_repo.create(pseudo="user_f", email="user_f@gmail.com", password="tata")
    user_g = user_repo.create(pseudo="user_g", email="user_g@gmail.com", password="tata")
    user_h = user_repo.create(pseudo="user_h", email="user_h@gmail.com", password="tata")

    challenge_repo = ChallengeRepository()
    challenge_1 = challenge_repo.create(subject="Dessine-moi un mouton",
                                        title="Balade champêtre",
                                        ch_type=ChallengeType.drawing,
                                        start_datetime=datetime.now(),
                                        end_datetime=datetime(day=12, month=5, year=2022),
                                        timelimit_seconds=120,
                                        user_created=danny)

    challenge_2 = challenge_repo.create(subject="Chofite",
                                        title="Bolopop",
                                        ch_type=ChallengeType.drawing,
                                        start_datetime=datetime.now(),
                                        end_datetime=datetime(day=12, month=5, year=2022),
                                        timelimit_seconds=None,
                                        user_created=tuthur)

    challenge_3 = challenge_repo.create(subject="Chantez votre chanson favorite",
                                        title="Karaoké",
                                        ch_type=ChallengeType.sound,
                                        start_datetime=datetime.now(),
                                        end_datetime=datetime(day=12, month=5, year=2022),
                                        timelimit_seconds=None,
                                        user_created=tuthur)

    challenge_4 = challenge_repo.create(subject="Un sentier d'automne",
                                        title="Exprimez vos pensées profondes",
                                        ch_type=ChallengeType.text,
                                        start_datetime=datetime.now(),
                                        end_datetime=datetime(day=12, month=5, year=2022),
                                        timelimit_seconds=None,
                                        user_created=tuthur)

    collab_challenge = challenge_repo.create_collaborative_challenge(
        subject="Draw what you want",
        title="Collaborative mayhem",
        ch_type=ChallengeType.drawing,
        start_datetime=datetime.now(),
        end_datetime=None,
        timelimit_seconds=None,
        user_created=danny
    )

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

    challenge_repo.create_invite(tuthur.id, danny.id, challenge_1.id)
    challenge_repo.create_invite(tuthur.id, danny.id, challenge_2.id)
    challenge_repo.create_invite(tuthur.id, danny.id, challenge_4.id)
    challenge_repo.create_invite(tuthur.id, danny.id, challenge_3.id)
    challenge_repo.create_invite(danny.id, user_a.id, collab_challenge.id)
    challenge_repo.create_invite(danny.id, user_b.id, collab_challenge.id)
    challenge_repo.create_invite(danny.id, user_c.id, collab_challenge.id)
    challenge_repo.create_invite(danny.id, user_d.id, collab_challenge.id)
    challenge_repo.create_invite(danny.id, user_e.id, collab_challenge.id)
    challenge_repo.create_invite(danny.id, user_f.id, collab_challenge.id)
    challenge_repo.create_invite(danny.id, user_g.id, collab_challenge.id)
    challenge_repo.create_invite(danny.id, user_h.id, collab_challenge.id)



