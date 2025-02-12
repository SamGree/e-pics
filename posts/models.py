from django.db import models
from django.db import models
from users.models import User
from django.conf import settings
from cloudinary.models import CloudinaryField


class Post(models.Model):
    """
    Model representing a blog post, including title, description,
    associated user, and related likes.
    """
    title = models.CharField(max_length=100)
    description = models.TextField()
    image = CloudinaryField('image')  # Image uploaded via Cloudinary
    download_count = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, related_name='posts', on_delete=models.CASCADE)
    likes = models.ManyToManyField(
        settings.AUTH_USER_MODEL, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Post"
        verbose_name_plural = "Posts"

    def __str__(self):
        return self.title
        