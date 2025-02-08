from rest_framework import serializers
from .models import Album
from posts.serializers import PostSerializer


class AlbumSerializer(serializers.ModelSerializer):
    posts = PostSerializer(many=True, read_only=True)
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())

    class Meta:
        model = Album
        fields = ['id', 'name', 'created_at', 'user', 'posts']
        read_only_fields = ['id', 'created_at']
        