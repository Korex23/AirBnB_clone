#!/usr/bin/python3
"""Configures the models package."""
from .city import City
from .user import User
from .place import Place
from .state import State
from .review import Review
from .amenity import Amenity
from .base_model import BaseModel
from .engine.file_storage import FileStorage


storage = FileStorage()
storage.reload()

MODELS = {
        "City": City,
        "User": User,
        "Place": Place,
        "State": State,
        "Review": Review,
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        }
