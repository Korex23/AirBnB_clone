#!/usr/bin/python3
"""Defines a FileStorage class"""
import os
import json
from models.city import City
from models.user import User
from models.place import Place
from models.state import State
from models.review import Review
from models.amenity import Amenity
from models.base_model import BaseModel


class FileStorage:
    """Represents a data storage class"""

    __file_path = "file.json"
    __objects = {}

    MODELS = {
        "City": City,
        "User": User,
        "Place": Place,
        "State": State,
        "Review": Review,
        "Amenity": Amenity,
        "BaseModel": BaseModel,
        }

    def all(self):
        """Returns the dictionary __objects"""
        return type(self).__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        key = f"{type(obj).__name__}.{obj.id}"
        type(self).__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        objects_dict = {}
        for key, value in type(self).__objects.items():
            objects_dict[key] = value.to_dict()
        with open(type(self).__file_path, "w", encoding="utf-8") as json_file:
            json.dump(objects_dict, json_file)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        if os.path.isfile(type(self).__file_path):
            with open(type(self).__file_path, encoding="utf-8") as json_file:
                objects_dict = json.load(json_file)

            for key, value in objects_dict.items():
                _class_ = value["__class__"]
                type(self).__objects[key] = type(self).MODELS[_class_](**value)
