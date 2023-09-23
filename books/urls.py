from django.urls import path
from .views import (
    ListBooksView,
    bookView,
    addCommentsView,
    addRatingView,
)

urlpatterns = [
    path("", ListBooksView.as_view(), name="book_list"),
    path("<int:id>/", bookView, name="book_detail"),
    path("comment/<int:id>/", addCommentsView, name="add_comment"),
    path("rate/<int:id>/", addRatingView, name="add_rating"),
]
