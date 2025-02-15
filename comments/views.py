from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Comment
from .serializers import CommentSerializer
from posts.views import IsAuthenticatedOrReadOnly
from posts.models import Post


class CommentCreateView(APIView):
    """
    API view for creating a comment on a specific post.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def post(self, request, post_id):
        """
        Handle POST request to create a new comment for a given post.
        """
        try:
            post = Post.objects.get(id=post_id)
            serializer = CommentSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save(user=request.user, post=post)
                return Response(
                    serializer.data, status=status.HTTP_201_CREATED)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response(
                {'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)


class CommentUpdateView(APIView):
    """
    API view for updating or deleting a specific comment.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def patch(self, request, comment_id):
        """
        Handle PATCH request to partially update a comment.
        Only the owner of the comment can perform this action.
        """
        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
            serializer = CommentSerializer(
                comment, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(
                serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Comment not found or not owned by user'},
                status=status.HTTP_404_NOT_FOUND)

    def delete(self, request, comment_id):

        try:
            comment = Comment.objects.get(id=comment_id, user=request.user)
            comment.delete()
            return Response(
                {'message': 'Comment deleted successfully.'},
                status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Comment not found or not owned by user.'},
                status=status.HTTP_404_NOT_FOUND)


class PostCommentsView(APIView):
    """
    Class-based view for fetching all comments for a specific post.
    URL: /comments/<post_id>/
    """

    def get(self, request, post_id):
        comments = Comment.objects.filter(
            id=post_id).order_by('-created_at')
        if comments.exists():
            serializer = CommentSerializer(comments, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response({'message': 'No comments found for this post.'},
                        status=status.HTTP_204_NO_CONTENT)        
