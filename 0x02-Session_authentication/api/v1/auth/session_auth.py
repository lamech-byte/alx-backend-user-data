#!/usr/bin/env python3
"""
SessionAuth module
"""

import uuid

from api.v1.auth.auth import Auth


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

        return self.user_id_by_session_id.get(session_id)

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

        return self.user_id_by_session_id.get(session_id)

    def current_user(self, request=None):
        """
        Returns a User instance based on a session cookie value.

        Args:
            request: The request object.

        Returns:
            User instance or None.
        """
        if request is None:
            return None

        session_cookie = self.session_cookie(request)
        if session_cookie is None:
            return None

        user_id = self.user_id_for_session_id(session_cookie)
        if user_id is None:
            return None

        user = User.get(user_id)
        return user
