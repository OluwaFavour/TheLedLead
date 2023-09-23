# TheLedLead API Documentation

TheLedLead API empowers users to engage with TheLedLead website, offering a range of interactive functionalities. Users can seamlessly create accounts, log in, log out, explore available books, post comments, and rate books. For book uploads, exclusive privileges are granted to admin users, enabling them to contribute new content to the platform.

`Get csrf token from cookies and add it to the header of each POST request`

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

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "Not logged in"
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
  
    - Status Code: 400 Bad Request
      - Body:
        - When user is already logged in:

          ```json
          {
              "message": "Already logged in"
          }
          ```

        - When username is not provided:

          ```json
          {
              "message": "Username is required"
          }
          ```

        - When password is not provided:

          ```json
          {
              "message": "Password is required"
          }
          ```

    - Status Code: 404 Not Found
      - Body:
        - When user does not exist:

          ```json
          {
              "message": "User does not exist"
          }
          ```

- **Change Password View**
  - URL: `/change-password/`
  - Method: `POST`
  - Description: Change the password of an authenticated user.
  - Authentication: Required (user must be logged in).
  - Request:
    - Body:
      - `old_password` (string, required): The user's current password.
      - `new_password1` (string, required): The new password.
      - `new_password2` (string, required): Confirm the new password.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "message": "Password changed successfully"
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:
        - When the user is not logged in:

          ```json
          {
              "message": "Not logged in"
          }
          ```

    - Status Code: 400 Bad Request
      - Body:
        - When old password is not provided:

          ```json
          {
              "message": "Old password is required"
          }
          ```

        - When new password is not provided:

          ```json
          {
              "message": "New password is required"
          }
          ```

        - When confirm password is not provided:

          ```json
          {
              "message": "Confirm password is required"
          }
          ```

        - When new password and confirm password do not match:

          ```json
          {
              "message": "New password and confirm password do not match"
          }
          ```

- **List Books View**
  - URL: `/books/`
  - Method: `GET`
  - Description: Retrieve a list of books with details, including average rating, total ratings, and total comments.
  - Authentication: Not required.
  - Request:
    - Body: None

  - Responses:
    - Status Code: 200 OK
      - Body: A JSON array containing book details, including average rating, total ratings, and total comments.

        ```json
        [
            {
                "id": (int) Book ID,
                "title": (string) Book title,
                "image_url": (string) URL to the book's image (if available),
                "content": (string) Book content,
                "date_published": (string) Date the book was published,
                "published_by": {
                    "username": (string) Username of the publisher (if available),
                    "email": (string) Email of the publisher (if available)
                },
                "average_rating": (float) Average rating of the book,
                "total_ratings": (int) Total number of ratings for the book,
                "total_comments": (int) Total number of comments for the book
            },
            // ... (more book entries)
        ]
        ```

