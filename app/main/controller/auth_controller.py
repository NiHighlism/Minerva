'''
All Endpoints required for authentication
operations such as login, logout and signup.

'''

from logging import getLogger

from flask import abort, request
from flask_jwt_extended import (create_access_token, create_refresh_token, decode_token, get_jwt_identity, get_raw_jwt,
                                jwt_refresh_token_required, jwt_required)
from flask_login import current_user, login_required
from flask_restplus import Resource

from app.main.service.auth_service import Authentication
from app.main.util.dto import AuthDto, UserDto

api = AuthDto.api
user_auth = AuthDto.user_auth
user = UserDto.user
email = AuthDto.reset_email
login_info = AuthDto.login_info
change_password = AuthDto.change_password

LOG = getLogger(__name__)


@api.route('/login')
class UserLogin(Resource):
    """ User Login Resource """
    @api.doc('Endpoint for User Login')
    @api.expect(user_auth, validate=True)
    @api.marshal_with(login_info)
    def post(self):
        # get the post data
        post_data = request.json
        resp = Authentication.login_user(data=post_data)

        if resp[1] != 200:
            return resp
        else:
            access_token = create_access_token(identity=resp[0]['username'])
            refresh_token = create_refresh_token(identity=resp[0]['username'])

            resp[0]['access_token'] = access_token
            resp[0]['refresh_token'] = refresh_token

            return resp


@api.route('/refreshToken')
class RefereshJWTToken(Resource):
    @login_required
    def post(self):
        try:
            print(request.headers)
            LOG.error(request.headers, exc_info=True)
            token = request.headers['Authorization']
            user_id = decode_token(token)
            username = user_id['identity']
            response_object = {
                'username': username,
                'access_token': create_access_token(identity=username),
                'refresh_token': create_refresh_token(identity=username)
            }
            return response_object, 200

        except BaseException:
            response_object = {
                'status': 'fail',
                'message': 'Could not refresh token. '
            }
            LOG.error("Couldn't refresh token", exc_info=True)
            return response_object, 500


@api.route('/logout')
class UserLogout(Resource):
    """
    Logout Resource
    """
    @login_required
    @api.doc('Endpoint for User Logout')
    def post(self):
        return Authentication.logout_user()


@api.route('/isLoggedIn')
class CheckLogIn(Resource):
    def get(self):

        if current_user.is_authenticated:
            resp = {
                'status': 'success',
                'message': 'Logged In'
            }
            return resp, 200
        else:
            resp = {
                'status': 'fail',
                'message': ' Not Logged In'
            }
            return resp, 400


# Signup
@api.route('/signup')
class SignUp(Resource):

    @api.doc('Endpoint for Signing Up a new user')
    @api.expect(user, validate=True)
    def post(self):
        post_data = request.json
        send_mail = request.args.get('send_mail')
        resp = Authentication.signup_user(data=post_data, send_mail=send_mail)

        return resp


# Verify Email after signing up
@api.route('/resendVerificationEmail')
class SendVerificationEmail(Resource):
    """ Send user verification mail to the user."""
    @api.doc('Endpoint for sending a verification mail to the user')
    @api.expect(email, validate=True)
    def post(self):
        data = request.json
        return Authentication.resend_verification(data)


@api.route('/confirm/<token>', methods=['GET'])
class ConfirmToken(Resource):
    """ Confirm the Email Verification Token Sent """
    @api.doc('Endpoint to Confirm the Email Verification Token Sent ')
    def get(self, token):
        return Authentication.confirm_token_service(token)

# I think we can implement this without this function, remove if redundant


# Request a reset of Password


@api.route('/reset/request', methods=["POST"])
class ResetRequest(Resource):
    """Send a request to change the password """
    @api.doc('Endpoint to Send a request to change the password ')
    @api.expect(email, validate=True)
    def post(self):
        post_data = request.json
        return Authentication.reset_password_mail(data=post_data)


@api.route('/reset/<token>', methods=["GET", "POST"])
class ResetTokenVerify(Resource):
    """Confirm the token sent to change the password and set a new password."""
    @api.doc(
        'Endpoint to Confirm the token sent to change the password and set a new password')
    def get(self, token):
        return Authentication.confirm_reset_token_service(token)

    def post(self, token):
        return Authentication.reset_password_with_token(token)


@api.route('/changePassword')
class changePassword(Resource):
    @api.expect(change_password, validate=True)
    def post(self):
        post_data = request.json
        return Authentication.change_user_password(post_data)
