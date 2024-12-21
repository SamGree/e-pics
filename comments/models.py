from django.db import models
from django.conf import settings
from posts.models import Post

class Comment(models.Model):
    """
    Model representing a comment on a blog post, associated with a user and a post.
    """
    content = models.TextField()
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='comments')
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True)
    likes = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='liked_comments', blank=True)

    def __str__(self):
        return f'Comment by {self.user.username} on {self.post.title}'
