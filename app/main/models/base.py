"""
Base Model for Posts
and Comments. 
"""
import datetime

from sqlalchemy.sql import and_, select
from sqlalchemy.ext.declarative import declared_attr

from app.main import db
from app.main.models.reactions import Reaction

class Base(db.Model):

    """
    Description of Base Post model.
    Columns
    -----------
    :id: int [pk]
    :author_id: int [Foreign Key -> User.id]
    :upvotes: int
    :downvotes: int
    :creation_time: DateTime [not NULL]
    :last_edit_time: DateTime [not NULL]
    :body: Text
    """

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    body = db.Column(db.Text)
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_edit_time = db.Column(db.DateTime, default=datetime.datetime.now())

    type = db.Column(db.String(10))
    __mapper_args__ = {
        'polymorphic_identity':'base',
        'polymorphic_on':type
    }

    # Relationships

    # Relationships
    reaction_list = db.relationship(
        'Reaction', backref="reaction_id", lazy='dynamic'
    )


    def __init__(self, author_id, body, type):
        self.author_id = author_id
        self.body=body
        self.type=type

    def upvote(self, user_id):
        upvote = Reaction(1, user_id, self.id)

        self.reaction_list.append(upvote)
        self.upvotes +=1 
        db.session.commit()

    def downvote(self, user_id):
        downvote = Reaction(-1, user_id, self.id)

        self.reaction_list.append(downvote)
        self.downvotes += 1
        db.session.commit()
        

    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()
