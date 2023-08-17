#!/usr/bin/env python3
"""auth module
"""

from db import DB
from sqlalchemy.orm.exc import NoResultFound
import bcrypt
from typing import Union
from user import User
import uuid


class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self) -> None:
        """Initialize a new Auth instance.
        """
        self._db = DB()

    def _hash_password(self, password: str) -> bytes:
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

    def _generate_uuid(self) -> str:
        """
        Generate a new UUID string.

        Returns:
            str: The string representation of a new UUID.
        """
        new_uuid = uuid.uuid4()
        return str(new_uuid)

    def create_session(self, email: str) -> Union[str, None]:
        """
        Create a new session for a user.

        Args:
            email (str): The user's email.

        Returns:
            Union[str, None]: The session ID if the user exists, else None.
        """
        try:
            user = self._db.find_user_by(email=email)
            session_id = self._generate_uuid()
            user.session_id = session_id
            return session_id
        except NoResultFound:
            return None

    def get_user_from_session_id(self, session_id: str) -> Optional[User]:
        """
        Get the User corresponding to a session ID.

        Args:
            session_id (str): The session ID to look up.

        Returns:
            Optional[User]: The corresponding User or None if not found.
        """
        if session_id is None:
            return None

        try:
            user = self._db.find_user_by(session_id=session_id)
            return user
        except NoResultFound:
            return None

    def destroy_session(self, user_id: int) -> None:
        """
        Destroy a user's session by setting their session ID to None.

        Args:
            user_id (int): The user's ID.

        Returns:
            None
        """
        try:
            user = self._db.find_user_by(id=user_id)
            user.session_id = None
        except NoResultFound:
            pass


if __name__ == "__main__":
    auth = Auth()
    email = 'bob@bob.com'
    password = 'MyPwdOfBob'
    auth.register_user(email, password)

    print(auth.valid_login(email, password))
    print(auth.valid_login(email, "WrongPwd"))
    print(auth.valid_login("unknown@email", password))
