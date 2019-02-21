import unittest

from app import db

from app.models.user import User

class TestUserModel(unittest.TestCase):

    def setUp(self):
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        # self.app_context.pop()
