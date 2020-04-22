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
    @api.doc("params : {'Query' : 'Search Query'}")
    @api.marshal_list_with(movie)
    def get(self):
        query = request.args.get("q")
        page = request.args.get("page") or 1
        resp = MovieService.search_for_movie(query, page)
        if resp[1] != 200:
            return abort(403, resp[1])
        else:
            return resp

@api.route('/search/pages')
class NumberOfPages(Resource):
    def get(self):
        query = request.args.get("q")
        resp = MovieService.get_total_pages(query)
        if resp[1] != 200:
            return abort(403, resp[1])
        else:
            return resp