from rest_framework import serializers
from .models import PostTag


class PostTagSerializer(serializers.ModelSerializer):
    tag_name = serializers.CharField(source='tag.name', read_only=True)

    class Meta:
        model = PostTag
        fields = ['id', 'post', 'tag', 'tag_name', 'created_at']
        read_only_fields = ['id', 'created_at']
