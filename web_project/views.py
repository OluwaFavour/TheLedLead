from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

# localhost:8000/
@api_view(['GET'])
def homeView(request):
    if request.method == 'GET':
        return Response({'message': 'Hello World! This is TheLedLead'}, status=status.HTTP_200_OK)

# localhost:8000/logout/
@api_view(['GET'])
def logout_view(request):
    if request.method == 'GET':
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({'message': 'Not logged in'}, status=status.HTTP_401_UNAUTHORIZED)
        # Access HttpRequest object
        http_request = request._request
        # Logout the user
        logout(http_request)
        return Response({'message': 'Logout successful'}, status=status.HTTP_200_OK)

# localhost:8000/signup/
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    if request.method == 'POST':
        # Access HttpRequest object
        http_request = request._request
        username = http_request.POST.get('username')
        email = http_request.POST.get('email')
        password = http_request.POST.get('password')
        password2 = http_request.POST.get('password2')

        if not username or not password or not password2 or not email:
            return Response({'message': 'Username, email, and both password fields are required'}, status=status.HTTP_400_BAD_REQUEST)

        # Check if a user with the same username already exists
        if User.objects.filter(username=username).exists():
            return Response({'message': 'Username already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if a user with the same email already exists
        if User.objects.filter(email=email).exists():
            return Response({'message': 'Email already exists'}, status=status.HTTP_400_BAD_REQUEST)
        
        # Check if the passwords match
        if password != password2:
            return Response({'message': 'Passwords do not match'}, status=status.HTTP_400_BAD_REQUEST)

        # Create the user
        user = User.objects.create_user(username=username, email=email, password=password)

        return Response({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)

# localhost:8000/login/
@api_view(['POST'])
@permission_classes([AllowAny])
def login_view(request):
    if request.method == 'POST':
        # Access HttpRequest object
        http_request = request._request
        username = http_request.POST.get('username')
        password = http_request.POST.get('password')
        user = authenticate(http_request, username=username, password=password)

        # Check if user exists and login
        if user is not None:
            login(http_request, user)
            return Response({'message': 'Login successful'})
        else:
            return Response({'message': 'Login failed'}, status=status.HTTP_401_UNAUTHORIZED)