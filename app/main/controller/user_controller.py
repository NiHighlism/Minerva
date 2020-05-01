# endpoint for user operations
from flask import abort, request
from flask_login import current_user, login_required
from flask_restplus import Resource

from app.main.service.user_service import UserService
from app.main.util.dto import AuthDto, MovieDto, UserDto

api = UserDto.api
user_auth = AuthDto.user_auth
user = UserDto.user
userInfo = UserDto.userInfo
updateInfo = UserDto.updateInfo
movie = MovieDto.movie
movieList = MovieDto.movieList


@api.route('/<username>')
class GetUserDetails(Resource):
    """ Fetch details of user by id """
    @api.doc('Endpoint to fetch details of a user by id')
    @api.marshal_with(userInfo)
    @api.doc(params={'username': 'Username of the requested user'})
    def get(self, username):
        # Fetching the user id
        return UserService.get_by_username(username)


@api.route("/update")
class UpdateUserInfo(Resource):
    @login_required
    @api.doc(params={"update_dict": "Key value pairs of all update values"})
    @api.expect(updateInfo)
    def post(self):
        update_dict = request.json
        return UserService.update_user_info(update_dict)

    # TODO: Superuser can't change username parameter.


@api.route("/add/seenList")
class AddSeenMovieList(Resource):
    @login_required
    @api.marshal_list_with(movieList)
    @api.expect(movieList)
    def post(self):
        post_data = request.json
        resp = UserService.add_to_seen_list(post_data)

        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp

@api.route("/add/bucketList")
class AdducketMovieList(Resource):
    @login_required
    @api.marshal_list_with(movieList)
    @api.expect(movieList)
    def post(self):
        post_data = request.json
        resp = UserService.add_to_bucket_list(post_data)

        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp

@api.route("/add/recommendList")
class AddRecommendMovieList(Resource):
    @login_required
    @api.marshal_list_with(movieList)
    @api.expect(movieList)
    def post(self):
        post_data = request.json
        resp = UserService.add_to_recommend_list(post_data)

        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp


@api.route("/<username>/getSeenList")
class getSeenList(Resource):
    @api.marshal_with(movieList)
    def get(self, username):
        resp = UserService.get_seen_list(username)
        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp
@api.route("/<username>/getBucketList")
class getBucketList(Resource):
    @api.marshal_list_with(movieList)
    def get(self, username):
        resp = UserService.get_bucket_list(username)
        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp
@api.route("/<username>/getRecommendList")
class getRecommendList(Resource):
    @api.marshal_list_with(movieList)
    def get(self, username):
        resp = UserService.get_recommend_list(username)
        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp
