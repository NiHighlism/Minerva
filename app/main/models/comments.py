"""
DB Model for Comments and
relevant junction tables
"""
import datetime

from sqlalchemy.sql import and_, select

from app.main import db, login_manager
from app.main.models.reactions import Reaction


class Comment(db.Model):

    _N = 6
    """
    Description of User model.
    Columns
    -----------
    :id: int [pk]
    :author_id: int [Foreign Key -> User.id]
    :post_id: int [Foreign Key -> Post.id]
    :upvotes: int
    :downvotes: int
    :creation_time: DateTime [not NULL]
    :last_edit_time: DateTime [not NULL]
    :comment_body: Text
    """

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    author_id = db.Column(db.Integer, db.ForeignKey("user.id"))
    post_id = db.Column(db.Integer, db.ForeignKey("post.id"))
    upvotes = db.Column(db.Integer, default=0)
    downvotes = db.Column(db.Integer, default=0)
    comment_body = db.Column(db.Text)
    path = db.Column(db.Text, index=True)
    parent_id = db.Column(db.Integer, db.ForeignKey('comment.id'))
    creation_time = db.Column(db.DateTime, default=datetime.datetime.now())
    last_edit_time = db.Column(db.DateTime, default=datetime.datetime.now())

    # Relationships
    replies = db.relationship(
        'Comment', backref=db.backref('parent', remote_side=[id]),
        lazy='dynamic')

    upvote_list = db.relationship(
        'Reaction', backref="comment.id", lazy='dynamic'
    )

    def __init__(self, author_id, post_id, comment_body):
        self.author_id = author_id
        self.post_id = post_id
        self.comment_body = comment_body

        db.session.add(self)
        db.session.commit()

        prefix = self.parent.path + '.' if self.parent else ''
        self.path = prefix + '{:0{}d}'.format(self.id, self._N)

        db.session.commit()

    def upvote_comment(self, user_id):
        upvote = Reaction(1, user_id, self.id)

        self.upvote_list.append(upvote)
        db.session.commit()

    def downvote_comment(self, user_id):
        downvote = Reaction(-1, user_id, self.id)

        self.downvote_list.append(downvote)
        db.session.commit()

    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()
