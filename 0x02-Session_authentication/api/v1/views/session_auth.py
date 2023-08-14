#!/usr/bin/env python3
"""
Session Authentication module
"""

from flask import request, jsonify, current_app
from api.v1.auth.session_auth import SessionAuth
from models.user import User
from api.v1.views import session_auth


@session_auth.route('/login', methods=['POST'], strict_slashes=False)
def login():
    """ Handles the /api/v1/auth_session/login route """
    email = request.form.get('email')
    password = request.form.get('password')

    if not email:
        return jsonify({"error": "email missing"}), 400
    if not password:
        return jsonify({"error": "password missing"}), 400

    user = User.search({'email': email})
    if not user:
        return jsonify({"error": "no user found for this email"}), 404

    if not user[0].is_valid_password(password):
        return jsonify({"error": "wrong password"}), 401

    auth = current_app.auth
    session_id = auth.create_session(user[0].id)

    response_data = user[0].to_json()
    response_data["email"] = email
    response = jsonify(response_data)
    response.set_cookie(current_app.config["SESSION_NAME"], session_id)

    return response
