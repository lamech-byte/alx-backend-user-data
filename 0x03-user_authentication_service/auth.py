#!/usr/bin/env python3
"""auth module
"""

from db import DB
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from typing import Union
from user import User


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialize a new Auth instance.
        """
        self._db = DB()

    def _hash_password(password: str) -> bytes:
        """
        Hash a password using bcrypt.

        Args:
            password (str): The password string to hash.

        Returns:
            bytes: The hashed password bytes.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password

    def register_user(self, email: str, password: str) -> Union[None, User]:
        """
        Register a new user.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            Union[None, User]: The created User object.

        Raises:
            ValueError: If a user with the same email already exists.
        """
        try:
            existing_user = self._db.find_user_by(email=email)
            raise ValueError(f"User {email} already exists")
        except NoResultFound:
            hashed_password = self._hash_password(password)
            user = self._db.add_user(email, hashed_password)
            return user

    def valid_login(self, email: str, password: str) -> bool:
        """
        Validate a user's login credentials.

        Args:
            email (str): The user's email.
            password (str): The user's password.

        Returns:
            bool: True if the login is valid, False otherwise.
        """
        try:
            user = self._db.find_user_by(email=email)
            hashed_password = user.hashed_password
            return bcrypt.checkpw(
                password.encode('utf-8'), hashed_password
            )
        except NoResultFound:
            return False


if __name__ == "__main__":
    auth = Auth()
    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    auth.register_user(email, password)

    print(auth.valid_login(email, password))
    print(auth.valid_login(email, "WrongPwd"))
    print(auth.valid_login("unknown@email", password))
    print(_hash_password("Hello Holberton"))
