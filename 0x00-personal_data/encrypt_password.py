#!/usr/bin/env python3
"""
encrypt_password.py - Module for hashing passwords using bcrypt.
"""

import bcrypt


def hash_password(password):
    """ Hash and salt a password using bcrypt """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    print(hash_password(password))
    print(hash_password(password))
