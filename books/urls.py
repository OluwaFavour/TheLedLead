from django.urls import path
from .views import ListBooksView, bookView, uploadBookView

urlpatterns = [
    path('', ListBooksView.as_view(), name='book-list'),
    path('upload/', uploadBookView, name='upload_book'),
    path('book<int:id>/', bookView, name='book_detail'),
]
