"""for user related operations"""

import datetime
from logging import getLogger
from random import sample

from sqlalchemy.orm.exc import NoResultFound

from app.main import db
from app.main.models.enums import PriorityType
from app.main.models.users import User
from flask_login import current_user

LOG = getLogger(__name__)


TAG_ID_INDEX = 1


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
        LOG.info('update_dict for user {}: {}'.format(current_user.username, update_dict))
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
