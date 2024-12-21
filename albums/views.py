from posts.views import IsAuthenticatedOrReadOnly
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Album
from .serializers import AlbumSerializer
from django.shortcuts import get_object_or_404
from posts.models import Post

class AlbumListCreateView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required to view albums"}, status=status.HTTP_401_UNAUTHORIZED)
        
        albums = Album.objects.filter(user=request.user)
        serializer = AlbumSerializer(albums, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        try:
            data = request.data
            print(f'Request data: {data}')
            data['user'] = request.user.id
            print(f'Request user data: {data['user']}')
            
            serializer = AlbumSerializer(data=data, context={'request': request})
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        except AttributeError:
            return Response({'error': 'Invalid or missing data in the request body'}, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            return Response({'error': f'An unexpected error occurred: {str(e)}'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class AlbumDetailView(APIView):
    permission_classes = [IsAuthenticatedOrReadOnly]

    def get(self, request, album_id):
        if not request.user.is_authenticated:
            return Response({"error": "Authentication required to view albums"}, status=status.HTTP_401_UNAUTHORIZED)
        album = Album.objects.filter(id=album_id, user=request.user).first()
        if not album:
            return Response({"error": "Album not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AlbumSerializer(album)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def patch(self, request, album_id):
        album = Album.objects.filter(id=album_id, user=request.user).first()
        if not album:
            return Response({"error": "Album not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)
        serializer = AlbumSerializer(album, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, album_id):
        album = Album.objects.filter(id=album_id, user=request.user).first()
        if not album:
            return Response({"error": "Album not found or not owned by user"}, status=status.HTTP_404_NOT_FOUND)
        album.delete()
        return Response({"message": "Album deleted successfully"}, status=status.HTTP_200_OK)
    
class AddPostToAlbumView(APIView):
    """
    API view for adding a post to a user's album using URL parameters.
    """
    permission_classes = [IsAuthenticatedOrReadOnly]  # Only authenticated users can access this view

    def post(self, request, album_id, post_id):
        # Get the album that belongs to the current user
        album = get_object_or_404(Album, id=album_id, user=request.user)

        # Get the post by ID
        post = get_object_or_404(Post, id=post_id)

        # Check if the post is already in the album
        if album.posts.filter(id=post.id).exists():
            return Response({"message": "Post is already in the album"}, status=status.HTTP_200_OK)

        # Add the post to the album
        album.posts.add(post)

        return Response({"message": "Post added to album successfully"}, status=status.HTTP_200_OK)

