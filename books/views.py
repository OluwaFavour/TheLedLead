from typing import Any
from django import http
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404
from django.views.generic import ListView
from .models import Book, Rating, Comment

# Create your views here.
class ListBooksView(ListView):
    model = Book
    
    def render_to_response(self, context: dict[str, Any], **response_kwargs: Any) -> HttpResponse:
        # Get list of books from context
        book_list = context.get('object_list', [])
        
        # Create a list of dictionaries containing book details from the book list
        books = [
            {'id': book.id,
            'title': book.title,
            'image_url': book.image_url.url if book.image_url else '',
            'content': book.content,
            'date_published': book.date_published,
            'published_by': {
                'username': book.published_by.username if book.published_by else '',
                'email': book.published_by.email if book.published_by else '',
            }
            } for book in book_list]
        
        # Return the list of books as JSON
        return JsonResponse(books, safe=False)

def bookView(request, id):
    if request.method == 'GET':
        # Get book
        book = get_object_or_404(Book, id=id)
        # Get list of comments under the book
        comments = Comment.objects.filter(book_id=id)
        if not  comments:
            print("Comment is empty")
        # Get list of ratings
        ratings = Rating.objects.filter(book_id=id)
        if not ratings:
            print("Ratings is zero")
            return HttpResponse(book)
        # Get total rating
        total_rating = 0
        for rating in ratings:
            total_rating += rating
        # Get number of ratings
        num_of_ratings = ratings.count()
        # Get average rating
        average_rating = round(float(total_rating / num_of_ratings), 1)
        return HttpResponse(book)