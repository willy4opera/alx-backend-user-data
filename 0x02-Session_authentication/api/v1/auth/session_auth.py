#!/usr/bin/env python3

'''The session authentication module for the API.
'''
from uuid import uuid4
from flask import request

from .auth import Auth
from models.user import User


class SessionAuth(Auth):
    '''The session authentication class.
    '''
    UserID_by_SessionID = {}

    def create_session(self, user_id: str = None) -> str:
        '''Here, we created a session id for the user.
        '''
        if type(user_id) is str:
            SessionID = str(uuid4())
            self.UserID_by_SessionID[SessionID] = user_id
            return SessionID

    def user_id_for_session_id(self, SessionID: str = None) -> str:
        '''Here, we retrieved the user id of the user associated with
        a given session id.
        '''
        if type(SessionID) is str:
            return self.UserID_by_SessionID.get(SessionID)

    def current_user(self, request=None) -> User:
        '''Here, we retrieved the user associated with the request.
        '''
        user_id = self.user_id_for_session_id(self.session_cookie(request))
        return User.get(user_id)

    def destroy_session(self, request=None):
        '''Here, we destroyed the authenticated session.
        '''
        SessionID = self.session_cookie(request)
        user_id = self.user_id_for_session_id(SessionID)
        if (request is None or SessionID is None) or user_id is None:
            return False
        if SessionID in self.UserID_by_SessionID:
            del self.UserID_by_SessionID[SessionID]
        return True
