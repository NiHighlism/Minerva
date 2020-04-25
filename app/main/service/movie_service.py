"""for user related operations"""

import datetime
from logging import getLogger

import requests
from flask import current_app
from sqlalchemy.orm.exc import NoResultFound

from app.main import db
from app.main.models.movies import Movie
from app.main.models.posts import Post

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
            key_params = {'apikey': apikey, 'i': imdb_ID}
            base_url = "http://www.omdbapi.com"

            request = requests.get(base_url, key_params)

            result_json = request.json()
            result = {}

            result['imdb_ID'] = imdb_ID
            result['title'] = result_json['Title']
            result['year'] = result_json['Year'].strip("-")
            result['release_date'] = result_json.get('Released', '')
            result['runtime'] = result_json.get('Runtime', '')
            result['plot'] = result_json.get('Plot', '')

            genres = result_json['Genre'].split(", ")
            result['genre'] = {"genreList": genres}

            directors = result_json['Director'].split(", ")
            result['director'] = {'directorList': directors}

            writers = result_json['Writer'].split(", ")
            result['writer'] = {'writerList': writers}

            actors = result_json['Actors'].split(", ")
            result['actors'] = {'actorsList': actors}

            languages = result_json['Language'].split(", ")
            result['language'] = {'languageList': languages}

            countries = result_json['Country'].split(", ")
            result['country'] = {'countryList': countries}

            result['awards'] = result_json.get('Awards', '')

            try:
                ratings = result_json['Ratings']
                result['imdb_rating'] = ratings[0]['Value']
                result['rotten_tomatoes'] = ratings[1]['Value']
                result['metascore'] = ratings[2]['Value']
            except Exception:
                result['imdb_rating'] = "N/A"
                result['rotten_tomatoes'] = "N/A"
                result['metascore'] = "N/A"

            result['poster_url'] = result_json.get('Poster', '')
            result['box_office'] = result_json.get('BoxOffice', '')

            movie = Movie(**result)
            return result, 200

        except BaseException:
            LOG.error('Details couldn\'t be fetched for ID: {}'.format(
                imdb_ID), exc_info=True)
            response_object = {
                'status': 'Error',
                'message': 'Failed fetching details. Try later.'
            }

            return response_object, 500

    @staticmethod
    def search_for_movie(query, page):
        try:
            print(query)
            # body={'query': {'multi_match': {'query': query, 'fields': "*"}}}

            # r = requests.post("http://localhost:9200/movie/_search", data=body)
            # print(r.status_code)
            results_per_page = current_app.config['RESULTS_PER_PAGE']
            res, totalResults = Movie.search(query, page, results_per_page)
            res_objects = res.all()

            movie_results = [movie for movie in res_objects]
            return movie_results, 200

        except BaseException as e:
            LOG.error(
                "Search query was not able to complete. Please try again later", exc_info=True)
            response_object = {
                'status': 'Error',
                'message': 'Failed fetching details. Try later.'
            }

            return response_object, 500

    @staticmethod
    def get_total_pages(query):
        try:
            results_per_page = current_app.config['RESULTS_PER_PAGE']
            res, totalResults = Movie.search(query, 1, results_per_page)
            total_pages = int(totalResults) / int(results_per_page) or 1

            return total_pages, 200

        except BaseException:
            LOG.error(
                "Search query was not able to complete. Please try again later", exc_info=True)
            response_object = {
                'status': 'Error',
                'message': 'Failed fetching details. Try later.'
            }

            return response_object, 500

    @staticmethod
    def get_all_posts(id):
        try:
            res = Post.query.filter_by(post_movie=id).all()
            print(res)

            posts = [post for post in res]
            return posts, 200

        except BaseException:
            LOG.error(
                "Search query was not able to complete. Please try again later", exc_info=True)
            response_object = {
                'status': 'Error',
                'message': 'Failed fetching details. Try later.'
            }

            return response_object, 500
