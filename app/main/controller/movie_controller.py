'''
All Endpoints required for movie
operations such as adding and fetching from DB.

'''

from flask import abort, request, jsonify
from flask_restplus import Resource

from app.main.models.movies import Movie
from app.main.util.dto import MovieDto
api = MovieDto.api

@api.route('/')
class HelloWorld(Resource):
    def get(self):
        return jsonify({"text" : "Hello World!"})
