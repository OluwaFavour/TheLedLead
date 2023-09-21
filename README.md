# TheLedLead API Documentation

This API allows users to interact with TheLedLead website. Users can perform actions such as signing up, logging in, and logging out.

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

### Authentication

- **Logout View**: Requires user authentication. The user must be logged in to log out.

- **Signup View**: Does not require user authentication. Anyone can sign up for a new account.

- **Login View**: Does not require user authentication. Users can log in using their credentials.
