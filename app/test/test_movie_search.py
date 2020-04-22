import unittest
import datetime


from app.main import db
from app.main.models.movies import Movie
from app.test.base import BaseTestCase
from app.main.util.search import (query_index)


class TestMovieSearch(BaseTestCase):

    def test_movie_model(self): 
        movie_object = {
            "imdb_ID": "tt1596363",
            "title": "The Big Short",
            "year": 2015,
            "runtime": "130 min",
            "release_date": "23 Dec 2015",
            "plot": "In 2006-2007 a group of investors bet against the US mortgage market. In their research they discover how flawed and corrupt the market is.",
            "genre": {
                "genreList": [
                    "Biography",
                    "Comedy",
                    "Drama",
                    "History"
                ]
            },
            "director": {
                "directorList": [
                    "Adam McKay"
                ]
            },
            "writer": {
                "writerList": [
                    "Charles Randolph (screenplay by)",
                    "Adam McKay (screenplay by)",
                    "Michael Lewis (based upon the book by)"
                ]   
            },
            "actors": {
                "actorsList": [
                    "Ryan Gosling",
                    "Rudy Eisenzopf",
                    "Casey Groves",
                    "Charlie Talbert"
                ]
            },
            "language": {
                "languageList": [
                    "English"
                ]
            },
            "country": {
                "countryList": [
                    "USA"
                ]
            },
            "awards": "Won 1 Oscar. Another 37 wins & 80 nominations.",
            "imdb_rating": "7.8/10",
            "rotten_tomatoes": "88%",
            "metascore": "81/100",
            "poster_url": "https://m.media-amazon.com/images/M/MV5BNDc4MThhN2EtZjMzNC00ZDJmLThiZTgtNThlY2UxZWMzNjdkXkEyXkFqcGdeQXVyNDk3NzU2MTQ@._V1_SX300.jpg",
            "box_office": "N/A"
        }

        movie = Movie(**movie_object)
        db.session.add(movie)

        movieRes = Movie.query.filter_by(imdb_ID="tt1596363").first()
        self.assertTrue(isinstance(movieRes, Movie))

    
    def search_movie(self):
        res, total = query_index("The Big Short", 1, 5)
        movie = res.first()
        
        self.assertTrue(movie.title == "The Big Short")
        self.assertTrue(movie.year == 2015)


if __name__ == '__main__':
    unittest.main()