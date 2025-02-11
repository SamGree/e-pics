from django.urls import path
from .views import PostLikeView, LikedPostsView

urlpatterns = [
    path('<int:post_id>', PostLikeView.as_view(), name='post-like'),
    path('', LikedPostsView.as_view(), name='post-like'),
]
