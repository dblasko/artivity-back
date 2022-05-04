from app import db

friendship = db.Table("friendship",
                      db.Column("left_friend_id", db.Integer, db.ForeignKey("user.id"), primary_key=True),
                      db.Column("right_friend_id", db.Integer, db.ForeignKey("user.id"), primary_key=True)
                      )


class User(db.Model):
    id = db.Column(db.Integer, primary_key=True, nullable=False)
    pseudo = db.Column(db.String(50), unique=True)
    email = db.Column(db.String(320), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)

    bio = db.Column(db.String(250), default="", nullable=False)

    challenges_answers = db.relationship("ChallengeAnswer", back_populates="user", lazy=True)
    challenges_created = db.relationship("Challenge", back_populates="user_created", lazy=True,
                                         primaryjoin="User.id==Challenge.user_created_id")

    friends = db.relationship("User", secondary=friendship,
                              primaryjoin=id == friendship.c.left_friend_id,
                              secondaryjoin=id == friendship.c.right_friend_id,
                              backref="friendship"
                              )

    def json_preview(self):
        return {
            "id": self.id,
            "pseudo": self.pseudo
        }

    def json(self):
        return {
            "id": self.id,
            "pseudo": self.pseudo,
            "email": self.email,
            "bio": self.bio
        }

    def public_json(self):
        return {
            "id": self.id,
            "pseudo": self.pseudo,
            "biography": self.bio
        }


class Friend_Invite(db.Model):
    inviter_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)
    invitee_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=False, primary_key=True)

    invite_time = db.Column(db.DateTime, nullable=False)

    invitee = db.relationship("User", foreign_keys=invitee_id, backref=db.backref('friend_invited'))
    inviter = db.relationship("User", foreign_keys=inviter_id, backref=db.backref('friend_inviter'))
