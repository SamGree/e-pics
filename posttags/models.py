from django.db import models
from posts.models import Post
from tags.models import Tag

class PostTag(models.Model):
    """
    Model representing the relationship between a post and a tag.
    """
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='post_tags')
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE, related_name='post_tags')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        constraints = [
            models.UniqueConstraint(fields=['post', 'tag'], name='unique_post_tag')
        ]

    def __str__(self):
        return f'{self.tag.name} tagged in {self.post.title}'

