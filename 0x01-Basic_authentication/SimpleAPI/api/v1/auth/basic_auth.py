#!/usr/bin/env python3
""" BasicAuth module
"""
from api.v1.auth.auth import Auth

class BasicAuth(Auth):
    """ BasicAuth class for managing basic authentication
    """
    def extract_base64_authorization_header(self, authorization_header: str) -> str:
        """
        Extract the Base64 part of the Authorization header for Basic Authentication.

        Args:
            authorization_header: The Authorization header string.

        Returns:
            The Base64 part of the Authorization header if valid, otherwise None.
        """
        if authorization_header is None or not isinstance(authorization_header, str):
            return None
        
        if not authorization_header.startswith('Basic '):
            return None
        
        return authorization_header.split(' ', 1)[1]
    pass
