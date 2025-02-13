# Introduction and Project Goals

- The API is hosted at E-Pics back-end. [Heroku-back-end](https://my-e-pics-d3d3d941434e.herokuapp.com/).
- You can find the back-end code for this API on GitHub. [Github back-end](https://github.com/SamGree/e-pics).
- The API is hosted at E-Pics live link.[E-pics](https://last-epics-76629a697a31.herokuapp.com/).
- You can find the front-end code for this API on GitHub.[Github frond-end](https://github.com/SamGree/last).
- This platform provides all the necessary functionality for users to carry out CRUD operations on the back-end.
  E-Pics is a photo-sharing platform where users can upload and share images with others.
  All uploaded photos are freely available for download, fostering a collaborative and sharing community.
  Users can create accounts to engage in various interactions, such as uploading and downloading images, liking, commenting, and saving images to albums within their profile.

---

## Table of Contents

- [Project Models](#project-models)
  - [albums](#albums)
  - [commentlikes](#commentlikes)
  - [comments](#comments)
  - [postlikes](#postlikes)
  - [posts](#posts)
  - [posttags](#posttags)
  - [tags](#tags)
  - [users](#users)
- [Unit Tests](#unit-tests)
- [Postman](#postman)
- [Deployment](#deployment)

---

### Albums App

| Name       | KYE             | TYPE             | EXTRA                            |
| ---------- | --------------- | ---------------- | -------------------------------- |
| user       | ForeignKey      | user             | CASCADE                          |
| name       | CharField       | String (max=100) | Required                         |
| created_at | DateTimeField   | DateTime         | auto_now_add                     |
| posts      | ManyToManyField | Post             | blank=True,related_name='albums' |

### commentlikes

| Name       | KYE           | TYPE                   | EXTRA                                |
| ---------- | ------------- | ---------------------- | ------------------------------------ |
| user       | ForeignKey    | User (AUTH_USER_MODEL) | CASCADE,related_name='comment_likes' |
| comment    | ForeignKey    | Comment                | CASCADE,related_name='comment_likes' |
| created_at | DateTimeField | DateTime               | auto_now_add                         |

### comments

| Name       | KYE             | TYPE                   | EXTRA                                     |
| ---------- | --------------- | ---------------------- | ----------------------------------------- |
| content    | TextField       |                        |                                           |
| user       | ForeignKey      | AUTH_USER_MODEL (User) | CASCADE, related_name='comments'          |
| post       | ForeignKey      | Post                   | CASCADE, related_name='comments'          |
| created_at | DateTimeField   |                        | auto_now_add=True (Set once when created) |
| likes      | ManyToManyField | AUTH_USER_MODEL (User) | blank=True, related_name='liked_comments' |

### postlikes

| Name       | KYE           | TYPE                   | EXTRA                                     |
| ---------- | ------------- | ---------------------- | ----------------------------------------- |
| user       | ForeignKey    | AUTH_USER_MODEL (User) | CASCADE, related_name='post_likes'        |
| post       | ForeignKey    | post                   | CASCADE, related_name='post_likes'        |
| created_at | DateTimeField |                        | auto_now_add=True (Set once when created) |

### posts

| Name           | KYE                  | TYPE                   | EXTRA                                     |
| -------------- | -------------------- | ---------------------- | ----------------------------------------- |
| title          | CharField            | -                      | max_length=100 (Required)                 |
| description    | TextField            | -                      | Required                                  |
| image          | CloudinaryField      | -                      | Stores image via Cloudinary               |
| download_count | PositiveIntegerField | -                      | default=0                                 |
| created_at     | DateTimeField        | -                      | auto_now_add=True (Set once when created) |
| user           | ForeignKey           | User                   | CASCADE, related_name='posts'             |
| likes          | ManyToManyField      | AUTH_USER_MODEL (User) | blank=True, related_name='liked_posts'    |

### posttags

| Name       | KYE           | TYPE | EXTRA                                |
| ---------- | ------------- | ---- | ------------------------------------ |
| post       | ForeignKey    | Post | CASCADE, related_name='post_tags'    |
| tag        | ForeignKey    | Tag  | CASCADE, related_name='post_tags'    |
| created_at | DateTimeField | -    | auto_now_add=True (Set when created) |

### tags

| Name       | KYE           | TYPE | EXTRA                                |
| ---------- | ------------- | ---- | ------------------------------------ |
| name       | CharField     | -    | max_length=50, unique=True           |
| created_at | DateTimeField | -    | auto_now_add=True (Set when created) |

### users

- Model inherits fields from AbstractUser
  | Name | KYE | TYPE | EXTRA |
  | ---------- | ------------- | ---- | -------------------- |
  |id| AutoField| Django default| Primary Key (Automatically generated)|
  |username| CharField| Inherited from AbstractUser |Unique Identifier|
  |email| EmailField| Inherited from AbstractUser| Unique, Optional|
  |password| CharField| Inherited from AbstractUser |Hashed for security|
  |profile_image|CloudinaryField| Custom Field |Stores profile image via Cloudinary|
  |bio|TextField| Custom Field|Optional user bio (blank=True, null=True)|
  ***
  ***

## Unit Tests

- Tests for my Albums models.
  ![Albums models](/readme.img/album.test.png)
- Creates test instances of User, Post, and Album to use across multiple tests.
  test_album_creation:
  Verifies that an album is created with the correct name, user, and that created_at is not null.
  test_album_posts_relationship:
  Ensures the ManyToManyField relationship between Album and Post works correctly.
  test_album_string_representation:
  Checks that the **str** method returns the album name.
  test_related_name_for_user:
  Confirms that the related_name='albums' for the user field works, allowing access to all albums of a user.
  test_related_name_for_post:
  Ensures the related_name='albums' for the posts field works, allowing access to all albums a post belongs to.

---

- Tests for my commentlikes models.
- ![commentlikes models](/readme.img/commentlikes.test.png)
- Creates test instances for User, Post, and Comment, which are required for the CommentLike model tests.
  test_commentlike_creation:
  Validates that a CommentLike can be created with the correct user and comment.
  test_commentlike_unique_constraint:
  Ensures the database enforces the UniqueConstraint on user and comment fields to prevent duplicate likes.
  test_commentlike_related_name_for_user:
  Verifies that the related_name='comment_likes' on the user field works, allowing access to all likes by a user.
  test_commentlike_related_name_for_comment:
  Checks the related_name='comment_likes' on the comment field to ensure it works correctly.
  test_commentlike_str_representation:
  Confirms that the **str** method returns the expected string representation.

---

- Tests for my comments models.
- ![comments models](/readme.img/comments.py.test.png)
- Creates test instances for User, Post, and Comment, which are reused across tests. test_comment_creation: Verifies that a Comment can be created with the correct content, user, post, and created_at values. test_comment_related_name_for_post: Tests the related_name='comments' for the post field, ensuring you can access all comments on a post. test_comment_related_name_for_user: Tests the related_name='comments' for the user field, ensuring you can access all comments by a user. test_comment_str_representation: Ensures the str method returns the expected string format: "Comment by on ". test_comment_likes_relationship: Tests the many-to-many likes relationship, ensuring: Users can like a comment. The related_name='liked_comments' allows access to all comments a user has liked.

---

- Tests for my postlikes models.
- ![postlikes](/readme.img/postlikes.test.png)
- Creates test instances of User, Post, and PostLike. test_postlike_creation: Ensures that a PostLike can be created and its fields (user, post, and created_at) are populated correctly. test_postlike_unique_constraint: Validates that the UniqueConstraint on user and post prevents duplicate likes by the same user for the same post. test_postlike_related_name_for_user: Ensures that the related_name='post_likes' for the user field works, allowing access to all likes by a user. test_postlike_related_name_for_post: Ensures that the related_name='post_likes' for the post field works, allowing access to all likes on a post. test_postlike_str_representation:
  Checks that the str method of the PostLike model returns the expected string format: "username likes post title".

---

- Tests for my posts models.
  ![posts models](/readme.img/posts.test.py.png)
- Post API Test Suite
  The PostAPITest class tests the API endpoints for managing posts, tags, and related features. It ensures proper functionality, authentication, and data integrity. Below are the key tests:
  List Posts: Verifies that the API retrieves a list of posts (GET /list-create-posts).
  Create Post: Tests creating a new post with tags (POST /list-create-posts).
  Retrieve Post: Ensures a specific post can be retrieved by ID (GET /detail-post/{post_id}).
  Update Post: Confirms a post owner can update their post (PATCH /detail-post/{post_id}).
  Delete Post: Verifies the owner can delete their post (DELETE /detail-post/{post_id}).
  Unauthenticated Access: Ensures unauthenticated users cannot create posts.
  Post Download: Tests downloading a post and increments the download count.
  Search Posts: Validates search functionality by title, username, or tags (GET /search).
  This test suite covers authentication, CRUD operations, and edge cases to ensure the API behaves as expected.

---

- Tests for my users app.
- ![users app](/readme.img/users.test.png)
- The User API Test Suite ensures that user authentication, registration, profile retrieval, updating, and logout functionalities work correctly. It follows the CRUD (Create, Read, Update, Delete) principles by testing different API endpoints. The test suite starts by setting up a test user and authentication token using Django's TestCase and APIClient(). This allows the simulation of authenticated requests. The test cases verify if users can successfully register, log in, log out, retrieve their profiles, and update their details. For user registration, the test checks if a new user can sign up with valid credentials and prevents duplicate username registration. The login test ensures that users can log in with correct credentials and receive an authentication token, while invalid credentials result in an error. The logout test verifies that authenticated users can log out and their session is invalidated. The test suite also includes profile-related operations. It ensures that authenticated users can retrieve their profile details and update their profile bio, while unauthenticated users are restricted from making profile updates.

---

## Postman

- The Postman collection file for this project is located at [postman](https://github.com/SamGree/e-pics/blob/main/postman/postman.json) .
- You can import this file into Postman to access the collection of API endpoints and test them.
- Import from postman
- Open Postman.
- Dropdown three dots next to you app name.
  ![postman](/readme.img/postmanj.png)
- Click on export.
- This will direct you to your computer files where you can choose to locate your postman file.
- By importing the Postman collection, you can seamlessly access and test the API endpoints of the E-PICS Task Management System for functionality.
- I have thoroughly tested all my apps using Postman to ensure that the CRUD operations function correctly.

---

## Deployment

- E-pics is deployed on Heroku using Heroku PostgreSQL as the database

1. Create a Heroku account and install the Heroku CLI.
2. Log in to Heroku CLI (heroku login) and create a new Heroku app (heroku create).
3. Set up Heroku PostgreSQL as the database (in settings Config Vars).
4. Push your code to the Heroku remote (git push heroku master).
5. Run migrations and set up the database (heroku run python manage.py migrate).
6. Your E-pics application should now be deployed and accessible via the provided Heroku app URL.
7. Your app should now be deployed and accessible via the provided Heroku URL.

---

## Technologies Used

- **Core Technologies**
  - Python – Main programming language.
  - Django (v5.1.4) – Web framework for building the backend.
  - Django REST Framework (DRF) Used for building REST APIs.
- **Authentication & Security**
  - dj-rest-auth – Provides authentication endpoints.
  - django-allauth – Handles social authentication.
  - djangorestframework-simplejwt – JWT authentication.
  - django-cors-headers – Manages CORS policies.
- **Database & ORM**
  - PostgreSQL – Database management system.
  - dj-database-url (v0.5.0) – Database configuration tool.
  - psycopg2-binary (v2.9.10) – PostgreSQL adapter for Django.
  - sqlparse – SQL query parsing.
- **Cloud & Storage**
  - Cloudinary (v1.41.0) – Cloud-based media storage.
  - django-cloudinary-storage (v0.3.0) – Cloudinary integration for Django.
  - pillow (v11.0.0) – Image processing library.
- **Deployment & Server**
  - Gunicorn (v23.0.0) – WSGI HTTP server for running the application.
  - Whitenoise (v6.8.2) – Serves static files efficiently.
  - Heroku – Cloud platform for deployment.
- **Utilities & Other Dependencies**
  - asgiref (v3.8.1) – ASGI compatibility for Django.
  - pillow (v11.0.0) – Image processing library.
  - python-decouple (v3.8) – Handles environment variables.
  - requests-oauthlib (v2.0.0) – OAuth authentication.
  - tzdata (v2024.2) – Timezone management.
  - pytz (v2024.2) – Timezone utilities.

## Validation

- I used [PEP8 CI Python linter](https://pep8ci.herokuapp.com/) validation to all my files, and Results:
  All clear, no errors found.

---

## Bugs

- I wrote the app name capital letter instead of small letter, error solved
- ![P to p](/readme.img/fix.P.to.p.png)

---

- Error occured because of os was not imported.
- ![os](/readme.img/forgot.import%20os.png)

---

- This error appears after deployment; if I wanted to add a post to the album, first click shows error, but second click on the same image then show the successful message.
- ![frontalbum](/readme.img/viewalbum.jpg)
- after debugging, the error I had was in the views.py albums, because (Ok) was not in _capital letter_ by changing to capital letter (OK) error solved
- ![views albums](/readme.img/viewalbum1.png)

---

## Credits
