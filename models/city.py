#!/usr/bin/python3
"""Defines a City class"""
from models.base_model import BaseModel


class City(BaseModel):
    """Represents a city"""

    state_id = ""
    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the city"""
        super().__init__(self, *args, **kwargs)
