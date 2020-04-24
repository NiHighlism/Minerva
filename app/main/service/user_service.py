"""for user related operations"""

import datetime
from logging import getLogger

from flask_login import current_user

from app.main import db
from app.main.models.movies import Movie
from app.main.models.users import User

LOG = getLogger(__name__)


class UserService:

    @staticmethod
    def get_by_username(username):
        try:
            user = User.query.filter_by(username=username).first()
            if user is None:
                LOG.info('User with username: {} does not exit'.format(username))
                response_object = {
                    'status': 'Invalid',
                    'message': 'User does not exist'
                }
                return response_object, 400
            return user, 200

        except Exception as e:
            LOG.error('Failed to fetch details for username :{}'.format(
                username), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def update_user_info(update_dict):
        LOG.info('update_dict for user {}: {}'.format(
            current_user.username, update_dict))
        try:
            user = User.query.filter_by(id=current_user.id).first()
            if user is None:
                LOG.info(
                    'User with id: {} does not exit'.format(
                        current_user.id))
                response_object = {
                    'status': 'Invalid',
                    'message': 'User does not exist'
                }
                return response_object, 300

            for key in update_dict:
                user.update_col(key, update_dict[key])

            response_object = {
                'status': 'Success',
                'message': 'Details updated Successfully'
            }
            return response_object, 200

        except Exception:
            LOG.error('Failed to update details for id :{}'.format(
                current_user.id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500

    @staticmethod
    def save_user_payment(data):
        try:
            user = User.query.filter_by(id=current_user.id).first()
            if user is None:
                LOG.info(
                    'User with id: {} does not exit'.format(
                        current_user.id))
                response_object = {
                    'status': 'Invalid',
                    'message': 'User does not exist'
                }
                return response_object, 300

            current_user.addPayment(data)
            response_object = {
                'status': 'Success',
                'message': 'Saved the payment into the users information.'
            }
            return response_object, 200

        except BaseException:
            LOG.error('Failed to save payment details for id :{}'.format(
                current_user.id), exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again',
            }
            return response_object, 500


    @staticmethod
    def add_to_movie_list(imdb_ID):
        try:
            user = User.query.filter_by(id=current_user.id).first()
            movie = Movie.query.filter_by(imdb_ID=imdb_ID).first()

            movie_list = user.movie_list

            if movie not in movie_list:
                user.add_to_movie_list(imdb_ID)
            
            user = User.query.filter_by(id=current_user.id).first()

            movie_list = user.movie_list
            return movie_list, 200
        except Exception:
            LOG.error("Movie couldn't be added to List.", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500


    @staticmethod
    def get_movie_list(id):
        user = User.query.filter_by(id=id).first()
        
        movie_list = [movie for movie in user.movie_list]
        return movie_list, 200