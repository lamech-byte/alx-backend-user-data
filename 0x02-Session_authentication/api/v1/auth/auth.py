#!/usr/bin/env python3
"""
Auth module
"""

import os
from flask import request

class Auth:
    """
    Auth class for managing authentication and authorization
    """

    def __init__(self):
        """
        Constructor
        """
        pass

    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determines if a route requires authentication

        Args:
            path (str): The path of the route.
            excluded_paths (list): List of paths to exclude from authentication.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or not isinstance(
            excluded_paths, list
        ):
            return True

        if path[-1] != '/':
            path += '/'

        if path in excluded_paths:
            return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Extracts the value of the Authorization header from a request.

        Args:
            request: The request object.

        Returns:
            str: The value of the Authorization header, or None if not found.
        """
        if request is None or not isinstance(request, Request):
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """
        Retrieves the current User based on the Authorization header.

        Args:
            request: The request object.

        Returns:
            User: The User instance if the Authorization header is valid,
                  None otherwise.
        """
        return None

    def session_cookie(self, request=None) -> str:
        """
        Returns a cookie value from a request.

        Args:
            request: The request object.

        Returns:
            str: The value of the cookie named SESSION_NAME, or None if not found.
        """
        if request is None:
            return None

        session_name = os.environ.get('SESSION_NAME', '_my_session_id')
        return request.cookies.get(session_name)
