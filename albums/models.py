from django.db import models
from users.models import User
from posts.models import Post


class Album(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="albums"
    )
    name = models.CharField(max_length=100)
    created_at = models.DateTimeField(auto_now_add=True)
    posts = models.ManyToManyField(
        Post, related_name="albums", blank=True)

    def __str__(self):
        return self.name
    