from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.contrib.admin.views.decorators import staff_member_required
from .models import Book, Rating, Comment


# localhost:8000/books/
@permission_classes([AllowAny])
class ListBooksView(APIView):
    def get(self, request):
        if request.method == "GET":
            # Get list of books from context
            book_list = Book.objects.all()

            # Create a list of dictionaries containing book details from the book list
            books = [
                {
                    "id": book.id,
                    "title": book.title,
                    "image_url": book.image_url.url if book.image_url else "",
                    "content": book.content,
                    "date_published": book.date_published,
                    "published_by": {
                        "username": book.published_by.username
                        if book.published_by
                        else "",
                        "email": book.published_by.email if book.published_by else "",
                    },
                }
                for book in book_list
            ]

            # Return the list of books as JSON
            return Response(books, status=status.HTTP_200_OK)


# localhost:8000/books/<int:id>/
@api_view(["GET"])
@permission_classes([AllowAny])
def bookView(request, id: int):
    if request.method == "GET":
        # Get book
        book = get_object_or_404(Book, id=id)
        # Get list of comments under the book
        comments = Comment.objects.filter(book_id=id)
        # Get list of ratings
        ratings = Rating.objects.filter(book_id=id)
        # Get average rating
        average_rating: float = (
            round(float(sum(rating.rating for rating in ratings) / len(ratings)), 1)
            if ratings
            else 0
        )

        # Create a dictionary containing book details
        data = {
            "id": book.id,
            "title": book.title,
            "image_url": book.image_url.url if book.image_url else "",
            "content": book.content,
            "date_published": book.date_published,
            "published_by": {
                "username": book.published_by.username if book.published_by else "",
                "email": book.published_by.email if book.published_by else "",
            },
            "comments": [
                {
                    "id": comment.id,
                    "content": comment.content,
                    "date_posted": comment.date_posted,
                    "user": {
                        "username": comment.user.username,
                        "email": comment.user.email,
                    },
                }
                for comment in comments
            ],
            "ratings": [
                {
                    "id": rating.id,
                    "rating": rating.rating,
                    "user": {
                        "username": rating.user.username,
                        "email": rating.user.email,
                    },
                }
                for rating in ratings
            ],
            "total_comments": len(comments),
            "average_rating": average_rating,
        }

        # Return the book as JSON
        return Response(data, status=status.HTTP_200_OK)


# localhost:8000/books/upload/
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def uploadBookView(request) -> HttpResponse:
    if request.method == "POST":
        # Check if user is staff (admin)
        if not request.user.is_staff:
            return Response(
                {"message": "You are not authorized to perform this action"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Access HttpRequest object
        http_request = request._request
        # Get book details from request
        title = http_request.POST.get("title")
        content = http_request.POST.get("content")
        image_url = http_request.FILES.get("image_url")
        published_by = http_request.user

        # Create book
        book = Book.objects.create(
            title=title, content=content, image_url=image_url, published_by=published_by
        )

        # Return the book as JSON
        data = {
            "id": book.id,
            "title": book.title,
            "image_url": book.image_url.url if book.image_url else "",
            "content": book.content,
            "date_published": book.date_published,
            "published_by": {
                "username": book.published_by.username if book.published_by else "",
                "email": book.published_by.email if book.published_by else "",
            },
        }
        return Response(data, status=status.HTTP_201_CREATED)


# localhost:8000/books/<int:id>/comment/
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addCommentsView(request, book_id: int):
    if request.method == "POST":
        # Access HttpRequest object
        http_request = request._request
        # Get comment details from request
        content = http_request.POST.get("content")
        user = http_request.user

        # Create comment
        comment = Comment.objects.create(content=content, book_id=book_id, user=user)

        # Return the comment as JSON
        data = {
            "id": comment.id,
            "content": comment.content,
            "date_posted": comment.date_posted,
            "user": {
                "username": comment.user.username,
                "email": comment.user.email,
            },
        }
        return Response(data, status=status.HTTP_201_CREATED)


# localhost:8000/books/<int:id>/rate/
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def addRatingView(request, book_id: int):
    if request.method == "POST":
        # Access HttpRequest object
        http_request = request._request
        # Get rating details from request
        rating = http_request.POST.get("rating")
        user = http_request.user

        # Create rating
        rating = Rating.objects.create(rating=rating, book_id=book_id, user=user)

        # Return the rating as JSON
        data = {
            "id": rating.id,
            "rating": rating.rating,
            "user": {
                "username": rating.user.username,
                "email": rating.user.email,
            },
        }
        return Response(data, status=status.HTTP_201_CREATED)
