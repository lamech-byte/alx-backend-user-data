#!/usr/bin/env python3
"""
Session Exp Auth Module

This module defines the SessionExpAuth class, which is responsible for handling
session-based authentication with session expiration for the API.
"""

from api.v1.auth.session_auth import SessionAuth
from datetime import datetime, timedelta
import os


class SessionExpAuth(SessionAuth):
    """
    SessionExpAuth Class

    This class inherits from SessionAuth and adds the functionality
    of session expiration
    to the session-based authentication mechanism.
    """

    def __init__(self):
        """
        Initialize SessionExpAuth instance.

        This constructor overloads the parent constructor and also initializes
        the session duration based on the SESSION_DURATION environment
        variable.
        If the environment variable is missing or invalid, a default
        of 0 is used.

        Args:
            None

        Returns:
            None
        """
        super().__init__()
        session_duration = os.environ.get("SESSION_DURATION")
        try:
            self.session_duration = int(session_duration)
        except (ValueError, TypeError):
            self.session_duration = 0

    def create_session(self, user_id=None):
        """
        Create a session for the given user.

        This method overloads the parent method and adds the session
        creation time
        to the user_id_by_session_id dictionary.

        Args:
            user_id (str): The ID of the user for whom the session
            is being created.

        Returns:
            str: The created session ID.
        """
        session_id = super().create_session(user_id)
        if session_id:
            self.user_id_by_session_id[session_id] = {
                "user_id": user_id,
                "created_at": datetime.now()
            }
        return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieve the user ID associated with a session ID.

        This method checks the session duration and expiration time
        to determine whether the session is valid or expired.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            str or None: The associated user ID or None if the
            session is invalid.
        """
        if not session_id or session_id not in self.user_id_by_session_id:
            return None

        session_data = self.user_id_by_session_id[session_id]
        if self.session_duration <= 0:
            return session_data["user_id"]

        created_at = session_data.get("created_at")
        if not created_at:
            return None

        expiration_time = created_at + timedelta(seconds=self.session_duration)
        if datetime.now() > expiration_time:
            return None

        return session_data["user_id"]
