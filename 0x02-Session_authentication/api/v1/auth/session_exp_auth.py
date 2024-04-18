#!/usr/bin/env python3

'''The Session authentication with expiration module for the API.
'''
import os
from flask import request
from datetime import datetime, timedelta

from .session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    '''Session authentication class with expiration.
    '''

    def __init__(self) -> None:
        '''Initializes a new SessionExpAuth instance.
        '''
        super().__init__()
        try:
            self.session_duration = int(os.getenv('SESSION_DURATION', '0'))
        except Exception:
            self.session_duration = 0

    def start_session(self, user_id=None):
        '''Here, we created the session id for the user.
        '''
        session_id = super().start_session(user_id)
        if type(session_id) != str:
            return None
        self.user_id_by_session_id[session_id] = {
            'user_id': user_id,
            'created_at': datetime.now(),
        }
        return session_id

    def UserID_for_SessionID(self, session_id=None) -> str:
        '''Retrieves the user id of the user associated with
        a given session id.
        '''
        if session_id in self.user_id_by_session_id:
            session_dict = self.user_id_by_session_id[session_id]
            if self.session_duration <= 0:
                return session_dict['user_id']
            if 'created_at' not in session_dict:
                return None
            cur_time = datetime.now()
            time_span = timedelta(seconds=self.session_duration)
            exp_time = session_dict['created_at'] + time_span
            if exp_time < cur_time:
                return None
            return session_dict['user_id']
