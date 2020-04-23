"""
DB Model for Comments and
relevant junction tables
"""
import datetime

from sqlalchemy.sql import and_, select

from app.main import db, login_manager


class Comment(db.Model):
    """
    Description of User model.
    Columns
    -----------
    :id: int [pk]
    :author_id: int [Foreign Key -> User.id]
    :post_id: int [Foreign Key -> Post.id]
    :creation_time: DateTime [not NULL]
    :last_edit_time: DateTime [not NULL]
    :comment_body: Text
    """

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_edit_time = db.Column(db.DateTime, default=datetime.datetime.now())
    comment_body = db.Column(db.Text)

    def __init__(self):
        pass
        #TODO: Create __init__ method

    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()
