"""for user related operations"""

import datetime
import requests

from logging import getLogger
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound

from app.main import db
from app.main.models.movies import Movie

LOG = getLogger(__name__)


class MovieService:

    @staticmethod
    def get_by_imdb_id(imdb_ID):
        try:
            movie = Movie.query.filter_by(imdb_ID=imdb_ID).first()

            if movie is not None:
                print("SEEDHA DB SE UTHAYA, BADA MAZAA AAYA")
                return movie, 200
            
            apikey = current_app.config['OMDB_API_KEY']
            key_params = {'apikey' : apikey, 'i' : imdb_ID}
            base_url = "http://www.omdbapi.com"
            
            request = requests.get(base_url, key_params)
            
            result_json = request.json()
            result = {}

            result['imdb_ID'] = imdb_ID
            result['title'] = result_json['Title']
            result['year'] = result_json['Year']
            result['release_date'] = result_json['Released']
            result['runtime'] = result_json['Runtime']
            result['plot'] = result_json['Plot']
            
            genres = result_json['Genre'].split(", ")
            result['genre'] = {"genreList" : genres}

            directors = result_json['Director'].split(", ")
            result['director'] = {'directorList' : directors}

            writers = result_json['Writer'].split(", ")
            result['writer'] = {'writerList' : writers}

            actors = result_json['Actors'].split(", ")
            result['actors'] = {'actorsList' : actors}

            
            languages = result_json['Language'].split(", ")
            result['language'] = {'languageList' : languages}

            countries = result_json['Country'].split(", ")
            result['country'] = {'countryList' : countries}

            result['awards'] = result_json['Awards']
            
            ratings = result_json['Ratings']
            result['imdb_rating'] = ratings[0]['Value']
            result['rotten_tomatoes'] = ratings[1]['Value']
            result['metascore'] = ratings[2]['Value']

            result['poster_url'] = result_json['Poster']
            result['box_office'] = result_json['BoxOffice']
            
            movie = Movie(**result)
            return result, 200

        except BaseException:
            LOG.error('Details couldn\'t be fetched for ID: {}'.format(imdb_ID), exc_info=True)
            response_object = {
                'status' : 'Error',
                'message' : 'Failed fetching details. Try later.'
            }

            return response_object, 500
