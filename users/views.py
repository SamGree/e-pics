"""
Views for user-related operations including registration, login, logout,
profile retrieval, and profile updates.
"""

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from rest_framework.authtoken.models import Token
from .serializers import UserSerializer
from posts.serializers import PostSerializer
from .models import User
from posts.models import Post


class RegisterView(APIView):
    """
    API view for user registration.
    Allows new users to register by providing their details.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user registration.
        Validates and saves the user data provided in the request.
        """
        username = request.data.get('username', '').strip()
        # print("username: ", username)
        if ' ' in username:
            return Response({'error': 'Username cannot contain spaces.'},
                            status=status.HTTP_400_BAD_REQUEST)

        if User.objects.filter(username__iexact=username).exists():
            return Response({'error': 'Username already exists.'},
                            status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data, context={
            'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    """
    API view for user login.
    Authenticates the user and returns a token if credentials are valid.
    """
    permission_classes = [AllowAny]

    def post(self, request):
        """
        Handle user login.
        Validates username and password, then generates or retrieves an auth
        token.
        """
        username = request.data.get('username', '').strip()
        password = request.data.get('password')

        if ' ' in username:
            return Response({'error': 'Username cannot contain spaces.'},
                            status=status.HTTP_400_BAD_REQUEST)

        try:
            user = User.objects.get(username=username)
        except User.DoesNotExist:
            return Response({'error': 'Invalid username.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        if not user.check_password(password):
            return Response({'error': 'Invalid password.'},
                            status=status.HTTP_401_UNAUTHORIZED)

        # If username and password are correct
        token, _ = Token.objects.get_or_create(user=user)
        user_data = UserSerializer(user).data
        return Response({'token': token.key, 'user': user_data},
                        status=status.HTTP_200_OK)


class LogoutView(APIView):
    """
    API view for logging out the authenticated user.
    Deletes the authentication token.
    """

    permission_classes = [IsAuthenticated]

    def post(self, request):
        """
        Handle user logout.
        Deletes the user's authentication token if authenticated.
        """
        if request.user.is_authenticated:
            try:
                request.user.auth_token.delete()
                return Response({'message': 'Successfully logged out.'},
                                status=status.HTTP_200_OK)
            except Exception as e:
                return Response({'error': str(e)},
                                status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        return Response({'error': 'User is not authenticated.'},
                        status=status.HTTP_401_UNAUTHORIZED)


class UserProfileDetailView(APIView):
    """
    API view for retrieving user profile details and their posts.
    """
    def get(self, request, user_id):
        """
        Handle GET request for user profile and associated posts.
        """
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({'error': 'User not found'},
                            status=status.HTTP_404_NOT_FOUND)
        # print("user: ", user)
        user_serializer = UserSerializer(user)
        posts = Post.objects.filter(user=user)
        post_serializer = PostSerializer(posts, many=True)

        return Response({
            'user': user_serializer.data,
            'posts': post_serializer.data
        }, status=status.HTTP_200_OK)


class UserProfileUpdateView(APIView):
    """
    API view for updating user profile details.
    """
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        """
        Handle PATCH request to partially update user profile.
        """
        user = request.user
        serializer = UserSerializer(user, data=request.data, partial=True,
                                    context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
