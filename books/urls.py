from django.urls import path
from .views import ListBooksView, bookView, uploadBookView, addCommentsView, addRatingView

urlpatterns = [
    path('', ListBooksView.as_view(), name='book_list'),
    path('upload/', uploadBookView, name='upload_book'),
    path('<int:id>/', bookView, name='book_detail'),
    path('<int:id>/comment/', addCommentsView, name='add_comment'),
    path('<int:id>/rate/', addRatingView, name='add_rating'),
]
