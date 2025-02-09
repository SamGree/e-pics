from django.db import models
from django.contrib.auth.models import AbstractUser
from cloudinary.models import CloudinaryField

# Create your models here.
class User(AbstractUser):
    """
    Custom User model that extends the default AbstractUser model.
    Includes additional fields for profile image, and user bio.
    """
    # Profile image stored using Cloudinary
    profile_image = CloudinaryField('profile_image', blank=True, null=True)
    # Optional bio field for user profiles
    bio = models.TextField(blank=True, null=True)


    def __str__(self):
        return self.username
