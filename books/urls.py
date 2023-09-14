from django.urls import path
from .views import listBooksView, bookView

urlpatterns = [
    path('', listBooksView, name='listBooks'),
    path('book<int:id>/', bookView, name='book_detail'),
]
