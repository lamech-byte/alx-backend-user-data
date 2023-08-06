#!/usr/bin/env python3
"""
Module to securely hash passwords using bcrypt.
"""

import bcrypt


def hash_password(password: str) -> bytes:
    """
    Hashes and salts a password using bcrypt.

    Args:
        password (str): The password to be hashed.

    Returns:
        bytes: The salted and hashed password.
    """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


if __name__ == "__main__":
    pass
