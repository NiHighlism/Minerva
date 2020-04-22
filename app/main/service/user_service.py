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
    def get_by_id(id):
        try:
            user = User.query.filter_by(id=id).first()
            if user is None:
                LOG.info('User with id: {} does not exit'.format(id))
                response_object = {
                    'status': 'Invalid',
                    'message': 'User does not exist'
                }
                return response_object, 300
            return user, 200

        except Exception as e:
            LOG.error('Failed to fetch details for id :{}'.format(
                'id'), exc_info=True)
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
    def add_to_watch_list(imdb_ID):
        try:
            user = User.query.filter_by(id=current_user.id).first()
            movie = Movie.query.filter_by(imdb_ID=imdb_ID).first()

            watch_list = user.watch_list

            if movie in watch_list:
                response_object = {
                    'status': 'success',
                    'message': 'Movie exists already in watch list'
                }
                return response_object, 200

            user.add_to_watch_list(imdb_ID)
            response_object = {
                'status': 'success',
                'message': 'Movie added successfully'
            }

            return response_object, 200

        except Exception:
            LOG.error("Movie couldn't be added to List.", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500

    @staticmethod
    def add_to_bucket_list(imdb_ID):
        try:
            user = User.query.filter_by(id=current_user.id).first()
            movie = Movie.query.filter_by(imdb_ID=imdb_ID).first()

            bucket_list = user.bucket_list

            if movie in bucket_list:
                response_object = {
                    'status': 'success',
                    'message': 'Movie exists already in bucket list'
                }
                return response_object, 200

            user.add_to_bucket_list(imdb_ID)

        except Exception:
            LOG.error("Movie couldn't be added to List.", exc_info=True)
            response_object = {
                'status': 'fail',
                'message': 'Try again later. '
            }

            return response_object, 500
