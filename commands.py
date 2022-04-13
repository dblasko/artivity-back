from app import app, db
from repositories import UserRepository


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
    user_repo.create(pseudo="danny", email="daniel.blasko.dev@gmail.com", password="toto")
    user_repo.create(pseudo="tuthur", email="arthur.gardon@gmail.com", password="tata")

