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


if __name__ == "__main__":
    app.run(host="0.0.0.0", port="5000")
