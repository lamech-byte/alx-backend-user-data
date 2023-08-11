#!/usr/bin/env python3
"""
SessionExpAuth module
"""

from api.v1.auth.session_auth import SessionAuth
from typing import List, TypeVar
from datetime import datetime, timedelta


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for managing Session authentication with expiration
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        self.session_duration = int(os.environ.get('SESSION_DURATION', 0))

    def create_session(self, user_id=None):
        """
        Creates a new session for a user.

        Args:
            user_id (str): The user ID.

        Returns:
            str: The new session ID.
        """
        session_id = super().create_session(user_id)
        if session_id is None:
            return None

        session_dict = {
            'user_id': user_id,
            'created_at': datetime.now()
        }
        self.user_id_by_session_id[session_id] = session_dict
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves a user ID based on a session ID.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The associated user ID, or None if not found or expired.
        """
        if session_id is None or session_id not in self.user_id_by_session_id:
            return None

        session_dict = self.user_id_by_session_id[session_id]
        if self.session_duration > 0:
            created_at = session_dict.get('created_at')
            if created_at is None:
                return None

            expiration_time = created_at + timedelta(
                seconds=self.session_duration
            )
            if expiration_time < datetime.now():
                return None

        return session_dict.get('user_id')
