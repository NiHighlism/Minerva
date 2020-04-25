"""
DB Model for Posts and
relevant junction tables
"""
import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import and_, select

from app.main import db
from app.main.models.base import Base
from app.main.models.comments import Comment
from app.main.models.movies import Movie
from app.main.models.postSearches import SearchableMixin


class Post(Base, SearchableMixin):
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
    id = db.Column(db.Integer, db.ForeignKey("base.id"), primary_key=True)
    post_id = db.Column(db.Integer, autoincrement=True,
                        primary_key=True, unique=True)
    title = db.Column(db.Text, nullable=False)

    post_movie = db.Column(db.String(20))

    __searchable__ = ['title', 'body']

    __mapper_args__ = {
        'polymorphic_identity': 'post',
        'inherit_condition': (id == Base.id)
    }

    comments = db.relationship('Comment', primaryjoin="(Post.post_id == Comment.parent_post_id)",
                               backref=db.backref('post'), lazy='dynamic')

    def __init__(self, author_id, post_movie, title, post_body):
        super().__init__(author_id, post_body, "post")
        self.title = title
        self.post_movie = post_movie
        db.session.add(self)
        db.session.commit()

    def add_comment(self, author_id, comment_body):
        parent_post_id = self.id
        comment = Comment(author_id, parent_post_id, comment_body)
        self.comments.append(comment)
        db.session.commit()

        return comment.id

    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()

    def delete_post(self, post_id):
        post = Post.query.filter_by(id=post_id).delete()
        db.session.commit()
