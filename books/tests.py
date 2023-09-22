from django.test import TestCase
from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
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

class ListBooksViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse("book_list")
        
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

    def test_list_books(self):
        # Create some sample books
        book1 = Book.objects.create(
            title="Book 1",
            content="Content 1",
            published_by=self.user
        )
        book2 = Book.objects.create(
            title="Book 2",
            content="Content 2",
            published_by=self.user
        )

        # Make a GET request to list books
        response = self.client.get(self.url)

        # Check if the response status code is 200 OK (as it's an AllowAny view)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the book details
        self.assertEqual(len(response.data), 2)  # Assuming two books are created

        # Check if the book details match the expected values
        for book in response.data:
            if book["id"] == book1.id:
                self.assertEqual(book["title"], book1.title)
                self.assertEqual(book["content"], book1.content)
                self.assertEqual(book["published_by"]["username"], self.user.username)
                self.assertEqual(book["published_by"]["email"], self.user.email)
            elif book["id"] == book2.id:
                self.assertEqual(book["title"], book2.title)
                self.assertEqual(book["content"], book2.content)
                self.assertEqual(book["published_by"]["username"], self.user.username)
                self.assertEqual(book["published_by"]["email"], self.user.email)


class BookViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )
        
        # Create a sample book
        book = Book.objects.create(
            title="Book 1",
            content="Content 1",
            published_by=self.user
        )
        
        self.url = reverse("book_detail", args=[book.id])


    def test_get_book_details_authenticated(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make a GET request to view book details
        response = self.client.get(self.url)

        # Check if the response status code is 200 OK
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        book = Book.objects.get(id=1)
        # Check if the response data contains the book details
        self.assertEqual(response.data["id"], book.id)
        self.assertEqual(response.data["title"], book.title)
        self.assertEqual(response.data["content"], book.content)
        self.assertEqual(response.data["published_by"]["username"], self.user.username)
        # Add more assertions for other book details if needed

    def test_get_book_details_unauthenticated(self):
        # Make a GET request to view book details without authentication
        response = self.client.get(self.url)

        # Check if the response status code is 200 OK (as it's an AllowAny view)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Check if the response data contains the book details
        book = Book.objects.get(id=1)
        self.assertEqual(response.data["id"], book.id)
        self.assertEqual(response.data["title"], book.title)
        self.assertEqual(response.data["content"], book.content)
        self.assertEqual(response.data["published_by"]["username"], self.user.username)


class UploadBookViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        
        # Create a test admin user
        self.admin_user = User.objects.create_user(
            username="adminuser",
            password="adminpassword",
            is_staff=True
        )

        # Create a test regular user
        self.regular_user = User.objects.create_user(
            username="regularuser",
            password="regularpassword"
        )

        # Define the URL for the upload book view
        self.url = reverse("upload_book")

    def test_upload_book_authenticated_admin(self):
        # Authenticate the admin user
        self.client.force_authenticate(user=self.admin_user)

        # Make a POST request to upload a book as an admin
        data = {
            "title": "Test Book",
            "content": "Test Content",
        }
        response = self.client.post(self.url, data, format="multipart")

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response data contains the book details
        self.assertEqual(response.data["title"], data["title"])
        self.assertEqual(response.data["image_url"], "")
        self.assertEqual(response.data["content"], data["content"])
        self.assertEqual(response.data["published_by"]["username"], self.admin_user.username)
        self.assertEqual(response.data["published_by"]["email"], self.admin_user.email)

    def test_upload_book_authenticated_regular_user(self):
        # Authenticate the regular user
        self.client.force_authenticate(user=self.regular_user)

        # Make a POST request to upload a book as a regular user (non-admin)
        data = {
            "title": "Test Book",
            "content": "Test Content",
        }
        response = self.client.post(self.url, data, format="multipart")

        # Check if the response status code is 403 Forbidden
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    def test_upload_book_unauthenticated(self):
        # Make a POST request to upload a book without authentication
        data = {
            "title": "Test Book",
            "content": "Test Content",
        }
        response = self.client.post(self.url, data, format="multipart")

        # Check if the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AddCommentViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create a test book for the comment
        self.book = Book.objects.create(
            title="Test Book",
            content="Test Content",
            published_by=self.user
        )

        # Define the URL for the add comment view
        self.url = reverse("add_comment", args=[self.book.id])

    def test_add_comment_authenticated_user(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make a POST request to add a comment as an authenticated user
        data = {
            "content": "Test Comment",
        }
        response = self.client.post(self.url, data, format="multipart")

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response data contains the comment details
        self.assertEqual(response.data["content"], data["content"])
        self.assertEqual(response.data["user"]["username"], self.user.username)
        # Add more assertions for other comment details if needed

    def test_add_comment_unauthenticated_user(self):
        # Make a POST request to add a comment without authentication
        data = {
            "content": "Test Comment",
        }
        response = self.client.post(self.url, data, format="multipart")

        # Check if the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

class AddRatingViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()

        # Create a test user
        self.user = User.objects.create_user(
            username="testuser",
            password="testpassword"
        )

        # Create a test book for the rating
        self.book = Book.objects.create(
            title="Test Book",
            content="Test Content",
            published_by=self.user
        )

        # Define the URL for the add rating view
        self.url = reverse("add_rating", args=[self.book.id])

    def test_add_rating_authenticated_user(self):
        # Authenticate the user
        self.client.force_authenticate(user=self.user)

        # Make a POST request to add a rating as an authenticated user
        data = {
            "rating": 5,
        }
        response = self.client.post(self.url, data, format="multipart")

        # Check if the response status code is 201 Created
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        # Check if the response data contains the rating details
        self.assertEqual(response.data["rating"], data["rating"])
        self.assertEqual(response.data["user"]["username"], self.user.username)
        # Add more assertions for other rating details if needed

    def test_add_rating_unauthenticated_user(self):
        # Make a POST request to add a rating without authentication
        data = {
            "rating": 5,
        }
        response = self.client.post(self.url, data, format="multipart")

        # Check if the response status code is 401 Unauthorized
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)