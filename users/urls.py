"""
URL patterns for user-related operations, including registration, login, logout, 
profile retrieval, and profile updates.
"""
from django.urls import path
from .views import RegisterView, LoginView, LogoutView, UserProfileUpdateView, UserProfileDetailView

urlpatterns = [
    path('register/', RegisterView.as_view(), name='register'), # User registration endpoint
    path('login/', LoginView.as_view(), name='login'), # User login endpoint
    path('logout/', LogoutView.as_view(), name='logout'), # User logout endpoint
    path('profile/<int:user_id>', UserProfileDetailView.as_view(), name='user-profile-detail'), # Retrieve user profile details
    path('profile/update', UserProfileUpdateView.as_view(), name='profile-update'),  # Update user profile
]
