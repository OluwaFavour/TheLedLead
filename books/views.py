from rest_framework import status
from rest_framework.decorators import (
    api_view,
    permission_classes,
    authentication_classes,
)
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


# localhost:8000/books/comment/add/<int:book_id>/ (name='add_comment')
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def addCommentsView(request, book_id: int):
    # Check if book exists
    try:
        book = Book.objects.get(id=book_id)
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


# localhost:8000/books/comment/<int:comment_id>/ (name='comment_detail')
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def commentView(request, comment_id: int):
    # Check if comment exists
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"message": "Comment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Get list of replies under the comment
    replies = Comment.objects.filter(parent_comment_id=comment_id)
    # Get list of likes
    likes = comment.likes.all()

    # Create a dictionary containing comment details
    data = {
        "id": comment.id,
        "content": comment.content,
        "date_posted": comment.date_posted,
        "user": {
            "username": comment.user.username,
            "email": comment.user.email,
        },
        "reply_count": len(replies),
        "like_count": len(likes),
        "replies": [
            {
                "reply_id": reply.id,
                "content": reply.content,
                "date_posted": reply.date_posted,
                "user": {
                    "username": reply.user.username,
                    "email": reply.user.email,
                },
            }
            for reply in replies
        ],
        "likes": [
            {
                "like_id": like.id,
                "username": like.username,
                "email": like.email,
            }
            for like in likes
        ],
    }

    # Return the comment as JSON
    return Response(data, status=status.HTTP_200_OK)


# localhost:8000/books/comment/reply/<int:comment_id>/ (name='reply_comment')
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def replyToCommentView(request, comment_id):
    try:
        parent_comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"message": "Comment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    content = request.data.get("content")
    user = request.user

    comment = Comment.objects.create(
        content=content,
        book=parent_comment.book,
        user=user,
        parent_comment=parent_comment,
    )

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


# localhost:8000/books/comment/edit/<int:comment_id>/ (name='edit_comment')
@api_view(["PUT"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def editCommentView(request, comment_id):
    # Check if comment exists
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"message": "Comment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if user is the author of the comment
    if comment.user != request.user:
        return Response(
            {"message": "You are not authorized to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    content = request.data.get("content")
    if not content:
        return Response(
            {"message": "Content cannot be empty"},
            status=status.HTTP_400_BAD_REQUEST,
        )

    comment.content = content
    comment.save()

    data = {
        "id": comment.id,
        "content": comment.content,
        "date_posted": comment.date_posted,
        "user": {
            "username": comment.user.username,
            "email": comment.user.email,
        },
    }
    return Response(data, status=status.HTTP_200_OK)


# localhost:8000/books/comment/delete/<int:comment_id>/ (name='delete_comment')
@api_view(["DELETE"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def deleteCommentView(request, comment_id):
    # Check if comment exists
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"message": "Comment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if user is the author of the comment
    if comment.user != request.user:
        return Response(
            {"message": "You are not authorized to perform this action"},
            status=status.HTTP_403_FORBIDDEN,
        )

    comment.delete()
    return Response(
        {"message": "Comment deleted successfully"}, status=status.HTTP_200_OK
    )


# localhost:8000/books/comment/like/<int:comment_id>/ (name='like_comment')
@api_view(["POST"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def likeCommentView(request, comment_id):
    # Check if comment exists
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"message": "Comment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Check if user has already liked the comment
    if comment.likes.filter(id=request.user.id).exists():
        # Unlike comment
        comment.likes.remove(request.user)
        comment.save()
        return Response({"message": "Comment unliked"}, status=status.HTTP_200_OK)

    # Like comment
    comment.likes.add(request.user)
    comment.save()
    return Response({"message": "Comment liked"}, status=status.HTTP_200_OK)


# localhost:8000/books/comment/likes/<int:comment_id>/ (name='get_comment_likes')
@api_view(["GET"])
@authentication_classes([TokenAuthentication])
@permission_classes([IsAuthenticated])
def getCommentLikesView(request, comment_id):
    # Check if comment exists
    try:
        comment = Comment.objects.get(id=comment_id)
    except Comment.DoesNotExist:
        return Response(
            {"message": "Comment not found"},
            status=status.HTTP_404_NOT_FOUND,
        )

    # Get list of users who liked the comment
    likes = comment.likes.all()

    # Create a list of dictionaries containing user details from the likes list
    data = [
        {
            "id": like.id,
            "username": like.username,
            "email": like.email,
        }
        for like in likes
    ]

    # Return the list of users as JSON
    return Response(
        {"likes": data, "like_count": len(likes)}, status=status.HTTP_200_OK
    )


# localhost:8000/books/rate/<int:id>/ (name='add_rating')
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
    rating_str = request.data.get("rating")
    
    print(rating_str)
    rating = int(rating_str)
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
