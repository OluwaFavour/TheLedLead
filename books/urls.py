from django.urls import path
from .views import ListBooksView, bookView

urlpatterns = [
    path('', ListBooksView.as_view(), name='book-list'),
    path('book<int:id>/', bookView, name='book_detail'),
]
