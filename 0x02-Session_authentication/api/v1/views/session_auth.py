#!/usr/bin/env python3
"""
Session Auth View

This module defines the view for session-based authentication.
It provides routes for handling login and session management.

Routes:
    - POST /auth_session/login: Handles session-based authentication login.
"""

from flask import Flask, request, jsonify, make_response
from api.v1.views import app_views
from models.user import User
from api.v1.app import auth


@app_views.route(
  '/auth_session/login', methods=['POST'], strict_slashes=False
)
def session_login():
    """
    Handles session-based authentication login.

    Retrieves email and password from the request form.
    Checks if email and password are provided and not empty.
    Retrieves the User instance based on the provided email.
    Validates the password of the user.
    If successful, creates a session ID for the user.
    Returns the User's JSON representation and sets the session cookie.

    Returns:
        Response: JSON representation of the User and session cookie.
    """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400

    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search(email)
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user.is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = auth.create_session(user.id)
    response_data = user.to_json()
    response = make_response(jsonify(response_data), 200)
    response.set_cookie(auth.SESSION_NAME, session_id)

    return response
