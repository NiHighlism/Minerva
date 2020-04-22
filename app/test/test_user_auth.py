import datetime
import json
import unittest

from app.main import db
from app.main.models.users import User
from app.test.base import BaseTestCase


def add_user(self):
    return self.client.post(
        '/auth/signup?send_mail=no',
        data=json.dumps(dict(
            email='example@gmail.com',
            username='test_username',
            password='test_passwd'
        )),
        content_type='application/json'
    )


def login_user(self):
    return self.client.post(
        '/auth/login',
        data=json.dumps(dict(
            email='example@gmail.com',
            password='test_passwd',
            remember="No"
        )),
        content_type='application/json'
    )


class TestAuth(BaseTestCase):

    def test_user_login(self):
        """ Test for login of registered-user login """

        with self.client:
            user_response = add_user(self)
            response_data = json.loads(user_response.data.decode())
            self.assertTrue(response_data['status'] == 'success')
            self.assertEqual(user_response.status_code, 200)

            user = User.query.filter_by(email="example@gmail.com").first()
            user.is_verified = 1
            db.session.commit()

            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            self.assertTrue(data['username'] == "test_username")
            self.assertEqual(login_response.status_code, 200)

    def test_valid_logout(self):
        """ Test for logout """
        with self.client:
            # registered user login
            user_response = add_user(self)
            response_data = json.loads(user_response.data.decode())
            self.assertTrue(response_data['status'])
            self.assertEqual(user_response.status_code, 200)

            user = User.query.filter_by(email="example@gmail.com").first()
            user.is_verified = 1
            db.session.commit()

            login_response = login_user(self)
            data = json.loads(login_response.data.decode())
            self.assertEqual(login_response.status_code, 200)

            # valid token logout
            response = self.client.get(
                '/auth/logout',
            )

            data = json.loads(response.data.decode())
            self.assertTrue(data['status'] == 'success')
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
