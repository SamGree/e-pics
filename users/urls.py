"""
URL patterns for user-related operations, including registration, login, logout, 
profile retrieval, and profile updates.
"""
from django.urls import path
from .views import RegisterView

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'), # User registration endpoint
]