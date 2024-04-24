# PROJECT AUTHOR : ODIONYE OBIAJULU WILLIAMS
#  PROJECT TITLE : Authentication Service

The content of this project are tasks for learning to create user authentication systems and services.

## Project Requirements/Dependencies

+ bcrypt
+ python3 3.7
+ SQLAlchemy 1.3.x
+ pycodestyle 2.5


# Completed Task

+ [x] 0. **User model**<br />[user.py](user.py) contains the SQLAlchemy model named `User` for the database table named `users` (by using the [mapping declaration](https://docs.sqlalchemy.org/en/13/orm/tutorial.html#declare-a-mapping) of SQLAlchemy) and meets the following requirements:

  + The model for this task have the following attributes:
    + `id`, the integer primary key.
    + `email`, the non-nullable string.
    + `hashed_password`, the non-nullable string.
    + `session_id`, the nullable string.
    + `reset_token`, the nullable string.
