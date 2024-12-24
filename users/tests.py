from django.test import TestCase
from rest_framework.test import APIClient
from rest_framework import status
from .models import User
from .serializers import UserSerializer
from rest_framework.authtoken.models import Token

class UserModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username="testuser", password="password123", bio="Test bio")

    def test_user_creation(self):
        self.assertEqual(self.user.username, "testuser")
        self.assertTrue(self.user.check_password("password123"))
        self.assertEqual(self.user.bio, "Test bio")

    def test_user_str(self):
        self.assertEqual(str(self.user), "testuser")


class UserSerializerTestCase(TestCase):
    def setUp(self):
        self.valid_data = {
            "username": "testuser",
            "password": "password123",
            "password_again": "password123",
            "bio": "Test bio"
        }

        self.invalid_data = {
            "username": "",
            "password": "password123",
            "password_again": "password1234"
        }

    def test_serializer_valid_data(self):
        serializer = UserSerializer(data=self.valid_data)
        self.assertTrue(serializer.is_valid())

    def test_serializer_invalid_data(self):
        serializer = UserSerializer(data=self.invalid_data)
        self.assertFalse(serializer.is_valid())
        self.assertIn("username", serializer.errors)  # Check for the specific field error
        self.assertIn("This field may not be blank.", str(serializer.errors["username"]))


class UserViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(username="testuser", password="password123")
        self.token = Token.objects.create(user=self.user)

        self.register_url = "/users/register"
        self.login_url = "/users/login"
        self.logout_url = "/users/logout"
        self.profile_url = f"/users/profile/{self.user.id}"
        self.update_url = "/users/profile/update"

    def test_register_view_success(self):
        data = {
            "username": "newuser",
            "password": "password123",
            "password_again": "password123",
            "bio": "New user bio"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_register_view_failure(self):
        data = {
            "username": "",
            "password": "password123",
            "password_again": "password1234"
        }
        response = self.client.post(self.register_url, data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_login_view_success(self):
        data = {
            "username": "testuser",
            "password": "password123"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_view_failure(self):
        data = {
            "username": "testuser",
            "password": "wrongpassword"
        }
        response = self.client.post(self.login_url, data)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_view_success(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.post(self.logout_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_user_profile_detail_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        response = self.client.get(self.profile_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("user", response.data)  # Ensure "user" key exists
        self.assertEqual(response.data["user"]["username"], self.user.username)

    def test_user_profile_update_view(self):
        self.client.credentials(HTTP_AUTHORIZATION=f"Token {self.token.key}")
        data = {"bio": "Updated bio"}
        response = self.client.patch(self.update_url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user.refresh_from_db()
        self.assertEqual(self.user.bio, "Updated bio")
