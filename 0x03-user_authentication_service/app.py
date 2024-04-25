#!/usr/bin/env python3

'''A Baic Flask app with user authentication features.
'''
from flask import Flask, jsonify, request, abort, redirect

from auth import Auth


app = Flask(__name__)
AUTH = Auth()


@app.route("/", methods=["GET"], strict_slashes=False)
def index() -> str:
    '''GET /
    Return:
        - The home page's payload.
    '''
    return jsonify({"message": "Bienvenue"})


@app.route("/users", methods=["POST"], strict_slashes=False)
def users() -> str:
    '''POST /users
    Return:
        - The account creation payload.
    '''
    U_email, U_password = request.form.get(
        "email"), request.form.get("password")
    try:
        AUTH.register_user(U_email, U_password)
        return jsonify({"email": U_email, "message": "user created"})
    except ValueError:
        return jsonify({"message": "email already registered"}), 400


@app.route("/sessions", methods=["POST"], strict_slashes=False)
def login() -> str:
    '''POST LOGIN /sessions
    Return:
        - The account login.
    '''
    U_email, U_password = request.form.get(
        "email"), request.form.get("password")
    if not AUTH.valid_login(U_email, U_password):
        abort(401)
    session_id = AUTH.create_session(U_email)
    response = jsonify({"email": U_email, "message": "logged in"})
    response.set_cookie("session_id", session_id)
    return response


@app.route("/sessions", methods=["DELETE"], strict_slashes=False)
def logout() -> str:
    '''DELETE user /sessions
    Return:
        - Redirects user to home route.
    '''
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    AUTH.destroy_session(user.id)
    return redirect("/")


@app.route("/profile", methods=["GET"], strict_slashes=False)
def profile() -> str:
    '''GET /profile
    Return:
        - User's profile information.
    '''
    session_id = request.cookies.get("session_id")
    user = AUTH.get_user_from_session_id(session_id)
    if user is None:
        abort(403)
    return jsonify({"email": user.email})


@app.route("/reset_password", methods=["POST"], strict_slashes=False)
def get_reset_password_token() -> str:
    '''POST /reset_password
    Return:
        - User's password reset payload.
    '''
    email = request.form.get("email")
    token_reset = None
    try:
        token_reset = AUTH.get_reset_password_token(email)
    except ValueError:
        token_reset = None
    if token_reset is None:
        abort(403)
    return jsonify({"email": email, "reset_token": token_reset})


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
