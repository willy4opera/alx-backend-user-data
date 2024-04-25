#!/usr/bin/env python3

'''In this task you will define a _hash_password method
that takes in a password string arguments and returns bytes.
'''
import bcrypt
from uuid import uuid4
from typing import Union
from sqlalchemy.orm.exc import NoResultFound

from db import DB
from user import User


def _hash_password(password: str) -> bytes:
    '''Hashes a password.
    '''
    return bcrypt.hashpw(password.encode("utf-8"), bcrypt.gensalt())


class Auth:
    '''Here, we define the
    auth class to interact with the authentication database.
    '''

    def __init__(self):
        '''Here, we initialized the new Auth instance.
        '''
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
        '''A The adds new user to the database method.
        '''
        try:
            self._db.find_user_by(email=email)
        except NoResultFound:
            return self._db.add_user(email, _hash_password(password))
        raise ValueError("User {} already exists".format(email))
