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


class TestUserSearch(BaseTestCase):

    def test_user_search(self):
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
            self.user_id = data['id']
            self.assertEqual(login_response.status_code, 200)

            self.url = "/user/{}".format(self.user_id)
            response = self.client.get(
                self.url
            )

            data = json.loads(response.data.decode())['resource']
            self.assertTrue(data['username'] == 'test_username')
            self.assertTrue(data['first_name'] == "")
            self.assertEqual(response.status_code, 200)

    def test_user_col_update(self):
        """ Test the /user/update [POST] endpoint """

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
            self.user_id = data['id']
            self.assertEqual(login_response.status_code, 200)

            response = self.client.post(
                '/user/update',
                data=json.dumps(dict(
                    first_name='Mukul',
                    last_name='Mehta',
                    dob=datetime.datetime.strptime("12 May 2000", "%d %b %Y")
                ), default=str),
                content_type='application/json'
            )

            print(response)

            self.url = "/user/{}".format(self.user_id)
            response = self.client.get(
                self.url
            )

            data = json.loads(response.data.decode())['resource']
            self.assertTrue(data['username'] == 'test_username')
            self.assertTrue(data['first_name'] == "Mukul")
            self.assertTrue(data['last_name'] == "Mehta")
            self.assertTrue(data['dob'] == "Fri, 12 May 2000 00:00:00 -0000")
            self.assertEqual(response.status_code, 200)


if __name__ == '__main__':
    unittest.main()
