#!/usr/bin/env python3
""" BasicAuth module
"""

import base64
from api.v1.auth.auth import Auth


class BasicAuth(Auth):
    """ BasicAuth class for managing basic authentication
    """

    def extract_base64_authorization_header(
        self, authorization_header: str
    ) -> str:
        """
        Extract the Base64 part of the Authorization header for
        Basic Authentication.

        Args:
            authorization_header (str): The Authorization header string.

        Returns:
            str: The Base64 part of the Authorization header if valid,
            otherwise None.
        """
        if authorization_header is None or not isinstance(
            authorization_header, str
        ):
            return None

        if not authorization_header.startswith('Basic '):
            return None

        return authorization_header.split(' ', 1)[1]

    def decode_base64_authorization_header(
        self, base64_authorization_header: str
    ) -> str:
        """
        Decode a Base64 encoded authorization header.

        Args:
            base64_authorization_header (str): The Base64 encoded
            authorization header.

        Returns:
            str: The decoded value as a UTF-8 string if valid,
            otherwise None.
        """
        if base64_authorization_header is None or not isinstance(
            base64_authorization_header, str
        ):
            return None

        try:
            decoded_bytes = base64.b64decode(base64_authorization_header)
            decoded_string = decoded_bytes.decode('utf-8')
            return decoded_string
        except base64.binascii.Error:
            return None

    def extract_user_credentials(
        self, decoded_base64_authorization_header: str
    ) -> (str, str):
        """
        Extract user email and password from a decoded Base64 authorization
        header.

        Args:
            decoded_base64_authorization_header: The decoded Base64
            authorization header.

        Returns:
            A tuple containing the user email and password if valid,
            otherwise (None, None).
        """
        if decoded_base64_authorization_header is None or not isinstance(
            decoded_base64_authorization_header, str
        ):
            return None, None

        if ':' not in decoded_base64_authorization_header:
            return None, None

        user_email, user_password = decoded_base64_authorization_header.split(
            ':', 1
        )
        return user_email, user_password
