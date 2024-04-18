#!/usr/bin/env python3

'''The Session authentication with expiration
and storage support module for the API.
'''
from flask import request
from datetime import datetime, timedelta

from models.user_session import UserSession
from .session_exp_auth import SessionExpAuth


class SessionDBAuth(SessionExpAuth):
    '''The session authentication class with expiration and storage support.
    '''

    def start_session(self, user_id=None) -> str:
        '''Here, we Created and stores a session id for the user.
        '''
        session_id = super().start_session(user_id)
        if type(session_id) == str:
            kwargs = {
                'user_id': user_id,
                'session_id': session_id,
            }
            user_session = UserSession(**kwargs)
            user_session.save()
            return session_id

    def UserID_for_SessionID(self, session_id=None):
        '''Here, we retrieved the user id of the user associated with
        a given session id.
        '''
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return None
        if len(sessions) <= 0:
            return None
        time_now = datetime.now()
        time_span = timedelta(seconds=self.session_duration)
        time_expired = sessions[0].created_at + time_span
        if time_expired < time_now:
            return None
        return sessions[0].user_id

    def destroy_session(self, request=None) -> bool:
        '''Destroys an authenticated session.
        '''
        session_id = self.session_cookie(request)
        try:
            sessions = UserSession.search({'session_id': session_id})
        except Exception:
            return False
        if len(sessions) <= 0:
            return False
        sessions[0].remove()
        return True
