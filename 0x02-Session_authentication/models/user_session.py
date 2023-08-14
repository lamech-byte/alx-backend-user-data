#!/usr/bin/env python3
"""
UserSession Module

This module defines the UserSession class, which represents user session information stored in the database.
"""

from models.base import Base
from sqlalchemy import Column, String

class UserSession(Base):
    """
    UserSession class

    This class defines the UserSession model with attributes user_id and session_id.
    """
    __tablename__ = 'user_sessions'
    user_id = Column(String(60), nullable=False)
    session_id = Column(String(60), nullable=False)
    
    def __init__(self, *args: list, **kwargs: dict):
        """
        Initializes UserSession instance.

        Args:
            *args (list): List of arguments.
            **kwargs (dict): Keyword arguments.
        """
        super().__init__(*args, **kwargs)
