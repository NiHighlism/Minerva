"""
DB Model for Likes and
relevant junction tables
"""
import datetime

from sqlalchemy.sql import and_, select

from app.main import db, login_manager


class Reaction(db.Model):
    """
    Description of User model.
    Columns
    -----------
    :id: int [pk]
    :value: int [pk]
    :user_id: int [Foreign Key -> User.id]
    :post_id: int [Foreign Key -> Post.id]
    :creation_time: DateTime [not NULL]
    """

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    value = db.Column(db.Integer)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now())

    def __init__(self, value, user_id, post_id):
        self.value = value
        self.user_id = user_id
        self.post_id = post_id
