from django.test import TestCase
from django.contrib.auth.models import User
from .models import Book, Comment, Rating

# Create your tests here.

class BookModelTest(TestCase):
    
    def setUp(self):
        user = User.objects.create(username="Test", password="asdf1023")
        Book.objects.create(
            title="A Test-Book :D",
            content="It's just a test",
            published_by=user
        )
    
    def test_book_title(self):
        book = Book.objects.get(id=1)
        expected_book_title = book.title
        self.assertEqual(expected_book_title, "A Test-Book :D")
        
    def test_book_content(self):
        book = Book.objects.get(id=1)
        expected_book_content = book.content
        self.assertEqual(expected_book_content, "It's just a test")
    
    def test_book_publisher(self):
        book = Book.objects.get(id=1)
        expected_publisher = book.published_by.username
        self.assertEqual(expected_publisher, "Test")

class CommentModelTest(TestCase):
    
    def setUp(self):
        # Get user
        user = User.objects.create(username="Test", password="asdf1023")
        book = Book.objects.create(
            title="A Test-Book :D",
            content="It's just a test",
            published_by=user
        )
        Comment.objects.create(book=book, user=user, content="Just a test")
    
    def test_comment_content(self):
        comment = Comment.objects.get(id=1)
        expected_content = comment.content
        self.assertEqual(expected_content, "Just a test")
    
    def test_comment_owner(self):
        comment = Comment.objects.get(id=1)
        expected_owner = comment.user.username
        self.assertEqual(expected_owner, "Test")
    
    def test_book_commented_own(self):
        comment = Comment.objects.get(id=1)
        expected_book = comment.book.title
        self.assertEqual(expected_book, "A Test-Book :D")

class RatingModelTest(TestCase):
    
    def setUp(self):
        # Get user
        user = User.objects.create(username="Test", password="asdf1023")
        book = Book.objects.create(
            title="A Test-Book :D",
            content="It's just a test",
            published_by=user
        )
        Rating.objects.create(user=user, book=book, rating=3)
    
    def test_rating(self):
        rating = Rating.objects.get(id=1)
        expected_rating = rating.rating
        self.assertEqual(expected_rating, 3)
    
    def test_rate_owner(self):
        rating = Rating.objects.get(id=1)
        expected_rater = rating.user.username
        self.assertEqual(expected_rater, "Test")
    
    def test_book_rated(self):
        rating = Rating.objects.get(id=1)
        expected_book = rating.book.title
        self.assertEqual(expected_book, "A Test-Book :D")