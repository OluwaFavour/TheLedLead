from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.db.models import Count
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from books.models import Book
from .enums import getMonth

# localhost:8000/tll-admin/ (name="admin-index")
@api_view(["GET"])
def index(request):
    if request.method == "GET":
        if not request.user.is_staff:
            return Response(
                {"message": "You are not authorized to access this page"},
                status=status.HTTP_403_FORBIDDEN,
            )
        return Response(
            {"message": "This is the admin dashboard"}, status=status.HTTP_200_OK
        )


# localhost:8000/tll-admin/views/ (name="admin-views")
@api_view(["GET"])
def getAllTimeViews(request):
    if request.method == "GET":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"message": "You are not logged in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {"message": "You are not authorized to access this page"},
                status=status.HTTP_403_FORBIDDEN,
            )

        views = 0
        books = Book.objects.all()
        for book in books:
            views += book.read_by.count()

        # Return the number of views
        return Response({"views": views}, status=status.HTTP_200_OK)

# localhost:8000/tll-admin/views/<int:id>/ (name="admin-views-book")
@api_view(["GET"])
def getViewsPerBook(request, id: int):
    if request.method == "GET":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"message": "You are not logged in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {"message": "You are not authorized to access this page"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the book
        book = get_object_or_404(Book, id=id)
        # Return the number of views
        return Response(
            {"id": id, "views": book.read_by.count()}, status=status.HTTP_200_OK
        )

# localhost:8000/tll-admin/views/<int:year>/ (name="admin-views-year")
@api_view(["GET"])
def getYearlyViews(request, year: int):
    if request.method == "GET":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"message": "You are not logged in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {"message": "You are not authorized to access this page"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the number of users who read each book in the specified year
        books_read_with_readers_count = (
            Book.objects.filter(read_by__readbook__read_date__year=year)
            .annotate(readers_count=Count("read_by__readbook__user"))
            .distinct()
        )

        num_of_books_read = books_read_with_readers_count.count()
        num_of_views = 0
        for book in books_read_with_readers_count:
            num_of_views += book.readers_count

        # Return the number of views
        return Response(
            {
                "year": year,
                "number of books read": num_of_books_read,
                "views": num_of_views,
            },
            status=status.HTTP_200_OK,
        )

# localhost:8000/tll-admin/views/<int:year>/<int:id>/ (name="admin-views-year-book")
@api_view(["GET"])
def getYearlyViewsPerBook(request, id: int, year: int):
    if request.method == "GET":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"message": "You are not logged in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {"message": "You are not authorized to access this page"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get the book
        book = get_object_or_404(Book, id=id)
        # Get the number of users who read the book in the specified year
        readers_count = book.read_by.filter(readbook__read_date__year=year).count()

        # Return the number of views
        return Response(
            {"year": year, "id": id, "views": readers_count}, status=status.HTTP_200_OK
        )

# localhost:8000/tll-admin/views/<int:year>/<int:month>/ (name="admin-views-month")
@api_view(["GET"])
def getMonthlyViews(request, month: int, year: int):
    if request.method == "GET":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"message": "You are not logged in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {"message": "You are not authorized to access this page"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get Month name
        month_name = getMonth(month)
        if month_name is None:
            return Response(
                {"message": "Invalid month number"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Get the number of users who read each book in the specified month
        books_read_with_readers_count = (
            Book.objects.filter(
                read_by__readbook__read_date__year=year,
                read_by__readbook__read_date__month=month,
            )
            .annotate(readers_count=Count("read_by__readbook__user"))
            .distinct()
        )

        num_of_books_read = books_read_with_readers_count.count()
        num_of_views = 0
        for book in books_read_with_readers_count:
            num_of_views += book.readers_count

        # Return the number of views
        return Response(
            {
                "year": year,
                "month_number": month,
                "month_name": month_name,
                "number of books read": num_of_books_read,
                "views": num_of_views,
            },
            status=status.HTTP_200_OK,
        )

# localhost:8000/tll-admin/views/<int:year>/<int:month>/<int:id>/ (name="admin-views-month-book")
@api_view(["GET"])
def getMonthlyViewsPerBook(request, id: int, month: int, year: int):
    if request.method == "GET":
        # Check if user is authenticated
        if not request.user.is_authenticated:
            return Response(
                {"message": "You are not logged in"},
                status=status.HTTP_401_UNAUTHORIZED,
            )
        # Check if user is admin
        if not request.user.is_staff:
            return Response(
                {"message": "You are not authorized to access this page"},
                status=status.HTTP_403_FORBIDDEN,
            )

        # Get Month name
        month_name = getMonth(month)
        if month_name is None:
            return Response(
                {"message": "Invalid month number"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Get the book
        book = get_object_or_404(Book, id=id)
        # Get the number of users who read the book in the specified month
        readers_count = book.read_by.filter(
            read_by__readbook__read_date__year=year, readbook__read_date__month=month
        ).count()

        # Return the number of views
        return Response(
            {
                "year": year,
                "month_number": month,
                "month_name": month_name,
                "id": id,
                "views": readers_count,
            },
            status=status.HTTP_200_OK,
        )
