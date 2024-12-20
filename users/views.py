from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import AllowAny
from .models import User
from .serializers import UserSerializer


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
        if ' ' in username:
            return Response({'error': 'Username cannot contain spaces.'}, status=status.HTTP_400_BAD_REQUEST)
        
        if User.objects.filter(username__iexact=username).exists():
            return Response({'error': 'Username already exists.'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)