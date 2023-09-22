from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response

from books.models import Book

# Create your views here.
@api_view(['GET'])
def index(request):
    if request.method == "GET":
        if not request.user.is_staff:
            return Response({"message": "You are not authorized to access this page"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "This is the admin dashboard"}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getAllTimeViews(request):
    if request.method == "GET":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"message": "You are not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        # Check if user is admin
        if not request.user.is_staff:
            return Response({"message": "You are not authorized to access this page"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "This is the admin dashboard"}, status=status.HTTP_200_OK)
    
    views = 0
    books = Book.objects.all()
    for book in books:
        views += book.read_by.count()
    
    # Return the number of views
    return Response({"views": views}, status=status.HTTP_200_OK)

@api_view(['GET'])
def getViewsPerBook(request, id: int):
    if request.method == "GET":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response({"message": "You are not logged in"}, status=status.HTTP_401_UNAUTHORIZED)
        # Check if user is admin
        if not request.user.is_staff:
            return Response({"message": "You are not authorized to access this page"}, status=status.HTTP_403_FORBIDDEN)
        return Response({"message": "This is the admin dashboard"}, status=status.HTTP_200_OK)
    
    # Get the book
    book = get_object_or_404(Book, id=id)
    # Return the number of views
    return Response({"views": book.read_by.count()}, status=status.HTTP_200_OK)

@api_view(['GET'])
#
    
@api_view(['POST'])
@permission_classes([AllowAny])
def admin_login(request):
    if request.method == 'POST':
        # Check if user is authenticated
        if request.user.is_authenticated:
            return Response({'message': 'Already logged in'}, status=status.HTTP_400_BAD_REQUEST)
        # Access HttpRequest object
        http_request = request._request
        username = http_request.POST.get('username')
        # Check if user exists
        if not User.objects.filter(username=username).exists():
            return Response({'message': 'User does not exist'}, status=status.HTTP_404_NOT_FOUND)
        password = http_request.POST.get('password')
        user = authenticate(http_request, username=username, password=password)

        # Check if user password is correct and user is admin
        if user is not None and user.is_staff:
            login(http_request, user)
            return Response({'message': 'Admin Login successful'})
        else:
            return Response({'message': 'Admin Login failed'}, status=status.HTTP_401_UNAUTHORIZED)