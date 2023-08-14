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
from api.v1.auth.session_auth import SessionAuth

sa = SessionAuth()


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

    user = User.search({"email": email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404
    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    session_id = sa.create_session(user[0].id)
    response_data = user[0].to_json()
    response_data["__class__"] = "User"
    response = jsonify(response_data)
    response.set_cookie(app.config['SESSION_NAME'], session_id)

    return response, 200


@app_views.route(
    '/auth_session/logout', methods=['DELETE'], strict_slashes=False
)
def session_logout():
    """
    Handles session-based authentication logout.

    Deletes the user session (session ID) if available in the request's cookie.
    Returns an empty JSON dictionary with the status code 200 if successful.

    Returns:
        Response: Empty JSON dictionary with status code 200
        if session is destroyed.
    """
    if not sa.destroy_session(request):
        return jsonify({}), 404

    response = jsonify({})
    return response, 200
