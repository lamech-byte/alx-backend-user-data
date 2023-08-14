#!/usr/bin/env python3
""" Auth module
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth class for managing API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """
        Determine if authentication is required for a given path.

        Args:
            path (str): The path to be checked.
            excluded_paths (list of str): List of paths to be excluded.

        Returns:
            bool: True if authentication is required, False otherwise.
        """
        if path is None or excluded_paths is None or \
           not isinstance(excluded_paths, list):
            return True

        for excluded_path in excluded_paths:
            if excluded_path.endswith('*') and \
               path.startswith(excluded_path[:-1]):
                return False
            elif path == excluded_path:
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """
        Get the authorization header from the request.

        Returns:
            The value of the header 'Authorization' if present,
            None otherwise.
        """
        if request is None:
            return None

        return request.headers.get('Authorization')

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user from the request
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
