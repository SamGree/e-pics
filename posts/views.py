from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import BasePermission, SAFE_METHODS
from .models import Post
from .serializers import PostSerializer
from comments.serializers import CommentSerializer
from comments.models import Comment
from albums.serializers import AlbumSerializer
from albums.models import Album
from django.db.models import Q
from django.shortcuts import get_object_or_404
from cloudinary.uploader import destroy as cloudinary_destroy
from rest_framework.parsers import MultiPartParser, FormParser

class IsAuthenticatedOrReadOnly(BasePermission):
    """
    Custom permission allowing read-only access to unauthenticated users
    and full access to authenticated users.
    """
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True
        return request.user and request.user.is_authenticated

class PostListCreateView(APIView):
    """
    API view for listing all posts or creating a new post.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]
    
    # parser_classes = [MultiPartParser, FormParser]

    def get(self, request):
        """
        Retrieve a list of all posts.
        """
        posts = Post.objects.all()
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
    

    def post(self, request, *args, **kwargs):
        """
        Create a new post. Requires authentication.
        """
        serializer = PostSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PostDetailView(APIView):
    """
    API view for retrieving, updating, or deleting a single post.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, post_id):
        """
        Retrieve a single post along with its comments.
        """
        try:
            post = Post.objects.get(id=post_id)
            post_serializer = PostSerializer(post, context={'request': request})
            comments = Comment.objects.filter(post=post)
            comment_serializer = CommentSerializer(comments, many=True, context={'request': request})
            
            if request.user.is_authenticated:
                user_albums = Album.objects.filter(user=request.user)
                album_serializer = AlbumSerializer(user_albums, many=True)
            else:
                album_serializer = AlbumSerializer([], many=True)
            return Response({
                'post': post_serializer.data,
                'comments': comment_serializer.data,
                'albums': album_serializer.data
            }, status=status.HTTP_200_OK)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, post_id):
        """
        Update a specific post owned by the authenticated user.
        """
        try:
            post = Post.objects.get(id=post_id, user=request.user)
            serializer = PostSerializer(post, data=request.data, partial=True, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        except Post.DoesNotExist:
            return Response({'error': 'Post not found or not owned by user'}, status=status.HTTP_404_NOT_FOUND)


    def delete(self, request, post_id):
        """
        Delete a specific post owned by the authenticated user.
        """
        try:
            post = Post.objects.get(id=post_id, user=request.user)

            public_id = post.image.public_id
            cloudinary_destroy(public_id)

            post.delete()
            return Response({'message': 'Post deleted successfully'}, status=status.HTTP_200_OK)
        
        except Post.DoesNotExist:
            return Response({'error': 'Post not found or not owned by user'}, status=status.HTTP_404_NOT_FOUND)

class PostDownloadView(APIView):
    """
    API view for downloading a post's image and tracking download count.
    """
    def get(self, request, post_id):
        """
        Increment the download count and return the image URL.
        """
        post = get_object_or_404(Post, id=post_id)

        post.download_count += 1
        post.save()

        return Response({'download_url': post.image.url, 'download_count': post.download_count}, status=status.HTTP_200_OK)

class SearchView(APIView):
    """
    API view for searching posts based on title, username, or tags.
    """
    def get(self, request):
        query = request.query_params.get('q', '').strip()
        
        if not query:
            return Response({"message": "Enter a search term."}, status=status.HTTP_400_BAD_REQUEST)
        
        # Filter posts by title, author's username, or tags
        posts = Post.objects.filter(
            Q(title__icontains=query) |
            Q(user__username__icontains=query) |
            Q(post_tags__tag__name__icontains=query)
        ).distinct()
        
        serializer = PostSerializer(posts, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)
