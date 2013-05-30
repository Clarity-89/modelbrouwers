from django.test import TestCase
from django.contrib.auth.models import User
from utils import get_username

class UsernameTest(TestCase):
    def setUp(self):
        class User(object):
            def __init__(self, username):
                super(User, self).__init__()
                self.username = username

        class TestObject(object):
            def __init__(self, username):
                super(TestObject, self).__init__()
                self.field = User(username)
                self.user = User(username)

        self.object1 = TestObject('BBT')
        self.object2 = TestObject('Joe_Silent')

    def test_username_correct(self):
        """
        Tests that underscores are converted to spaces
        """
        self.assertEqual(get_username(self.object1, field='field'), 'BBT')
        self.assertEqual(get_username(self.object2, field='field'), 'Joe Silent')
        self.assertEqual(get_username(self.object2), 'Joe Silent')