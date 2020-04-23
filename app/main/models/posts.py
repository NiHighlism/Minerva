"""
DB Model for Posts and
relevant junction tables
"""
import datetime

from sqlalchemy.sql import and_, select

from app.main import db, login_manager
from app.main.models.comments import Comment


class Post(db.Model):
    """
    Description of User model.
    Columns
    -----------
    :id: int [pk]
    :title: Text [not NULL]
    :author_id: int [Foreign Key]
    :creation_time: DateTime [not NULL]
    :last_edit_time: DateTime [not NULL]
    :post_body: Text

    # Relationships
    :comments: Relationship -> Comments (one to many)
    """

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.Text, nullable=False)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_edit_time = db.Column(db.DateTime, default=datetime.datetime.now())
    post_body = db.Column(db.Text)

    # Relationships
    comments = db.relationship('Comment', backref="post")

    def __init__(self, title, author_id, post_body):
        self.title = title
        self.author_id = author_id
        self.post_body = post_body

        db.session.add(self)
        db.session.commit()

    def upvote_post(self, user_id):
        upvote = Reaction(1, user_id, self.id)

        self.upvote_list.append(upvote)
        db.session.commit()

    def downvote_post(self, user_id):
        downvote = Reaction(-1, user_id, self.id)

        self.downvote_list.append(downvote)
        db.session.commit()

    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()
