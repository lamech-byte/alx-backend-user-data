#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, exc
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import InvalidRequestError
from sqlalchemy.orm.exc import NoResultFound
from user import Base, User  # Import the User model from user.py


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=False)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session

    def add_user(self, email: str, hashed_password: str) -> User:
        """
        Add a new user to the database.

        Args:
            email (str): The user's email.
            hashed_password (str): The user's hashed password.

        Returns:
            User: The created User object.
        """
        new_user = User(email=email, hashed_password=hashed_password)
        self._session.add(new_user)
        self._session.commit()
        return new_user

    def find_user_by(self, **kwargs) -> User:
        """
        Find a user by specified filters.

        Args:
            **kwargs: Arbitrary keyword arguments used for filtering.

        Returns:
            User: The found User object.

        Raises:
            NoResultFound: If no results are found.
            InvalidRequestError: If wrong query arguments are passed.
        """
        try:
            user = self._session.query(User).filter_by(**kwargs).one()
            return user
        except NoResultFound:
            raise NoResultFound("No user found")
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query arguments")

    def update_user(self, user_id: int, **kwargs) -> None:
        """
        Update a user's attributes.

        Args:
            user_id (int): The ID of the user to update.
            **kwargs: Arbitrary keyword arguments representing user attributes.

        Returns:
            None

        Raises:
            NoResultFound: If the user is not found.
            ValueError: If an invalid attribute is passed.
        """
        try:
            user = self.find_user_by(id=user_id)
            for attr, value in kwargs.items():
                if hasattr(user, attr):
                    setattr(user, attr, value)
                else:
                    raise ValueError(f"Invalid attribute: {attr}")
            self._session.commit()
        except NoResultFound:
            raise NoResultFound("User not found")


if __name__ == "__main__":
    my_db = DB()

    user_1 = my_db.add_user("test@test.com", "PwdHashed")
    print(user_1.id)

    find_user = my_db.find_user_by(email="test@test.com")
    print(find_user.id)

    try:
        find_user = my_db.find_user_by(email="test2@test.com")
        print(find_user.id)
    except NoResultFound:
        print("Not found")

    try:
        find_user = my_db.find_user_by(no_email="test@test.com")
        print(find_user.id)
    except InvalidRequestError:
        print("Invalid")
