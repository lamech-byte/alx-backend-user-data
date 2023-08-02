#!/usr/bin/env python3
"""
encrypt_password.py - Module for hashing and validating passwords using bcrypt.
"""

import bcrypt


def hash_password(password):
    """ Hash and salt a password using bcrypt """
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
    return hashed_password


def is_valid(hashed_password, password):
    """ Validate that the provided password matches the hashed password """
    return bcrypt.checkpw(password.encode('utf-8'), hashed_password)


if __name__ == "__main__":
    password = "MyAmazingPassw0rd"
    encrypted_password = hash_password(password)
    print(encrypted_password)
    print(is_valid(encrypted_password, password))
