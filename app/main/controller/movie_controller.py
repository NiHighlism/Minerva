'''
All Endpoints required for movie
operations such as adding and fetching from DB.

'''
from flask import abort, jsonify, request, current_app
from flask_restplus import Resource

from app.main.service.movie_service import MovieService
from app.main.util.dto import MovieDto

api = MovieDto.api
movie = MovieDto.movie


# @api.route('/<imdb_ID')
# class MovieJSON(Resource):
#     """ Fetch details for movie with given ID """
#     @api.doc("params: {'imdb_ID' : 'Movie ID on IMDB'")
#     @api.marshal_with(movie)
#     def get(self, imdb_ID):
#         resp = 

@api.route('/<imdb_ID>')
@api.route('/search/id/<imdb_ID>')
class SearchIMDBID(Resource):
    """ User Login Resource """
    @api.doc("params: {'imdb_ID' : 'Movie ID on IMDB'")
    @api.marshal_with(movie)
    def get(self, imdb_ID):
        resp = MovieService.get_by_imdb_id(imdb_ID)
        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp

@api.route('/search')
class SearchMovies(Resource):
    """ Movie Search Resource """
    @api.doc("params : {'Title' : 'Title of Movie', 'Year' : 'Release Year of movie', 'Language' : 'Release Language of movie'}")
    @api.marshal_list_with(movie)
    def get(self):
        print(request.args)