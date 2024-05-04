#!/usr/bin/python3
"""Defines an Amenity class"""
from models.base_model import BaseModel


class Amenity(BaseModel):
    """Represents an amenity"""

    name = ""

    def __init__(self, *args, **kwargs):
        """Initializes the amenity"""
        super().__init__(self, *args, **kwargs)
