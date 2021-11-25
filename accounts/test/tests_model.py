from accounts.models import User
from django.test import TestCase


class UserModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.username = 'user'
        cls.password = '1234'
        cls.first_name = 'Jhon'
        cls.last_name = 'Wick'
        cls.is_superuser = False
        cls.is_staff = False

        cls.user = User.objects.create_user(
            username=cls.username,
            password=cls.password,
            first_name=cls.first_name,
            last_name=cls.last_name,
            is_superuser=cls.is_superuser,
            is_staff=cls.is_staff
        )

    def test_user_fields(self):
        self.assertIsInstance(self.user.username, str)
        self.assertEqual(self.user.username, self.username)

        self.assertIsInstance(self.user.password, str)

        self.assertIsInstance(self.user.first_name, str)
        self.assertEqual(self.user.first_name, self.first_name)

        self.assertIsInstance(self.user.last_name, str)
        self.assertEqual(self.user.last_name, self.last_name)

        self.assertIsInstance(self.user.is_superuser, bool)
        self.assertEqual(self.user.is_superuser, self.is_superuser)

        self.assertIsInstance(self.user.is_staff, bool)
        self.assertEqual(self.user.is_staff, self.is_staff)
