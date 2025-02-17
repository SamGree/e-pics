"""e_pics URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from .views import root_route

urlpatterns = [
    path('', root_route),
    # Admin panel for managing the Django application
    path('admin/', admin.site.urls),

    # Routes for the blog application
    path('posts/', include('posts.urls')),

    # Routes for user management
    path('users/', include('users.urls')),

    path('comments/', include('comments.urls')),

    path('albums/', include('albums.urls')),

    path('post-like/', include('postlikes.urls')),

    path('comment-like/', include('commentlikes.urls')),
]
