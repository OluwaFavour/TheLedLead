from datetime import datetime
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.base_user import AbstractBaseUser
from django.views.decorators.csrf import csrf_protect
from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.auth import AuthToken, TokenAuthentication


def knoxLogin(user: AbstractBaseUser):
    # Create token for user
    try:
        _, token = AuthToken.objects.create(user)
    except Exception as e:
        return Response(
            {"message": "Login failed", "error": str(e)},
            status=status.HTTP_401_UNAUTHORIZED,
        )
    else:
        return Response(
            {
                "message": "Login successful",
                "user": {"id": user.id, "username": user.username, "email": user.email},
                "is_admin": user.is_superuser,
                "token": token,
            },
            status=status.HTTP_200_OK,
        )


# localhost:8000/
@api_view(["GET"])
def homeView(request):
    if request.method == "GET":
        return Response(
            {"message": "Hello World! This is TheLedLead"}, status=status.HTTP_200_OK
        )


# localhost:8000/logout/
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    # Access HttpRequest object
    http_request = request._request
    # Logout the user
    logout(http_request)
    return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)


# localhost:8000/signup/
@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def signup(request):
    # Access HttpRequest object
    http_request = request._request
    username = http_request.POST.get("username")
    email = http_request.POST.get("email")
    password = http_request.POST.get("password")
    password2 = http_request.POST.get("password2")

    if not username or not password or not password2 or not email:
        return Response(
            {"message": "Username, email, and both password fields are required"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if a user with the same username already exists
    if User.objects.filter(username=username).exists():
        return Response(
            {"message": "Username already exists"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Check if a user with the same email already exists
    if User.objects.filter(email=email).exists():
        return Response(
            {"message": "Email already exists"}, status=status.HTTP_400_BAD_REQUEST
        )

    # Check if the passwords match
    if password != password2:
        return Response(
            {"message": "Passwords do not match"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Create the user
    user = User.objects.create_user(username=username, email=email, password=password)
    # Create knox token for user
    _, token = AuthToken.objects.create(user)

    return Response(
        {
            "message": "User created successfully",
            "user": {"id": user.id, "username": user.username, "email": user.email},
            "token": token,
        },
        status=status.HTTP_201_CREATED,
    )


# localhost:8000/login/
@csrf_protect
@api_view(["POST"])
@permission_classes([AllowAny])
def login_view(request):
    # Access HttpRequest object
    http_request = request._request
    username = http_request.POST.get("username")
    # Check if username is provided
    if not username:
        return Response(
            {"message": "Username is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    # Check if user exists
    try:
        user = User.objects.get(username=username)
    except User.DoesNotExist:
        return Response(
            {"message": "User does not exist"},
            status=status.HTTP_404_NOT_FOUND,
        )

    password = http_request.POST.get("password")
    # Check if password is provided
    if not password:
        return Response(
            {"message": "Password is required"}, status=status.HTTP_400_BAD_REQUEST
        )
    user = authenticate(http_request, username=username, password=password)
    # Check if user password is correct and login
    if user is not None:
        return knoxLogin(user)
    else:
        return Response(
            {"message": "Login failed", "error": "Invalid username or password"},
            status=status.HTTP_401_UNAUTHORIZED,
        )


# localhost:8000/change-password/
@csrf_protect
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def changePassword(request):
    # Access HttpRequest object
    http_request = request._request
    old_password = http_request.POST.get("old_password")
    new_password1 = http_request.POST.get("new_password1")
    new_password2 = http_request.POST.get("new_password2")
    # Check if old password is provided
    if not old_password:
        return Response(
            {"message": "Old password is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Check if new password is provided
    if not new_password1:
        return Response(
            {"message": "New password is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Check if confirm password is provided
    if not new_password2:
        return Response(
            {"message": "Confirm password is required"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    # Check if new password and confirm password match
    if new_password1 != new_password2:
        return Response(
            {"message": "New password and confirm password do not match"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    # Get user
    user = request.user

    # Save the new password
    user.set_password(http_request.POST.get("new_password1"))
    user.save()
    # Update the session
    update_session_auth_hash(request, user)
    return Response(
        {"message": "Password changed successfully"}, status=status.HTTP_200_OK
    )