- **Book View**
  - URL: `/books/{id}/`
  - Method: `GET`
  - Description: Retrieve details of a book including comments, ratings, and reader information.
  - Authentication: Required.
  - Request:
    - Body: None
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "id": 1,
            "title": "Sample Book",
            "image_url": "http://example.com/book.jpg",
            "content": "Lorem ipsum...",
            "date_published": "2023-09-21T12:34:56Z",
            "published_by": {
                "username": "author123",
                "email": "author@example.com"
            },
            "comments": [
                {
                    "id": 101,
                    "content": "Great book!",
                    "date_posted": "2023-09-22T08:45:00Z",
                    "user": {
                        "username": "user456",
                        "email": "user456@example.com"
                    }
                },
                {
                    "id": 102,
                    "content": "I loved it!",
                    "date_posted": "2023-09-23T14:20:00Z",
                    "user": {
                        "username": "user789",
                        "email": "user789@example.com"
                    }
                }
            ],
            "ratings": [
                {
                    "id": 201,
                    "rating": 5,
                    "user": {
                        "username": "user456",
                        "email": "user456@example.com"
                    }
                },
                {
                    "id": 202,
                    "rating": 4,
                    "user": {
                        "username": "user789",
                        "email": "user789@example.com"
                    }
                }
            ],
            "total_comments": 2,
            "average_rating": 4.5
        }
        ```

  - Additional Notes:
    - When a user successfully retrieves book details, the book is marked as "read" by that user, and the book's readership information is updated.

- **Upload Book View**
  - URL: `/books/upload/`
  - Method: `POST`
  - Description: Allows authorized staff users to upload a new book.
  - Authentication: Required for staff users.
  - Request:
    - Body (multipart/form-data):
      - `title` (string, required): The title of the book.
      - `content` (text, required): The content or description of the book.
      - `image_url` (file, optional): An image file representing the book's cover.
  - Responses:
    - Status Code: 201 Created
      - Body (JSON):

        ```json
        {
            "id": 1,
            "title": "Sample Book",
            "image_url": "/media/book_covers/sample-book/sample.jpg",
            "content": "This is a sample book description.",
            "date_published": "2023-09-21T12:34:56.789Z",
            "published_by": {
                "username": "admin",
                "email": "admin@example.com"
            }
        }
        ```

      - Description: The book has been successfully created and returned as JSON.

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

      - Description: User is not authenticated.

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to perform this action"
        }
        ```

      - Description: User is not authorized to upload books.

    - Status Code: 400 Bad Request
      - Body:
        - When `title` or `content` is empty:

          ```json
          {
              "message": "Title or content cannot be empty"
          }
          ```

        - When invalid or missing data is sent in the request.

  - Notes:
    - The `image_url` field is optional, but you can include an image file to represent the book's cover.
    - The `date_published` field is automatically generated upon book creation.
    - The `published_by` field indicates the user who published the book.

- **Update Book View**
  - URL: `/books/{id}/update/` (Replace `{id}` with the book's ID)
  - Method: `PATCH`
  - Description: Update the details of a book, such as title, content, or image.
  - Authentication: Required for admin users.
  - Request:
    - Body (multipart/form-data):
      - `title` (string, optional): The updated title of the book.
      - `content` (string, optional): The updated content of the book.
      - `image_url` (file, optional): The updated book cover image.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "id": 123,
            "title": "Updated Book Title",
            "image_url": "http://example.com/media/book_covers/updated-book-title/image.jpg",
            "content": "Updated book content...",
            "date_published": "2023-09-21T12:34:56Z",
            "published_by": {
                "username": "admin",
                "email": "admin@example.com"
            }
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to perform this action"
        }
        ```

    - Status Code: 404 Not Found
      - Body:

        ```json
        {
            "message": "Book not found"
        }
        ```

    - Status Code: 200 OK (When no changes are made)
      - Body:

        ```json
        {
            "message": "Nothing changed"
        }
        ```

  - Additional Notes:
    - This endpoint allows admin users to update book details such as title, content, or the book cover image.
    - The `date_published` field is automatically updated to the current date and time when the book is updated.

- **Delete Book View**
  - URL: `/books/{id}/update/`
  - Method: `DELETE`
  - Description: Delete a book with the specified ID if the user is authorized and the book exists.
  - Authentication: Required (User must be authenticated and have staff privileges).
  - Request:
    - Headers:
      - `Authorization` (string, required): Token or credentials for user authentication.
    - URL Parameters:
      - `id` (integer, required): The unique identifier of the book to be deleted.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "message": "Book deleted successfully"
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to perform this action"
        }
        ```

    - Status Code: 404 Not Found
      - Body:
        - When the specified book does not exist:

          ```json
          {
              "message": "Book not found"
          }
          ```

  - Additional Notes:
    - This endpoint requires user authentication, and the user must have staff privileges to delete a book.

