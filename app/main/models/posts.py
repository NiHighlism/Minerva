"""
DB Model for Posts and
relevant junction tables
"""
import datetime

from sqlalchemy.sql import and_, select

from app.main import db, login_manager


class Post(db.Model):
    """
    Description of User model.
    Columns
    -----------
    :id: int [pk]
    :title: Text [not NULL]
    :creation_time: DateTime [not NULL]
    :last_edit_time: DateTime [not NULL]
    :post_author: int
    :post_body: Text
    """

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_edit_time = db.Column(db.DateTime, default=datetime.datetime.now())
    post_body = db.Column(db.Text)

    def __init__(self)

    db.session.add(self)
    db.session.commit()

    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()
