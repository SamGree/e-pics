from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from rest_framework.authtoken.models import Token

User = get_user_model()


class UserAPITest(TestCase):
    def setUp(self):
        """
        Set up test data for user API tests.
        """
        self.client = APIClient()

        # Create test user
        self.user = User.objects.create_user(username="testuser", password="testpassword", bio="This is a test bio")
        self.token = Token.objects.create(user=self.user)

        # Authentication headers
        self.auth_headers = {"HTTP_AUTHORIZATION": f"Token {self.token.key}"}

        # URLs
        self.register_url = reverse("register")
        self.login_url = reverse("login")
        self.logout_url = reverse("logout")
        self.profile_url = reverse("user-profile-detail", kwargs={"user_id": self.user.id})
        self.profile_update_url = reverse("profile-update")

    def test_register_user(self):
        """
        Test user registration with valid credentials.
        """
        data = {
            "username": "newuser",
            "password": "newpassword123",
            "password_again": "newpassword123",
            "bio": "New user bio"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["username"], "newuser")

    def test_register_user_with_existing_username(self):
        """
        Test user registration fails if the username already exists.
        """
        data = {
            "username": "testuser",  # Already taken username
            "password": "newpassword123",
            "password_again": "newpassword123"
        }
        response = self.client.post(self.register_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertIn("error", response.data)

    def test_login_user(self):
        """
        Test login with valid credentials.
        """
        data = {"username": "testuser", "password": "testpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("token", response.data)

    def test_login_invalid_credentials(self):
        """
        Test login fails with incorrect password.
        """
        data = {"username": "testuser", "password": "wrongpassword"}
        response = self.client.post(self.login_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_logout_user(self):
        """
        Test logging out an authenticated user.
        """
        response = self.client.post(self.logout_url, **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("message", response.data)

    def test_retrieve_user_profile(self):
        """
        Test retrieving user profile by ID.
        """
        response = self.client.get(self.profile_url, **self.auth_headers)  # Added authentication headers
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["user"]["username"], "testuser")

    def test_update_user_profile(self):
        """
        Test updating user profile details.
        """
        data = {"bio": "Updated bio"}
        response = self.client.patch(self.profile_update_url, data, format="json", **self.auth_headers)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["bio"], "Updated bio")

    def test_update_user_profile_unauthenticated(self):
        """
        Test that unauthenticated users cannot update profiles.
        """
        data = {"bio": "Unauthorized update"}
        response = self.client.patch(self.profile_update_url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN) 
