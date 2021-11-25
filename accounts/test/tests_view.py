from rest_framework.test import APITestCase


class UserAccountTest(APITestCase):

    def test_created_superuser_success(self):
        superuser_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": True,
            "is_staff": True,
        }
        response_data = {
            "id": 1,
            "username": "user",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": True,
            "is_staff": True,
        }

        response = self.client.post('/api/accounts/', superuser_data)

        self.assertDictContainsSubset(response_data, response.json())

    def test_created_superuser_fail(self):
        superuser_data = {
            "password": "1234",
            "first_name": "John",
            "last_name": "Wick",
            "is_staff": True,
        }

        response = self.client.post('/api/accounts/', superuser_data)
        self.assertEqual(response.status_code, 400)

    def test_created_critic_user_success(self):
        critic_data = {
            "username": "user",
            "password": "1234",
            "first_name": "Arioscritc",
            "last_name": "Metamorfosis",
            "is_superuser": False,
            "is_staff": True,
        }
        user_response_data = {
            "id": 1,
            "username": "user",
            "first_name": "Arioscritc",
            "last_name": "Metamorfosis",
            "is_superuser": False,
            "is_staff": True,
        }

        response = self.client.post('/api/accounts/', critic_data)

        self.assertDictContainsSubset(user_response_data, response.json())

    def test_created_user_success(self):
        user_data = {
            "username": "user",
            "password": "1234",
            "first_name": "Altarius",
            "last_name": "Bonanza",
            "is_superuser": False,
            "is_staff": False,
        }
        response_data = {
            "id": 1,
            "username": "user",
            "first_name": "Altarius",
            "last_name": "Bonanza",
            "is_superuser": False,
            "is_staff": False,
        }

        response = self.client.post('/api/accounts/', user_data)

        self.assertDictContainsSubset(response_data, response.json())


class LoginTest(APITestCase):
    def test_login_superuser_success(self):
        superuser_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": True,
            "is_staff": True,
        }

        self.client.post('/api/accounts/', superuser_data)

        sign_up_data = {
            "username": "user",
            "password": "1234",
        }
        
        response = self.client.post('/api/login/', sign_up_data)
        self.assertEqual(response.status_code, 200)
        self.assertIn("token", response.json().keys())
        
    def test_login_superuser_error(self):
        superuser_data = {
            "username": "user",
            "password": "1234",
            "first_name": "John",
            "last_name": "Wick",
            "is_superuser": True,
            "is_staff": True,
        }

        self.client.post('/api/accounts/', superuser_data)

        sign_up_data = {
            "username": "user",
            "password": "    ",
        }

        response = self.client.post('/api/login/', sign_up_data)
        self.assertEqual(response.status_code, 400)
