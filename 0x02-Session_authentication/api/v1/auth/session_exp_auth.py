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


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for managing session-based authentication
    with session expiration.
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        session_duration_str = os.environ.get('SESSION_DURATION', '0')
        try:
            self.session_duration = int(session_duration_str)
        except ValueError:
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID for a user ID.

        Args:
            user_id (str): The user ID.

        Returns:
            str: The newly created Session ID.
        """
        session_id = super().create_session(user_id)
        if session_id:
            if self.user_id_by_session_id is None:
                self.user_id_by_session_id = {}
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
            return session_id
        return None

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves a user ID based on a Session ID.

        Args:
            session_id (str): The Session ID.

        Returns:
            str: The user ID if found and session is not expired,
            None otherwise.
        """
        if session_id is None or self.user_id_by_session_id is None:
            return None

        session_data = self.user_id_by_session_id.get(session_id)
        if session_data:
            created_at = session_data.get('created_at')
            if created_at:
                current_time = datetime.now()
                expiration_time = created_at + timedelta(
                    seconds=self.session_duration
                )
                if current_time <= expiration_time:
                    return session_data.get('user_id')

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
