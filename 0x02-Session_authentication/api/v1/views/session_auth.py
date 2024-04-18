#!/usr/bin/env python3

'''The Module of session authenticating views.
'''
import os
from typing import Tuple
from flask import abort, jsonify, request

from models.user import User
from api.v1.views import app_views


@app_views.route('/auth_session/login', methods=['POST'], strict_slashes=False)
def login() -> Tuple[str, int]:
    '''POST /api/v1/auth_session/login
    Return:
      - JSON representation of a User object.
    '''
    result_nt_found = {"error": "no user found for this email"}
    user_email = request.form.get('email')
    if user_email is None or len(user_email.strip()) == 0:
        return jsonify({"error": "email missing"}), 400
    password = request.form.get('password')
    if password is None or len(password.strip()) == 0:
        return jsonify({"error": "password missing"}), 400
    try:
        users = User.search({'email': user_email})
    except Exception:
        return jsonify(result_nt_found), 404
    if len(users) <= 0:
        return jsonify(result_nt_found), 404
    if users[0].is_valid_password(password):
        from api.v1.app import auth
        sessiond_id = auth.create_session(getattr(users[0], 'id'))
        res = jsonify(users[0].to_json())
        res.set_cookie(os.getenv("SESSION_NAME"), sessiond_id)
        return res
    return jsonify({"error": "wrong password"}), 401

@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False)
def logout() -> Tuple[str, int]:
    '''DELETE /api/v1/auth_session/logout
    Return:
      - An empty JSON object.
    '''
    from api.v1.app import auth
    is_destroyed = auth.destroy_session(request)
    if not is_destroyed:
        abort(404)
    return jsonify({})
