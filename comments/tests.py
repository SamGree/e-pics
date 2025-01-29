from django.test import TestCase
from django.contrib.auth import get_user_model
from posts.models import Post
from comments.models import Comment

User = get_user_model()

class CommentModelTest(TestCase):

    def setUp(self):
        """
        Set up test data for Comment model tests.
        """
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a second test user
        self.other_user = User.objects.create_user(username='otheruser', password='otherpassword')

        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            description='Test post description',
            user=self.user
        )

        # Create a test comment
        self.comment = Comment.objects.create(
            content='This is a test comment',
            user=self.user,
            post=self.post
        )

    def test_comment_creation(self):
        """
        Test that a comment can be created.
        """
        self.assertEqual(self.comment.content, 'This is a test comment')
        self.assertEqual(self.comment.user, self.user)
        self.assertEqual(self.comment.post, self.post)
        self.assertTrue(self.comment.created_at is not None)

    def test_comment_related_name_for_post(self):
        """
        Test that the related_name 'comments' works for Post.
        """
        self.assertIn(self.comment, self.post.comments.all())

    def test_comment_related_name_for_user(self):
        """
        Test that the related_name 'comments' works for User.
        """
        self.assertIn(self.comment, self.user.comments.all())

    def test_comment_str_representation(self):
        """
        Test the __str__ method of the Comment model.
        """
        expected_str = f'Comment by {self.user.username} on {self.post.title}'
        self.assertEqual(str(self.comment), expected_str)

    def test_comment_likes_relationship(self):
        """
        Test the many-to-many relationship for comment likes.
        """
        # Add a like to the comment
        self.comment.likes.add(self.other_user)

        # Check that the user is in the likes
        self.assertIn(self.other_user, self.comment.likes.all())

        # Check the related_name 'liked_comments' for the user
        self.assertIn(self.comment, self.other_user.liked_comments.all())

