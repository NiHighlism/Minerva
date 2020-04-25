"""
DB Model for Comments and
relevant junction tables
"""
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_, select

from app.main import db
from app.main.models.base import Base
from app.main.models.commentSearches import SearchableMixin


class Comment(SearchableMixin, Base):
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
    id = db.Column(db.Integer, db.ForeignKey("base.id"), primary_key=True)
    comment_id = db.Column(db.Integer, autoincrement=True,
                           primary_key=True, unique=True)
    parent_post_id = db.Column(db.Integer, db.ForeignKey("post.post_id"))

    __searchable__ = ['body']

    __mapper_args__ = {
        'polymorphic_identity': 'comment',
        'inherit_condition': (id == Base.id)
    }

    def __init__(self, author_id, parent_post_id, comment_body):
        super().__init__(author_id, comment_body, 'comment')
        self.parent_post_id = parent_post_id

        db.session.add(self)
        db.session.commit()

    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()

    def delete_comment(self, comment_id):
        comment = Comment.query.filter_by(id=comment_id).delete()
        db.session.commit()
