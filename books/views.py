from rest_framework import status
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_protect
from knox.auth import TokenAuthentication
from datetime import datetime
from .models import Book, Rating, Comment


def getAverageRating(book_id: int) -> float:
    ratings = Rating.objects.filter(book_id=book_id)
    average_rating: float = (
        round(float(sum(rating.rating for rating in ratings) / len(ratings)), 1)
        if ratings
        else 0
    )
    return average_rating


# localhost:8000/books/
@permission_classes([AllowAny])
class ListBooksView(APIView):
    def get(self, request):
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
                    "username": book.published_by.username if book.published_by else "",
                    "email": book.published_by.email if book.published_by else "",
                },
                "average_rating": getAverageRating(book.id),
                "total_ratings": Rating.objects.filter(book_id=book.id).count(),
                "total_comments": Comment.objects.filter(book_id=book.id).count(),
            }
            for book in book_list
        ]

        # Return the list of books as JSON
        return Response(books, status=status.HTTP_200_OK)


# localhost:8000/books/<int:id>/
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def bookView(request, id: int):
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

    # Mark book as read by user
    if not book.read_by.filter(id=request.user.id).exists():
        book.read_by.add(request.user, through_defaults={"read_date": datetime.now()})
        book.save()
    # Return the book as JSON
    return Response(data, status=status.HTTP_200_OK)


# localhost:8000/books/upload/ (name='upload_book')
@csrf_protect
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def uploadBookView(request):
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
    if not title or not content:
        return Response(
            {"message": "Title or content cannot be empty"},
            status=status.HTTP_400_BAD_REQUEST,
        )
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


# localhost:8000/books/<int:id>/update/ (name='update_book')
@csrf_protect
@api_view(["PATCH"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def updateBookView(request, id: int):
    if not request.user.is_staff:
        return Response(
            {"message": "You are not authorized to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Attempt to get the book by ID, and handle the case where it doesn't exist
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response(
            {"message": "Book not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    else:
        # Get book details from request
        title = request.data.get("title")
        content = request.data.get("content")
        image_url = request.FILES.get("image_url")

        # Check if all fields are all empty
        if not title and not content and not image_url:
            return Response({"message": "Nothing changed"}, status=status.HTTP_200_OK)

        # Update book
        if title:
            book.title = title
        if content:
            book.content = content
        if image_url:
            book.image_url = image_url
        book.date_published = datetime.now()

        # Save update
        book.save()

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
        return Response(data, status=status.HTTP_200_OK)


# localhost:8000/books/<int:id>/update/ (name='update_book')
@csrf_protect
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteBookView(request, id: int):
    if not request.user.is_staff:
        return Response(
            {"message": "You are not authorized to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    # Attempt to get the book by ID, and handle the case where it doesn't exist
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response(
            {"message": "Book not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Delete the book
    book.delete()
    return Response({"message": "Book deleted successfully"}, status=status.HTTP_200_OK)


# localhost:8000/books/comment/<int:id>/ (name='add_comment')
@csrf_protect
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addCommentsView(request, id: int):
    # Check if book exists
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response(
            {"message": "Book not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    # Access HttpRequest object
    http_request = request._request
    # Get comment details from request
    content = http_request.POST.get("content")
    user = http_request.user

    # Create comment
    comment = Comment.objects.create(content=content, book=book, user=user)

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


# localhost:8000/books/rate/<int:id>/ (name='add_rating')
@csrf_protect
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addRatingView(request, id: int):
    # Check if book exists
    try:
        book = Book.objects.get(id=id)
    except Book.DoesNotExist:
        return Response(
            {"message": "Book not found"},
            status=status.HTTP_404_NOT_FOUND,
        )
    
    # Access HttpRequest object
    http_request = request._request
    # Get rating details from request
    rating = int(http_request.POST.get("rating"))
    # Check if rating is valid
    if rating < 1 or rating > 5:
        return Response(
            {"message": "Rating must be between 1 and 5"},
            status=status.HTTP_400_BAD_REQUEST,
        )
    user = http_request.user

    # Check if user has already rated the book
    if Rating.objects.filter(book=book, user=user).exists():
        # Update previous rating with new rating
        ratingObj = Rating.objects.get(book=book, user=user)
        ratingObj.rating = rating
        ratingObj.save()

        # Return the rating as JSON
        data = {
            "id": ratingObj.id,
            "rating": ratingObj.rating,
            "user": {
                "username": ratingObj.user.username,
                "email": ratingObj.user.email,
            },
        }
        return Response(data, status=status.HTTP_200_OK)

    # Create rating
    rating = Rating.objects.create(rating=rating, book=book, user=user)

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
