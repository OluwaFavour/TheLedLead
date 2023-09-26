from django.urls import path
from books.views import (
    ListBooksView,
    bookView,
    uploadBookView,
    updateBookView,
    deleteBookView,
)
from .views import (
    index,
    getAllTimeViews,
    getViewsPerBook,
    getYearlyViews,
    getYearlyViewsPerBook,
    getMonthlyViews,
    getMonthlyViewsPerBook
)

urlpatterns = [
    path("", index, name="admin-index"),
    path("views/", getAllTimeViews, name="admin-views"),
    path("views/<int:id>/", getViewsPerBook, name="admin-views-book"),
    path("views/year=<int:year>/", getYearlyViews, name="admin-views-year"),
    path(
        "views/year=<int:year>/<int:id>/",
        getYearlyViewsPerBook,
        name="admin-views-year-book",
    ),
    path("views/year=<int:year>/month=<int:month>/", getMonthlyViews, name="admin-views-month"),
    path(
        "views/year=<int:year>/month=<int:month>/<int:id>/",
        getMonthlyViewsPerBook,
        name="admin-views-month-book",
    ),
    path("books/", ListBooksView.as_view(), name="admin-books"),
    path("books/<int:book_id>/", bookView, name="admin-books-detail"),
    path("books/upload/", uploadBookView, name="upload-book"),
    path("books/edit/<int:book_id>/", updateBookView, name="admin-books-edit"),
    path("books/delete/<int:book_id>/", deleteBookView, name="admin-books-delete"),
]
