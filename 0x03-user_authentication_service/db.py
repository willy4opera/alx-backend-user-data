#!/usr/bin/env python3

'''The DB module.
'''
from sqlalchemy import create_engine, tuple_
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy.orm.session import Session

from user import Base, User


class DB:
    '''The DB class.
    '''

    def __init__(self) -> None:
        '''Here, we initialize the new DB instance.
        '''
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        '''Store in Memory the session object.
        '''
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        '''Here, we implement the adds a new user to the database.
        '''
        try:
            new_user = User(email=email, hashed_password=hashed_password)
            self._session.add(new_user)
            self._session.commit()
        except Exception:
            self._session.rollback()
            new_user = None
        return new_user

    def find_user_by(self, **kwargs) -> User:
        '''The method finds users based on a set of filters.
        '''
        u_fields, u_values = [], []
        for key, value in kwargs.items():
            if hasattr(User, key):
                u_fields.append(getattr(User, key))
                u_values.append(value)
            else:
                raise InvalidRequestError()
        result = self._session.query(User).filter(
            tuple_(*u_fields).in_([tuple(u_values)])
        ).first()
        if result is None:
            raise NoResultFound()
        return result
