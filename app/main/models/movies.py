"""
DB Model for Movies table and
relevant junction tables
"""
import datetime
import json

from sqlalchemy.sql import and_, select

from app.main import db, login_manager
from app.main.models.movieSearches import SearchableMixin


class Movie(SearchableMixin, db.Model):
    """
    Description of User model.
    Columns
    -----------
    :id: int [pk]
    :user_id: int [Foreign Key -> User.id]
    :imdb_ID: varchar(128) [not NULL]
    :title: Text [not NULL]
    :year: int
    :release_date: DateTime
    :runtime: int
    :genre: JSON
    :director: JSON
    :writer: JSON
    :actors: JSON
    :plot: Text
    :language: JSON
    :country: JSON
    :awards: Text
    :ratings: JSON
    :imdb_rating: Float
    :rotten_tomatoes: int
    :metascore: int
    :poster_URL: varchar(255)
    :box_office: varchar(255)
    :added_to_db: DateTime
    """

    # Columns
    id = db.Column(db.Integer, primary_key=True)
    parent_user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    imdb_ID = db.Column(db.String(128), unique=True, nullable=False)
    title = db.Column(db.Text, nullable=False)
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

    __searchable__ = ['title', 'year', 'genre',
                      'director', 'actors', 'language', 'country']

    def __init__(self, imdb_ID, title, year, release_date, runtime, genre, director,
                 writer, actors, plot, language, country, awards,
                 imdb_rating, rotten_tomatoes, metascore, poster_url, box_office):

        self.imdb_ID = imdb_ID
        self.title = title
        self.year = year
        self.release_date = release_date
        self.runtime = runtime
        self.genre = genre
        self.director = director
        self.writer = writer
        self.actors = actors
        self.plot = plot
        self.language = language
        self.country = country
        self.awards = awards
        self.imdb_rating = imdb_rating
        self.rotten_tomatoes = rotten_tomatoes
        self.metascore = metascore
        self.poster_url = poster_url
        self.box_office = box_office
        self.added_time = datetime.datetime.now()

        db.session.add(self)
        db.session.commit()

    def update_col(self, key, value):
        setattr(self, key, value)
        db.session.commit()
