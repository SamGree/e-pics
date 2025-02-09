from django.shortcuts import render
from rest_framework.views import APIView
from comments.models import Comment
from posts.views import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import CommentLike, Comment


class CommentLikeView(APIView):
    """
    API view for liking or unliking a specific comment.
    """
    permission_classes = [IsAuthenticated]

    def post(self, request, comment_id):
        """
        Handle POST request to like or unlike a comment.
        """
        try:
            comment = Comment.objects.get(id=comment_id)

            if comment.user == request.user:
                return Response(
                    {'error': 'You cannot like your own comment.'},
                    status=status.HTTP_400_BAD_REQUEST
                )
            like, created = CommentLike.objects.get_or_create(
                user=request.user, comment=comment)

            if created:
                comment.likes.add(request.user)
                is_liked = True
                likes_count = comment.likes.count()
                return Response({
                    'message': 'Comment liked.',
                    'is_liked': is_liked,
                    'likes_count': likes_count,
                }, status=status.HTTP_201_CREATED)
            else:
                comment.likes.remove(request.user)
                like.delete()
                is_liked = False
                likes_count = comment.likes.count()
                return Response({
                    'message': 'Like removed from comment.',
                    'is_liked': is_liked,
                    'likes_count': likes_count,
                }, status=status.HTTP_200_OK)
        except Comment.DoesNotExist:
            return Response(
                {'error': 'Comment not found.'},
                status=status.HTTP_404_NOT_FOUND
                )
