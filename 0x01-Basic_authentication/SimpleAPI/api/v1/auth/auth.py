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
        Check if authentication is required for a path.

        Returns:
            True if path is None
            True if excluded_paths is None or empty
            False if path is in excluded_paths
            True otherwise
        """
        if path is None or not excluded_paths:
            return True

        for excluded_path in excluded_paths:
            if path == excluded_path or path.startswith(excluded_path):
                return False

        return True

    def authorization_header(self, request=None) -> str:
        """ Get the authorization header from the request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user from the request
        """
        return None
