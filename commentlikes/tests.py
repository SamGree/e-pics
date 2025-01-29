from django.test import TestCase
from django.contrib.auth import get_user_model
from comments.models import Comment
from posts.models import Post
from commentlikes.models import CommentLike

User = get_user_model()

class CommentLikeModelTest(TestCase):

    def setUp(self):
        """
        Set up test data for CommentLike model tests.
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

    def test_commentlike_creation(self):
        """
        Test that a CommentLike can be created.
        """
        comment_like = CommentLike.objects.create(user=self.other_user, comment=self.comment)
        self.assertEqual(comment_like.user, self.other_user)
        self.assertEqual(comment_like.comment, self.comment)

    def test_commentlike_unique_constraint(self):
        """
        Test that the unique constraint on user and comment works.
        """
        # Create a CommentLike
        CommentLike.objects.create(user=self.other_user, comment=self.comment)

        # Attempt to create a duplicate CommentLike
        with self.assertRaises(Exception):
            CommentLike.objects.create(user=self.other_user, comment=self.comment)

    def test_commentlike_related_name_for_user(self):
        """
        Test that the related_name 'comment_likes' works for User.
        """
        comment_like = CommentLike.objects.create(user=self.other_user, comment=self.comment)
        self.assertIn(comment_like, self.other_user.comment_likes.all())

    def test_commentlike_related_name_for_comment(self):
        """
        Test that the related_name 'comment_likes' works for Comment.
        """
        comment_like = CommentLike.objects.create(user=self.other_user, comment=self.comment)
        self.assertIn(comment_like, self.comment.comment_likes.all())

    def test_commentlike_str_representation(self):
        """
        Test the __str__ method of the CommentLike model.
        """
        comment_like = CommentLike.objects.create(user=self.other_user, comment=self.comment)
        self.assertEqual(str(comment_like), f'{self.other_user.username} likes comment {self.comment.id}')
