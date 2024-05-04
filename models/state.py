#!/usr/bin/python3
"""Defines a State class"""
from models.base_model import BaseModel


class State(BaseModel):
    """Represents a state"""

    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the state"""
        super().__init__(self, *args, **kwargs)
