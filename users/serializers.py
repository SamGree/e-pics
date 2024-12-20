from rest_framework import serializers
from .models import User

class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for the User model, handling validation, creation, and updating of user data.
    Includes additional logic for handling profile image uploads via Cloudinary.
    """
    password_again = serializers.CharField(write_only=True)
    profile_image = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'password_again', 'profile_image', 'bio']