from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from django.contrib.auth import get_user_model
from posts.models import Post
from posttags.models import PostTag
from tags.models import Tag

User = get_user_model()


class PostAPITest(TestCase):
    def setUp(self):
        """
        Set up test data for posts API tests.
        """
        self.client = APIClient()

        # Create test users
        self.user = User.objects.create_user(username="testuser", password="testpassword")
        self.other_user = User.objects.create_user(username="otheruser", password="otherpassword")

        # Authenticate as the first user
        self.client.force_authenticate(user=self.user)

        # Create a test post
        self.post = Post.objects.create(
            title="Test Post",
            description="This is a test description",
            user=self.user
        )

        # Create a test tag
        self.tag = Tag.objects.create(name="TestTag")
        self.post_tag = PostTag.objects.create(post=self.post, tag=self.tag)

    def test_list_posts(self):
        """
        Test the retrieval of a list of posts.
        """
        url = reverse("list-create-posts")
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Post")

    def test_create_post(self):
        """
        Test the creation of a new post.
        """
        url = reverse("list-create-posts")
        data = {
            "title": "New Post",
            "description": "New description",
            "tags[]": ["NewTag"]
        }
        response = self.client.post(url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data["title"], "New Post")
        self.assertIn("NewTag", response.data["tags"])

    def test_retrieve_post(self):
        """
        Test retrieving a specific post by ID.
        """
        url = reverse("detail-post", kwargs={"post_id": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["post"]["title"], "Test Post")

    def test_update_post(self):
        """
        Test updating a post by the owner.
        """
        url = reverse("detail-post", kwargs={"post_id": self.post.id})
        data = {"title": "Updated Title"}
        response = self.client.patch(url, data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["title"], "Updated Title")

    def test_delete_post(self):
        """
        Test deleting a post by the owner.
        """
        url = reverse("detail-post", kwargs={"post_id": self.post.id})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Post.objects.count(), 0)

    def test_unauthenticated_post_creation(self):
        """
        Test that an unauthenticated user cannot create a post.
        """
        self.client.force_authenticate(user=None)
        url = reverse("list-create-posts")
        data = {"title": "Unauthenticated Post", "description": "No auth"}
        response = self.client.post(url, data)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_post_download(self):
        """
        Test the download functionality of a post.
        """
        url = reverse("post-download", kwargs={"post_id": self.post.id})
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn("download_url", response.data)
        self.assertEqual(response.data["download_count"], 1)

    def test_search_posts(self):
        """
        Test searching for posts by title, username, or tags.
        """
        url = reverse("search")
        response = self.client.get(url, {"q": "Test"})
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]["title"], "Test Post")
