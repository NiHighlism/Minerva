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
    """

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    imdb_ID = db.Column(db.String(128), unique=True, nullable=False)
    title =  db.Column(db.Text, nullable=False)
    year = db.Column(db.Integer)
    release_date = db.Column(db.String(128))
    runtime = db.Column(db.String(128))
    plot = db.Column(db.Text)
    
    genre = db.Column(db.JSON)
    director = db.Column(db.JSON)
    writer = db.Column(db.JSON)
    actors = db.Column(db.JSON)
    language = db.Column(db.JSON)
    country = db.Column(db.JSON)
    
    awards = db.Column(db.Text)
    imdb_rating = db.Column(db.String(128))
    rotten_tomatoes = db.Column(db.String(128))
    metascore = db.Column(db.String(128))
    poster_url = db.Column(db.String(255))
    box_office = db.Column(db.String(128))
    added_time = db.Column(db.DateTime)

    def __init__(self)

        db.session.add(self)
        db.session.commit()
        
    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()