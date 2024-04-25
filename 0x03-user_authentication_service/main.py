#!/usr/bin/env python3

'''A basic end-to-end integration test for `app.py`.
'''
import requests


EMAIL = "guillaume@holberton.io"
PASSWD = "b4l0u"
NEW_PASSWD = "t4rt1fl3tt3"
BASE_URL = "http://0.0.0.0:5000"


def register_user(email: str, password: str) -> None:
    '''Here we tests registeration module.
    '''
    url = "{}/users".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    result = requests.post(url, data=body)
    assert result.status_code == 200
    assert result.json() == {"email": email, "message": "user created"}
    result = requests.post(url, data=body)
    assert result.status_code == 400
    assert result.json() == {"message": "email already registered"}


def log_in_wrong_password(email: str, password: str) -> None:
    '''Here we test logging in with a wrong password.
    '''
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    result = requests.post(url, data=body)
    assert result.status_code == 401


def log_in(email: str, password: str) -> str:
    '''Tests logging in.
    '''
    url = "{}/sessions".format(BASE_URL)
    body = {
        'email': email,
        'password': password,
    }
    result = requests.post(url, data=body)
    assert result.status_code == 200
    assert result.json() == {"email": email, "message": "logged in"}
    return result.cookies.get('session_id')


def profile_unlogged() -> None:
    '''Here we tests retrieving profile information whilst logged out.
    '''
    url = "{}/profile".format(BASE_URL)
    result = requests.get(url)
    assert result.status_code == 403


def profile_logged(session_id: str) -> None:
    '''Here we test fetching user data while logged in.
    '''
    url = "{}/profile".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    result = requests.get(url, cookies=req_cookies)
    assert result.status_code == 200
    assert "email" in result.json()


def log_out(session_id: str) -> None:
    '''Here we tests logging out of a session.
    '''
    url = "{}/sessions".format(BASE_URL)
    req_cookies = {
        'session_id': session_id,
    }
    result = requests.delete(url, cookies=req_cookies)
    assert result.status_code == 200
    assert result.json() == {"message": "Bienvenue"}


def reset_password_token(email: str) -> str:
    '''Here we tests requesting a password reset.
    '''
    url = "{}/reset_password".format(BASE_URL)
    body = {'email': email}
    result = requests.post(url, data=body)
    assert result.status_code == 200
    assert "email" in result.json()
    assert result.json()["email"] == email
    assert "reset_token" in result.json()
    return result.json().get('reset_token')


def update_password(email: str, reset_token: str, new_password: str) -> None:
    '''Here we tests updating a user's password.
    '''
    url = "{}/resultet_password".format(BASE_URL)
    body = {
        'email': email,
        'reset_token': reset_token,
        'new_password': new_password,
    }
    result = requests.put(url, data=body)
    assert result.status_code == 200
    assert result.json() == {"email": email, "message": "Password updated"}


if __name__ == "__main__":
    register_user(EMAIL, PASSWD)
    log_in_wrong_password(EMAIL, NEW_PASSWD)
    profile_unlogged()
    session_id = log_in(EMAIL, PASSWD)
    profile_logged(session_id)
    log_out(session_id)
    reset_token = reset_password_token(EMAIL)
    update_password(EMAIL, reset_token, NEW_PASSWD)
    log_in(EMAIL, NEW_PASSWD)
