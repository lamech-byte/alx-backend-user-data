#!/usr/bin/env python3
"""
SessionAuth module
"""

import uuid
from api.v1.auth.auth import Auth
from flask import Blueprint, Flask, request, jsonify
from api.v1.views import app_views
from models.user import User


app_views = Blueprint('session_auth', __name__, url_prefix='/api/v1/auth_session')


class SessionAuth(Auth):
    """
    SessionAuth class for managing session-based authentication
    """

    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user_id.

        Args:
            user_id (str): The user ID.

        Returns:
            str: The created Session ID or None.
        """
        if user_id is None or not isinstance(user_id, str):
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(self, session_id: str = None) -> str:
        """
        Returns a User ID based on a Session ID.

        Args:
            session_id (str): The Session ID.

        Returns:
            str: The User ID associated with the Session ID, or None.
        """
        if session_id is None or not isinstance(session_id, str):
            return None

    @app_views.route(
        '/auth_session/login', methods=['POST'], strict_slashes=False
    )
    def session_login():
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

        session_id = auth.create_session(user[0].id)
        user_json = user[0].to_json()
        response = jsonify(user_json)
        response.set_cookie(os.environ.get(
            'SESSION_NAME', '_my_session_id'
        ), session_id)
        return response

        return self.user_id_by_session_id.get(session_id)
