from django.db import models
from django.conf import settings
from posts.models import Post


class PostLike(models.Model):
    """
    Model representing a like for a blog post by a user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="post_likes"
    )
    post = models.ForeignKey(
        Post,
        on_delete=models.CASCADE,
        related_name="post_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "post"],
                name="unique_post_like"
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} likes {self.post.title}"
        )
