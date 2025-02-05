# Table of Contents

## Introduction and Project Goals

- The API is hosted at E Pics back-end.
  You can find the front-end code for this API on GitHub under last front-end, while the deployed version is available at last-epics.
  This platform provides all the necessary functionality for users to carry out CRUD operations on the front-end.
  E Pics is a photo-sharing platform where users can upload and share images with others.
  All uploaded photos are freely available for download, fostering a collaborative and sharing community.
  Users can create accounts to engage in various interactions, such as uploading and downloading images, liking, commenting, and saving images to albums within their profile.

---

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
  ### Unit Tests
  - Tests for my Albums models.

### Deployment

- E-pics is deployed on Heroku using Heroku PostgreSQL as the database.
  1. Create a Heroku account and install the Heroku CLI.
  2. Log in to Heroku CLI (heroku login) and create a new Heroku app (heroku create).
  3. Set up Heroku PostgreSQL as the database (in settings Config Vars).
  4. Push your code to the Heroku remote (git push heroku master).
  5. Run migrations and set up the database (heroku run python manage.py migrate).
  6. Your E-pics application should now be deployed and accessible via the provided Heroku app URL.
  7. Your app should now be deployed and accessible via the provided Heroku URL.