- **Add Comment to a Book**
  - URL: `/books/comment/<int:id>/`
  - Method: `POST`
  - Description: Allows an authenticated user to add a comment to a book.
  - Authentication: Required (user must be logged in).
  - Request:
    - Body:
      - `content` (string, required): The content of the comment.
  - Responses:
    - Status Code: 201 Created
      - Body:

        ```json
        {
            "id": 1,
            "content": "This is a great book!",
            "date_posted": "2023-09-25T14:30:00Z",
            "user": {
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

    - Status Code: 400 Bad Request
      - Body:
        - When `content` is not provided:

          ```json
          {
              "message": "Content is required"
          }
          ```

- **Add Rating View**
  - URL: `/books/rate/<int:id>/`
  - Method: `POST`
  - Description: Add or update a user's rating for a book. Ratings must be between 1 and 5.
  - Authentication: Required.
  - Request:
    - Body:
      - `rating` (integer, required): The rating to add or update (must be between 1 and 5).
  - Responses:
    - Status Code: 201 Created
      - Body:

        ```json
        {
            "id": 1,
            "rating": 4,
            "user": {
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
        ```

    - Status Code: 200 OK (Updated Rating)
      - Body:

        ```json
        {
            "id": 1,
            "rating": 5,
            "user": {
                "username": "john_doe",
                "email": "john@example.com"
            }
        }
        ```

    - Status Code: 400 Bad Request
      - Body:
        - When rating is less than 1 or greater than 5:

          ```json
          {
              "message": "Rating must be between 1 and 5"
          }
          ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

  - Additional Notes:
    - If a user has already rated the book, their existing rating will be updated with the new rating value.

- **Admin Dashboard**
  - URL: `/tll-admin/`
  - Method: `GET`
  - Description: Access the admin dashboard if you have the necessary authorization.
  - Authentication: Required (Admin user).
  - Request: Not applicable.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "message": "This is the admin dashboard"
        }
        ```

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to access this page"
        }
        ```

  - Additional Notes:
    - This endpoint is used to access the admin dashboard, and it requires the user to be logged in as an admin. If the user is not an admin, a "403 Forbidden" response will be returned.

- **Get All-Time Views**
  - URL: `/tll-admin/views/`
  - Method: `GET`
  - Description: Retrieve the total number of views across all books.
  - Authentication: Required for admin users.
  - Request:
    - Headers:
      - `Authorization` (string, required): Token or session-based authentication.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "views": 12345
        }
        ```

      - Description: Returns the total number of views across all books.

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

      - Description: Returned when the user is not authenticated.

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to access this page"
        }
        ```

      - Description: Returned when the authenticated user is not an admin.

  - Additional Notes: This endpoint allows admin users to retrieve the total number of views across all books on TheLedLead website. It requires authentication, and only admin users are authorized to access this page. The response provides the total view count.

- **Get Views Per Book**
  - URL: `/tll-admin/views/<int:id>/`
  - Method: `GET`
  - Description: Retrieve the number of views for a specific book.
  - Authentication: Required for admin users.
  - Request:
    - Headers:
      - `Authorization` (string, optional): Bearer token for authentication (if logged in).
    - Path Parameters:
      - `id` (integer, required): The unique identifier of the book to retrieve views for.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "id": 1,
            "views": 42
        }
        ```

      - Description: Returns the number of views for the specified book.

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

      - Description: Indicates that the user is not authenticated.

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to access this page"
        }
        ```

      - Description: Indicates that the user does not have the necessary permissions to access this endpoint.

    - Status Code: 404 Not Found
      - Body:

        ```json
        {
            "message": "Book not found"
        }
        ```

      - Description: Indicates that the book with the specified ID does not exist.

  - Additional Notes:
    - This endpoint is intended for admin users only. It allows them to retrieve the number of views for a specific book.

