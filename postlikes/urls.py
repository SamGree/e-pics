from django.urls import path
from .views import PostLikeView, LikedPostsView

urlpatterns = [
    path('<int:post_id>', PostLikeView.as_view(
         ), name='post-like'),  # Like a specific post
    path('', LikedPostsView.as_view(), name='post-like'),
]
