import unittest
import datetime


from app.main import db
from app.main.models.users import User
from app.test.base import BaseTestCase


class TestUserModel(BaseTestCase):

    def test_user_model(self):

        user = User(
            username="test123",
            email='test@test.com',
            password='idk@test'
        )
        
        db.session.add(user)
        
        userRes = User.query.filter_by(username="test123").first()
        self.assertTrue(isinstance(userRes, User))



if __name__ == '__main__':
    unittest.main()