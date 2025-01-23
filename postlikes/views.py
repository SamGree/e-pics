from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from posts.views import IsAuthenticatedOrReadOnly
from rest_framework import status
from .models import PostLike
from posts.models import Post
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posts.serializers import PostSerializer



class PostLikeView(APIView):
    """
    API view for liking or unliking a post.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, post_id):
        post = get_object_or_404(Post, id=post_id)

        if request.user in post.likes.all():
            # User unliked the post
            post.likes.remove(request.user)
            likes_count = post.likes.count()
            return Response({
                'message': 'Like removed from post.',
                'likes_count': likes_count,
                'is_liked': False,
            }, status=status.HTTP_200_OK)
        else:
            # User liked the post
            post.likes.add(request.user)
            likes_count = post.likes.count()
            return Response({
                'message': 'Post liked.',
                'likes_count': likes_count,
                'is_liked': True,
            }, status=status.HTTP_201_CREATED)


class LikedPostsView(APIView):
    """
    API view for retrieving all posts liked by the authenticated user.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        
        liked_post_ids = PostLike.objects.filter(user=user).values_list('post_id', flat=True)
        liked_posts = Post.objects.filter(id__in=liked_post_ids)
        serializer = PostSerializer(liked_posts, many=True, context={'request': request})
        return Response(serializer.data, status=200)

