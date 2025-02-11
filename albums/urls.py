"""
URL patterns for blog-related operations, including creating, retrieving,
liking, downloading posts, managing comments
and performing search functionality.
"""
from django.urls import path
from .views import AlbumListCreateView, AlbumDetailView, AddPostToAlbumView

urlpatterns = [
    path('', AlbumListCreateView.as_view(), name='list-create-albums'),
    path('<int:album_id>', AlbumDetailView.as_view(), name='detail-album'),
    path('<int:album_id>/add-post/<int:post_id>', AddPostToAlbumView.as_view(),
         name='add-post-to-album'),

]
