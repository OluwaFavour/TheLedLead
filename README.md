# TheLedLead API Documentation

TheLedLead API empowers users to engage with TheLedLead website, offering a range of interactive functionalities. Users can seamlessly create accounts, log in, log out, explore available books, post comments, and rate books. For book uploads, exclusive privileges are granted to admin users, enabling them to contribute new content to the platform.

## Endpoints

- **Home View**
  - URL: `/`
  - Method: `GET`
  - Description: Retrieve a welcome message and information about the book publisher's website.
  - Authentication: Not required.
  - Response:
    - Status Code: 200 OK
    - Body:

      ```json
      {
          "message": "Hello World! This is TheLedLead"
      }
      ```

- **Logout View**
  - URL: `/logout/`
  - Method: `GET`
  - Description: Log out the currently authenticated user.
  - Authentication: Required (user must be authenticated).
  - Response:
    - Status Code: 200 OK
    - Body:

      ```json
      {
          "message": "Logout successful"
      }
      ```

- **Signup View**
  - URL: `/signup/`
  - Method: `POST`
  - Description: Register a new user account.
  - Authentication: Not required.
  - Request:
    - Body:
      - `username` (string, required): The username for the new user.
      - `email` (string, required): The email address for the new user.
      - `password` (string, required): The password for the new user.
      - `password2` (string, required): Confirmation of the password.
  - Responses:
    - Status Code: 201 Created
      - Body:

        ```json
        {
            "message": "User created successfully"
        }
        ```

    - Status Code: 400 Bad Request
      - Body:
        - When required fields are missing or not provided:

          ```json
          {
              "message": "Username, email, and both password fields are required"
          }
          ```

        - When a user with the same username already exists:

          ```json
          {
              "message": "Username already exists"
          }
          ```

        - When a user with the same email already exists:

          ```json
          {
              "message": "Email already exists"
          }
          ```

        - When the provided passwords do not match:

          ```json
          {
              "message": "Passwords do not match"
          }
          ```

- **Login View**
  - URL: `/login/`
  - Method: `POST`
  - Description: Log in a user with a valid username and password.
  - Authentication: Not required.
  - Request:
    - Body:
      - `username` (string, required): The username of the user to log in.
      - `password` (string, required): The password of the user.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "message": "Login successful"
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "Login failed"
        }
        ```

- **List Books**
  - URL: `/books/`
  - Method: `GET`
  - Description: Retrieve a list of books with their details, including title, image URL, content, date published, and published by information.
  - Authentication: Not required.
  - Responses:
    - Status Code: 200 OK
    - Body:

        ```json
        [
            {
            "id": 1,
            "title": "Book Title 1",
            "image_url": "https://example.com/image1.jpg",
            "content": "Book content goes here.",
            "date_published": "2023-09-20T10:00:00Z",
            "published_by": {
                "username": "admin",
                "email": "admin@example.com"
            }
            },
            {
            "id": 2,
            "title": "Book Title 2",
            "image_url": "https://example.com/image2.jpg",
            "content": "Another book content.",
            "date_published": "2023-09-21T11:00:00Z",
            "published_by": {
                "username": "author2",
                "email": "author2@example.com"
            }
            }
        ]
        ```

- **View Book Details**
  - URL: `/books/<int:id>/`
  - Method: `GET`
  - Description: View details of a specific book, including its title, image URL, content, date published, author information, comments, ratings, total comments, and average rating.
  - Authentication: Not required.
  - Responses:
    - Status: 200 OK
    - Body:

        ```json
        {
            "id": 1,
            "title": "Book Title 1",
            "image_url": "https://example.com/image1.jpg",
            "content": "Book content goes here.",
            "date_published": "2023-09-20T10:00:00Z",
            "published_by": {
            "username": "admin",
            "email": "admin@example.com"
            },
            "comments": [
            {
                "id": 1,
                "content": "Great book!",
                "date_posted": "2023-09-21T12:00:00Z",
                "user": {
                "username": "user1",
                "email": "user1@example.com"
                }
            }
            ],
            "ratings": [
            {
                "id": 1,
                "rating": 5,
                "user": {
                "username": "user1",
                "email": "user1@example.com"
                }
            }
            ],
            "total_comments": 1,
            "average_rating": 5.0
        }
        ```

- **Upload a Book (Admin Only)**
  - URL: `/books/upload/`
  - Method: `POST`
  - Description: Upload a new book to the platform. Only admin users are authorized to perform this action.
  - Authentication: Required (admin user).
  - Request:
    - Body:
      - `title` (string, required): The title of the book.
      - `image_url` (string, default: empty string): The URL of the book cover image.
      - `content` (string, required): The content of the book.
      - `date_published` (string, default: current date and time): The date and time when the book was published.
  - Responses:
    - Status: 201 Created
    - Body:

        ```json
        {
            "id": 3,
            "title": "New Book Title",
            "image_url": "https://example.com/new_image.jpg",
            "content": "New book content goes here.",
            "date_published": "2023-09-22T09:30:00Z",
            "published_by": {
            "username": "adminuser",
            "email": "adminuser@example.com"
            }
        }
        ```

- **Add Comment to a Book**
  - URL: `/books/<int:id>/comment/`
  - Method: `POST`
  - Description: Add a comment to a specific book.
  - Authentication: Required (logged-in user).
  - Request:
    - Body:
      - `content` (string, required): The comment to add to the book.
  - Responses:
    - Status: 201 Created
    - Body:

        ```json
        {
            "id": 2,
            "content": "Another comment on this book.",
            "date_posted": "2023-09-23T13:45:00Z",
            "user": {
            "username": "user2",
            "email": "user2@example.com"
            }
        }
        ```

- **Add Rating to a Book**
  - URL: `/books/<int:id>/rate/`
  - Method: `POST`
  - Description: Add a rating (1-5) to a specific book.
  - Authentication: Required (logged-in user).
  - Request:
    - Body:
      - `rating` (integer, required): The rating to add to the book.
  - Responses:
    - Staus: 201 Created
    - Body:

        ```json
        {
            "id": 2,
            "rating": 4,
            "user": {
            "username": "user2",
            "email": "user2@example.com"
            }
        }
        ```

### Authentication

- **Logout View**: Requires user authentication. The user must be logged in to log out.

- **Signup View**: Does not require user authentication. Anyone can sign up for a new account.

- **Login View**: Does not require user authentication. Users can log in using their credentials.

- **List Books**: Authentication is not required. Anyone can view the list of books.

- **View Book Details**: Authentication is not required. Anyone can view book details.

- **Upload a Book**: Requires admin authentication. Only admin users can upload books.

- **Add Comment to a Book**: Requires user authentication. Users can add comments after logging in.

- **Add Rating to a Book**: Requires user authentication. Users can add ratings after logging in.
