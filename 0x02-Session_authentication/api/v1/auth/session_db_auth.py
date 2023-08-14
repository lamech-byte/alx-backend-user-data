#!/usr/bin/env python3
"""
Session DB Auth Module

This module defines the SessionDBAuth class, which handles session-based authentication using database storage.
"""

from api.v1.auth.session_exp_auth import SessionExpAuth
from models.user_session import UserSession
from datetime import datetime, timedelta
from flask import request

class SessionDBAuth(SessionExpAuth):
    """
    Session DB Auth class

    This class extends SessionExpAuth and adds database storage for user sessions.
    """
    def create_session(self, user_id=None):
        """
        Creates a new session in the database.

        Args:
            user_id (str): The ID of the user.

        Returns:
            str: The created session ID.
        """
        if user_id is None:
            return None

        session_id = super().create_session(user_id)
        if session_id:
            user_session = UserSession(user_id=user_id, session_id=session_id)
            user_session.save()
            return session_id

    def user_id_for_session_id(self, session_id=None):
        """
        Retrieves user_id from UserSession in the database.

        Args:
            session_id (str): The session ID.

        Returns:
            str: The ID of the associated user.
        """
        if session_id is None:
            return None

        user_id = super().user_id_for_session_id(session_id)
        if user_id:
            user_session = UserSession.search({"session_id": session_id})
            if user_session and len(user_session) > 0:
                return user_session[0].user_id

    def destroy_session(self, request=None):
        """
        Destroys a session from the database.

        Args:
            request: The HTTP request.

        Returns:
            bool: True if session was successfully destroyed, False otherwise.
        """
        if request is None:
            return False

        session_id = self.session_cookie(request)
        if not session_id:
            return False

        user_id = self.user_id_for_session_id(session_id)
        if not user_id:
            return False

        user_session = UserSession.search({"session_id": session_id})
        if user_session and len(user_session) > 0:
            user_session[0].remove()
            return True
