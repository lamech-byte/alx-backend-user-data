#!/usr/bin/env python3
"""
SessionExpAuth module
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
from api.v1.auth.auth import Auth
import uuid
from models.user import User
from typing import TypeVar
from flask import request
import os


class SessionAuth(Auth):
    """
    SessionAuth class for managing session-based authentication.
    """
    user_id_by_session_id = {}

    def create_session(self, user_id: str = None) -> str:
        """
        Creates a Session ID for a user ID.

        Args:
            user_id (str): The user ID.

        Returns:
            str: The newly created Session ID.
        """
        if user_id is None:
            return None

        session_id = str(uuid.uuid4())
        self.user_id_by_session_id[session_id] = user_id
        return session_id

    def user_id_for_session_id(
        self, session_id: str = None
    ) -> TypeVar('User'):
        """
        Retrieves a user ID based on a Session ID.

        Args:
            session_id (str): The Session ID.

        Returns:
            str: The user ID if found, None otherwise.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Returns a User instance based on a cookie value.

        Args:
            request (Request): The Flask request object.

        Returns:
            User: The User instance if a valid session exists, None otherwise.
        """
        session_cookie = self.session_cookie(request)
        if session_cookie:
            user_id = self.user_id_for_session_id(session_cookie)
            if user_id:
                user = User.get(user_id)
                return user

        return None
