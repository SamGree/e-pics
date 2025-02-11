from django.test import TestCase
from django.contrib.auth import get_user_model
from albums.models import Album
from posts.models import Post

User = get_user_model()


class AlbumModelTest(TestCase):

    def setUp(self):
        """
        Set up test data for Album model tests.
        """
        # Create a test user
        self.user = User.objects.create_user(
            username='testuser',
            password='testpassword'
        )
        # Create a test post
        self.post = Post.objects.create(
            title='Test Post',
            description='This is a test post',
            user=self.user
        )
        # Create an album
        self.album = Album.objects.create(
            user=self.user,
            name='Test Album'
        )
        # Add the post to the album
        self.album.posts.add(self.post)

    def test_album_creation(self):
        """
        Test that an album is created with correct data.
        """
        self.assertEqual(self.album.name, 'Test Album')
        self.assertEqual(self.album.user, self.user)
        self.assertTrue(self.album.created_at is not None)

    def test_album_posts_relationship(self):
        """
        Test the ManyToMany relationship between Album and Post.
        """
        self.assertIn(self.post, self.album.posts.all())
        self.assertIn(self.album, self.post.albums.all())

    def test_album_string_representation(self):
        """
        Test the __str__ method of the Album model.
        """
        self.assertEqual(str(self.album), 'Test Album')

    def test_related_name_for_user(self):
        """
        Test that the related_name 'albums' works for the User model.
        """
        self.assertIn(self.album, self.user.albums.all())

    def test_related_name_for_post(self):
        """
        Test that the related_name 'albums' works for the Post model.
        """
        self.assertIn(self.album, self.post.albums.all())

    def test_album_name_max_length(self):
        """
        Test the max_length constraint for the name field.
        """
        max_length = Album._meta.get_field('name').max_length
        self.assertEqual(max_length, 100)
