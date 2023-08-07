#!/usr/bin/env python3
""" Auth module
"""
from typing import List, TypeVar
from flask import request


class Auth:
    """ Auth class for managing API authentication
    """
    def require_auth(self, path: str, excluded_paths: List[str]) -> bool:
        """ Check if authentication is required for a path
        """
        return False

    def authorization_header(self, request=None) -> str:
        """ Get the authorization header from the request
        """
        return None

    def current_user(self, request=None) -> TypeVar('User'):
        """ Get the current user from the request
        """
        return None