- **Get Yearly Views**
  - URL: `/tll-admin/views/<int:year>/`
  - Method: `GET`
  - Description: Retrieve the number of books read and views for a specified year.
  - Authentication: Required, user must be logged in as an admin.
  - Parameters:
    - `year` (integer, required): The year for which you want to retrieve views.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "year": 2023,
            "number of books read": 10,
            "views": 120
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to access this page"
        }
        ```

- **Get Yearly Views Per Book**
  - URL: `/tll-admin/views/<int:year>/<int:id>/`
  - Method: `GET`
  - Description: Retrieve the number of views for a specific book in a specified year.
  - Authentication: Required, user must be logged in as an admin.
  - Parameters:
    - `year` (integer, required): The year for which you want to retrieve views.
    - `id` (integer, required): The ID of the book for which you want to retrieve views.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "year": 2023,
            "id": 1,
            "views": 30
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to access this page"
        }
        ```

- **Get Monthly Views**
  - URL: `/tll-admin/views/<int:year>/<int:month>/`
  - Method: `GET`
  - Description: Retrieve the number of books read and views for a specified month within a year.
  - Authentication: Required, user must be logged in as an admin.
  - Parameters:
    - `year` (integer, required): The year for which you want to retrieve views.
    - `month` (integer, required): The month number (1-12) for which you want to retrieve views.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "year": 2023,
            "month_number": 7,
            "month_name": "July",
            "number of books read": 5,
            "views": 60
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to access this page"
        }
        ```

- **Get Monthly Views Per Book**
  - URL: `/tll-admin/views/<int:year>/<int:month>/<int:id>/`
  - Method: `GET`
  - Description: Retrieve the number of views for a specific book in a specified month and year.
  - Authentication: Required, user must be logged in as an admin.
  - Parameters:
    - `year` (integer, required): The year for which you want to retrieve views.
    - `month` (integer, required): The month number (1-12) for which you want to retrieve views.
    - `id` (integer, required): The ID of the book for which you want to retrieve views.
  - Responses:
    - Status Code: 200 OK
      - Body:

        ```json
        {
            "year": 2023,
            "month_number": 7,
            "month_name": "July",
            "id": 1,
            "views": 20
        }
        ```

    - Status Code: 401 Unauthorized
      - Body:

        ```json
        {
            "message": "You are not logged in"
        }
        ```

    - Status Code: 403 Forbidden
      - Body:

        ```json
        {
            "message": "You are not authorized to access this page"
        }
        ```

- Notes:
  - The endpoints allow administrators to retrieve views statistics for books read in specific years and months.
  - Authentication is required, and only admin users have access to these endpoints.
  - The response includes the number of books read and the total views for the specified period.
  - There are also specific endpoints to retrieve views for a particular book in a given year or month.
  - Month names are included in the response for better readability.

## Authentication

- **Logout View**: Requires user authentication. The user must be logged in to log out.

- **Signup View**: Does not require user authentication. Anyone can sign up for a new account.

- **Login View**: Does not require user authentication. Users can log in using their credentials.

- **List Books**: Authentication is not required. Anyone can view the list of books.

- **View Book Details**: Authentication is not required. Anyone can view book details.

- **Upload a Book**: Requires admin authentication. Only admin users can upload books.

- **Update a Book**: Requires admin authentication. Only admin users can update books.

- **Delete a Book**: Requires admin authentication. Only admin users can delete books.

- **Add Comment to a Book**: Requires user authentication. Users can add comments after logging in.

- **Add Rating to a Book**: Requires user authentication. Users can add ratings after logging in.

- **Admin Dashboard**: Requires admin authentication. Only admin users can access the admin dashboard.

- **Get All-Time Views**: Requires admin authentication. Only admin users can access this endpoint.

- **Get Views Per Book**: Requires admin authentication. Only admin users can access this endpoint.

- **Get Yearly Views**: Requires admin authentication. Only admin users can access this endpoint.

- **Get Yearly Views Per Book**: Requires admin authentication. Only admin users can access this endpoint.

- **Get Monthly Views**: Requires admin authentication. Only admin users can access this endpoint.

- **Get Monthly Views Per Book**: Requires admin authentication. Only admin users can access this endpoint.
