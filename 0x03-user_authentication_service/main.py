#!/usr/bin/env python3
"""
Main file
"""
from auth import Auth

auth = Auth()
email = 'test@test.com'
password = 'Hello Holberton'

hashed_password = auth._hash_password(password)
print(hashed_password)
