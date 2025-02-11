"""
URL patterns for blog-related operations, including creating, retrieving, 
liking, downloading posts, managing comments, and performing search functionality.
"""
from django.urls import path
from .views import PostListCreateView, PostDetailView, PostDownloadView, SearchView

urlpatterns = [
    path('', PostListCreateView.as_view(), name='list-create-posts'),
    path('<int:post_id>', PostDetailView.as_view(), name='detail-post'),
    path('<int:post_id>/download', PostDownloadView.as_view(), name='post-download'),# Download a specific post
    path('search/', SearchView.as_view(), name='search'), # Perform a search across posts
]
