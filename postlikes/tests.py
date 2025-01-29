from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from postlikes.models import PostLike

User = get_user_model()

class PostLikeModelTest(TestCase):

    def setUp(self):
        """
        Set up test data for PostLike model tests.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a second test user
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')

        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post',
            user=self.user
        )

    def test_postlike_creation(self):
        """
        Test that a PostLike can be created.
        """
        post_like = PostLike.objects.create(user=self.other_user, post=self.post)
        self.assertEqual(post_like.user, self.other_user)
        self.assertEqual(post_like.post, self.post)
        self.assertTrue(post_like.created_at is not None)

    def test_postlike_unique_constraint(self):
        """
        Test the unique constraint on user and post.
        """
        # Create a PostLike
        PostLike.objects.create(user=self.other_user, post=self.post)

        # Attempt to create a duplicate PostLike
        with self.assertRaises(Exception):
            PostLike.objects.create(user=self.other_user, post=self.post)

    def test_postlike_related_name_for_user(self):
        """
        Test that the related_name 'post_likes' works for User.
        """
        post_like = PostLike.objects.create(user=self.other_user, post=self.post)
        self.assertIn(post_like, self.other_user.post_likes.all())

    def test_postlike_related_name_for_post(self):
        """
        Test that the related_name 'post_likes' works for Post.
        """
        post_like = PostLike.objects.create(user=self.other_user, post=self.post)
        self.assertIn(post_like, self.post.post_likes.all())

    def test_postlike_str_representation(self):
        """
        Test the __str__ method of the PostLike model.
        """
        post_like = PostLike.objects.create(user=self.other_user, post=self.post)
        self.assertEqual(str(post_like), f'{self.other_user.username} likes {self.post.title}')
