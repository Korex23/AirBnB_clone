#!/usr/bin/pyhton3
"""Defines a BaseModel class"""
import uuid
import models
from datetime import datetime


class BaseModel:
    """Represent the base class"""

    def __init__(self, *args, **kwargs):
        """Initializes the an instance of BaseModel"""
        if kwargs:
            date_format = "%Y-%m-%dT%H:%M:%S.%f"
            for key, value in kwargs.items():
                if key != "__class__":
                    try:
                        value = datetime.strptime(str(value), date_format)
                    except ValueError:
                        pass
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = self.updated_at = datetime.now()
            models.storage.new(self)

    def save(self):
        """Updates the updated_at attribute with the current time"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """Returns a dictionary of the instance"""
        attributes = self.__dict__.copy()
        attributes["__class__"] = type(self).__name__

        for key, value in attributes.items():
            if isinstance(value, datetime):
                attributes[key] = value.isoformat()

        return attributes

    def __str__(self):
        """Returns the string representation of the instance"""
        return f"[{type(self).__name__}] ({self.id}) {self.__dict__}"
