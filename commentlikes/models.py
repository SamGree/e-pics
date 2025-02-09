from django.db import models
from django.conf import settings
from comments.models import Comment


class CommentLike(models.Model):
    """
    Model representing a like for a comment by a user.
    """

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="comment_likes"
    )
    comment = models.ForeignKey(
        Comment,
        on_delete=models.CASCADE,
        related_name="comment_likes"
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=["user", "comment"],
                name="unique_comment_like"
            )
        ]

    def __str__(self):
        return (
            f"{self.user.username} likes comment {self.comment.id}"
        )
