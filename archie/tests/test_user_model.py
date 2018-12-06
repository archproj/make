
import unittest
import time
from datetime import datetime
from app import create_app, db
from app.models import Role, User, Question, Comment, Answer


class UserModelTestCase(unittest.TestCase):

    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()
        Role.insert_roles()


    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()


    def test_user_slack_id(self):
        u = User(slack_id = 'X1245678')

