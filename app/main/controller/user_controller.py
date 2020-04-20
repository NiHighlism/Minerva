# endpoint for user operations
from app.main.service.user_service import UserService
from app.main.util.dto import AuthDto, UserDto
from flask import request
from flask_login import current_user, login_required
from flask_restplus import Resource

api = UserDto.api
user_auth = AuthDto.user_auth
user = UserDto.user
userInfo = UserDto.userInfo
payment = UserDto.payment


@api.route('/')
class GetUserDetails(Resource):
    """ Fetch details of user by id """
    @api.doc('Endpoint to fetch details of a user by id')
    @api.marshal_with(userInfo, envelope='resource')
    @api.doc(params={'id': 'Id of the requested user'})
    def get(self):
        # Fetching the user id
        return UserService.get_by_id(id=request.args.get('id'))


@api.route("/update")
class UpdateUserInfo(Resource):
    @login_required
    @api.doc(params={"update_dict": "Key value pairs of all update values"})
    @api.expect(userInfo)
    def post(self):
        update_dict = request.json
        return UserService.update_user_info(update_dict)
