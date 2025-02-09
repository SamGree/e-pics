from django.db import models


# Create your models here.
class Tag(models.Model):
    """
    Model representing a tag that can be associated with posts.
    """
    name = models.CharField(max_length=50, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
