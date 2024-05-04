#!/usr/bin/python3
"""Defines a User class"""
from models.base_model import BaseModel


class User(BaseModel):
    """Represents a user"""

    email = ""
    password = ""
    first_name = ""
    last_name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the user"""
        super().__init__(self, *args, **kwargs)
