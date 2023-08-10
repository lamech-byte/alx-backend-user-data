#!/usr/bin/env python3
"""
SessionExpAuth module
"""

from datetime import datetime, timedelta
from api.v1.auth.session_auth import SessionAuth


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth class for managing session-based authentication with expiration
    """

    def __init__(self):
        """
        Constructor
        """
        super().__init__()
        session_duration = os.environ.get('SESSION_DURATION')
        try:
            self.session_duration = int(session_duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Creates a Session ID with expiration

        Args:
            user_id (str): The user ID.

        Returns:
            str: The created Session ID.
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
        Retrieves the User ID for a given Session ID, with session expiration.

        Args:
            session_id (str): The Session ID.

        Returns:
            str: The User ID associated with the Session ID if valid and not expired, None otherwise.
        """
        if session_id is None:
            return None

        session_dict = self.user_id_by_session_id.get(session_id)
        if session_dict is None:
            return None

        user_id = session_dict.get('user_id')
        if self.session_duration <= 0:
            return user_id

        created_at = session_dict.get('created_at')
        if created_at is None:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return user_id
