""" for login/logout operations."""
from functools import wraps
from logging import getLogger

from flask import abort
from flask import current_app as app
from flask import g, make_response, redirect, render_template, request, url_for
from flask_login import current_user
from flask_login import login_user as flask_login_user
from flask_login import logout_user as logout

from app.main import db
from app.main.models.users import User
from app.main.util.email_verification import confirm_token, generate_confirmation_token
from app.main.util.forms import PasswordForm
from app.main.util.password_reset import confirm_reset_token, generate_reset_token
from app.main.util.sendgrid import async_send_mail

LOG = getLogger(__name__)


class Authentication:

    @staticmethod
    def isSuperUser(f):
        @wraps(f)
        def decorated(*args, **kwargs):
            if not current_user.is_authenticated:
                LOG.error("User isn't logged in.", exc_info=True)
                abort(403)

            if current_user.username != app.config['SUPERUSER_NAME']:
                LOG.error("The user doesn't have superuser access.",
                          exc_info=True)
                abort(403)
            return f(*args, **kwargs)
        return decorated

    @staticmethod
    def login_user(data):
        try:
            if current_user.is_authenticated:
                response_object = {
                    'status': 'Invalid',
                    'message': 'Already Logged In',
                }
                return response_object, 300
            user = User.query.filter_by(username=data.get('username')).first()
            if user is None:
                response_object = {
                    'status': 'fail',
                    'message': 'User does not exist. '
                }
                return response_object, 403
            if user and user.check_password(data.get('password')):
                if user.is_verified:
                    # convert string to bool
                    if data.get('remember').lower() == 'true' or data.get(
                            'remember').lower() == 'yes':
                        remem = True
                    else:
                        remem = False
                    flask_login_user(user, remember=remem)
                    response_object = {
                        'status': 'success',
                        'message': 'Successfully logged in.',
                    }

                    login_info = {
                        'id': current_user.id,
                        'username': current_user.username,
                    }
                    return login_info, 200
                else:
                    response_object = {
                        'status': 'fail',
                        'message': 'Please verify your email before first login',
                    }
                    return response_object, 402
            else:
                response_object = {
                    'status': 'fail',
                    'message': 'email or password does not match.',
                }
                return response_object, 401

        except BaseException:
            LOG.error('Login Failed', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def logout_user():
        try:
            if not current_user.is_authenticated:
                response_object = {
                    'status': 'Invalid',
                    'message': 'Not logged in',
                }
                return response_object, 400
            logout()
            response_object = {
                'status': 'success',
                'message': 'Logged Out Successfully',
            }
            return response_object, 200
        except BaseException:
            LOG.error('Logout Failed', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def signup_user(data, send_mail=True):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user is not None:
                response_object = {
                    'status': 'invalid',
                    'message': 'Email Already Registered',
                }
                LOG.info(
                    'Email already present in database. Redirect to Login Page')
                return response_object, 401
            user = User.query.filter_by(username=data.get('username')).first()
            if user is not None:
                response_object = {
                    'status': 'invalid',
                    'message': 'Username Already Taken',
                }
                LOG.info(
                    'Username %s already present in database. Ask to choose different username', data.get('username'))
                return response_object, 402

            user = User(data.get('username'),
                        data.get('password'), data.get('email'))

            if send_mail != "no":
                resp = Authentication.send_verification(data.get('email'))

                if resp[1] != 200:
                    User.query.filter_by(email=data.get('email')).delete()
                    db.session.commit()
                    raise BaseException

            response_object = {
                'status': 'success',
                'message': 'User added Successfully',
            }

            user.update_col('first_name', data.get('first_name'))
            user.update_col('last_name', data.get('last_name'))

            return response_object, 200

        except BaseException:
            LOG.error('User with email {} couldn\'t be Signed Up. Please try again'.format(
                data.get('email')), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def resend_verification(data):
        try:
            email = data.get('email')
            return Authentication.send_verification(email)
        except BaseException:
            LOG.error('Verification mail couldn\'t be sent', exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def send_verification(email):
        try:
            user = User.query.filter_by(email=email).first()
            if user is None:
                response_object = {
                    'status': 'error',
                    'message': 'User not present'
                }
                return response_object, 401

            if user.isVerified():
                response_object = {
                    'status': 'Error',
                    'message': 'Already verified'
                }
                return response_object, 403

            token = generate_confirmation_token(user.email)
            subject = "Minerva: Please confirm Email Address"
            confirm_url = url_for('api.auth_confirm_token',
                                  token=token, _external=True)
            print("Confirmation URL for {}: {}".format(
                user.username, confirm_url))
            async_send_mail(app._get_current_object(),
                            user.email, subject,
                            f"""Hey {user.username}<br/><br/>
Please use the below link to confirm your email address.<br/></br>
{confirm_url}<br/><br/><br/>
Mukul Mehta<br/>
Minerva""")

            response_object = {
                'status': 'Success',
                'Message': 'Verification Mail Sent successfully'
            }
            return response_object, 200

        except BaseException:
            LOG.error(
                'Verification Mail couldn\'t be sent to {}. Please try again'.format(email), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }

            return response_object, 500

    @staticmethod
    def confirm_token_service(token):
        try:
            email = confirm_token(token)
        except BaseException:
            LOG.info('The confirmation link has expired or is invalid')
            response_object = {
                'status': 'Fail',
                'message': 'Verification link is invalid or has expired',
            }
            return response_object, 400

        user = User.query.filter_by(email=email).first()
        if not user.is_verified:
            user.setVerified()
            response_object = {
                'status': 'Success',
                'message': 'Email Verified Successfully, head over to the homepage',
            }
        else:
            response_object = {
                'status': 'success',
                'message': 'Email Already Verified',
            }
        return response_object, 200

    @staticmethod
    def reset_password_mail(data):
        try:
            user = User.query.filter_by(email=data.get('email')).first()
            if user is None:
                LOG.info('User with email {} isn\'t registered.'.format(
                    data.get('email')))

                response_object = {
                    'status': 'fail',
                    'message': 'User is not registered'
                }
                return response_object, 401
            else:
                reset_token = generate_reset_token(data.get('email'))
                subject = "Minerva: Reset Password"
                reset_url = url_for('api.auth_reset_token_verify',
                                    token=reset_token, _external=True)
                async_send_mail(app._get_current_object(),
                                data.get('email'), subject,
                                f"""Hey {user.username}<br/><br/>
Please use the below link to reset your password.<br/></br>
{reset_url}<br/><br/><br/>
Minerva""")

            response_object = {
                'status': 'Success',
                'message': 'sent a password reset link on your registered email address.'
            }
            return response_object, 200
        except BaseException:
            LOG.error('Verification Mail couldn\'t be sent to {}. Please try again'.format(
                data.get('email')), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def confirm_reset_token_service(token):
        try:
            email = confirm_reset_token(token)
            print(email)
        except BaseException:
            LOG.info('The password reset link has expired or is invalid')
            response_object = {
                'status': 'Fail',
                'message': 'Password Reset link is invalid or has expired',
            }
            return response_object, 400
        form = PasswordForm()
        headers = {'Content-Type': 'text/html'}
        return make_response(render_template(
            'reset_password.html', form=form, token=token), 200, headers)

    @staticmethod
    def reset_password_with_token(token):
        """
        Take in password reset form from the user and change password.

        :param token: validation token
        :type token: str
        """
        try:
            email = confirm_reset_token(token)
        except BaseException:
            LOG.info('The password reset link has expired or is invalid')
            response_object = {
                'status': 'Fail',
                'message': 'Password Reset link is invalid or has expired',
            }
            return response_object, 400

        form = PasswordForm()
        if form.validate_on_submit():
            user = User.query.filter_by(email=email).first()
            user.resetPassword(form.password.data)
            response_object = {
                'status': 'Success',
                'message': 'Password has been reset successfully',
            }
            return response_object, 200

        return redirect(url_for('api.auth_reset_token_verify'), token=token)

    @staticmethod
    def change_user_password(data):
        try:
            user = User.query.filter_by(username=current_user.username).first()
            if not current_user.is_authenticated:
                response_object = {
                    'status': 'Invalid',
                    'message': 'Not logged in',
                }
                return response_object, 400

            if user.check_password(data.get('oldPassword')):
                user.resetPassword(data.get('newPassword'))
                response_object = {
                    'status': 'Success',
                    'message': 'Password changed successfully'
                }
                return response_object, 200

            LOG.warning("Password couldn\'t be changed since old password doesn't match for user {}.".format(
                user.username))
            response_object = {
                'status': 'Failed',
                'message': 'Password change failed.'
            }
            return response_object, 400

        except BaseException:
            LOG.error('Password couldn\'t be reset for user : {}'.format(
                current_user.username), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500
