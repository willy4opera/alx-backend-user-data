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

