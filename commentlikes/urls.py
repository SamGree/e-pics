from django.urls import path
from .views import CommentLikeView

urlpatterns = [
    path('<int:comment_id>', CommentLikeView.as_view(), name='comment-like'),# Like a specific comment
]
