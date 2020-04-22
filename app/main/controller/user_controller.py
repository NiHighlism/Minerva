# endpoint for user operations
from flask import abort, request
from flask_login import current_user, login_required
from flask_restplus import Resource

from app.main.service.user_service import UserService
from app.main.util.dto import AuthDto, UserDto

api = UserDto.api
user_auth = AuthDto.user_auth
user = UserDto.user
userInfo = UserDto.userInfo
payment = UserDto.payment


@api.route('/<id>')
class GetUserDetails(Resource):
    """ Fetch details of user by id """
    @api.doc('Endpoint to fetch details of a user by id')
    @api.marshal_with(userInfo, envelope='resource')
    @api.doc(params={'id': 'Id of the requested user'})
    def get(self, id):
        # Fetching the user id
        return UserService.get_by_id(id)


@api.route("/update")
class UpdateUserInfo(Resource):
    @login_required
    @api.doc(params={"update_dict": "Key value pairs of all update values"})
    @api.expect(userInfo)
    def post(self):
        update_dict = request.json
        return UserService.update_user_info(update_dict)

    # TODO: Superuser can't change username parameter.


@api.route("/add/watch")
class AddMovieWatchList(Resource):
    @login_required
    @api.doc(params={"imdb_ID": "IMDB ID of movie to be added. "})
    def get(self):
        imdb_ID = request.args.get("imdb_ID")
        resp = UserService.add_to_watch_list(imdb_ID)

        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp


@api.route("/add/bucket")
class AddMovieBucketList(Resource):
    @login_required
    @api.doc(params={"imdb_ID": "IMDB ID of movie to be added. "})
    def get(self):
        imdb_ID = request.args.get("imdb_ID")
        resp = UserService.add_to_bucket_list(imdb_ID)

        if resp[1] != 200:
            return abort(403, resp[0])
        else:
            return resp
