"""
URL patterns for blog-related operations, including creating, retrieving,
liking, downloading posts, managing comments
, and performing search functionality.
"""

from django.urls import path
from .views import CommentCreateView, CommentUpdateView, PostCommentsView

urlpatterns = [
    path('<int:post_id>/post', CommentCreateView.as_view(),
         name='create-comment'),
    path('<int:comment_id>', CommentUpdateView.as_view(),
         name='comment-detail'),
    path('post/<int:post_id>', PostCommentsView.as_view(),
         name='post-comments'),
]

