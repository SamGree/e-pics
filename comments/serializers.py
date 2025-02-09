from rest_framework import serializers
from .models import Comment
from urllib.parse import urljoin


class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model, including user details
    and likes count for each comment.
    """
    author = serializers.CharField(source='user.username', read_only=True)
    author_image = serializers.SerializerMethodField()
    post = serializers.PrimaryKeyRelatedField(read_only=True)
    likes_count = serializers.SerializerMethodField()
    is_liked = serializers.SerializerMethodField()

    class Meta:
        model = Comment
        fields = [
            'id', 'content', 'author', 'author_image', 'post', 'created_at',
            'likes_count', 'is_liked']
        read_only_fields = ['id', 'user', 'post', 'created_at']

    def get_likes_count(self, obj):
        return obj.comment_likes.count()

    def get_author_image(self, obj):
        if obj.user.profile_image:
            return urljoin(
                "https://res.cloudinary.com/", obj.user.profile_image.url
                )
        return None

    def get_is_liked(self, obj):
        """
        Check if the logged-in user has liked the post.
        """
        request = self.context.get('request', None)
        if request and request.user.is_authenticated:
            return obj.likes.filter(pk=request.user.pk).exists()
        return False
