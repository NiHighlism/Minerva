import datetime
import json
import unittest

from app.main import db
from app.test.base import BaseTestCase
from app.main.util.sendgrid import send_mail


class TestMisc(BaseTestCase):

    def test_send_mail(self):
        response_object, status = send_mail("test@example.com", "Test Mail", "This is a testing Mail")
        self.assertTrue(response_object['status'] == 'success')
        self.assertTrue(status == 200)

if __name__ == '__main__':
    unittest.main()