from rest_framework.views import APIView
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
    permission_classes = [IsAuthenticatedOrReadOnly]
    def post(self, request, post_id):
        """
        Toggle like/unlike a specific post.
        """
        try:
            post = Post.objects.get(id=post_id)
            like, created = PostLike.objects.get_or_create(user=request.user, post=post)
            if created:
                post.likes.add(request.user)
                return Response({'message': 'Post liked.'}, status=status.HTTP_201_CREATED)
            else:
                post.likes.remove(request.user)
                like.delete()
                return Response({'message': 'Like removed from post.'}, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found.'}, status=status.HTTP_404_NOT_FOUND)
        
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

