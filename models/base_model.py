#!/usr/bin/python3
"""
Module for Base Model
"""
import models
import uuid
from datetime import datetime
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base



Base = declarative_base()

class BaseModel():
    """
    Base Model from which other classes inherit from
    """
    id = Column(String(60), nullable=False, primary_key=True)
    created_at = Column(DateTime, default=datetime.utcnow(),
                        nullable=False)
    updated_at = Column(DateTime, default=datetime.utcnow(),
                        nullable=False)

    def __init__(self, *args, **kwargs):
        """
        Creates an instance of an object
        """
        if kwargs:
            self.__set_attributes(kwargs)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()

    def __str__(self):
        """
        Returns string type representation of object instance
        """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def __repr__(self):
        """
        Returns unofficial string type representation of object instance
        """
        return ("[{}] ({}) {}".format(self.__class__.__name__,
                                      self.id, self.__dict__))

    def __set_attributes(self, attr_dict):
        """
        Private method for setting attributes when instantiating an object
            using kwargs
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        if 'id' not in attr_dict:
            attr_dict['id'] = str(uuid.uuid4())
        if 'created_at' not in attr_dict:
            attr_dict['created_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['created_at'], datetime):
            attr_dict['created_at'] = datetime.strptime(
                attr_dict['created_at'], time_format)
        if 'updated_at' not in attr_dict:
            attr_dict['updated_at'] = datetime.utcnow()
        elif not isinstance(attr_dict['updated_at'], datetime):
            attr_dict['updated_at'] = datetime.strptime(
                attr_dict['updated_at'], time_format)
        for key, value in attr_dict.items():
            setattr(self, key, value)

    def save(self):
        """
        Save the current object to the database
        """
        self.updated_at = datetime.now()
        models.storage.new(self)
        models.storage.save()

    def delete(self):
        """
        Deletes the current object from the database
        """
        models.storage.delete(self)

    def to_dict(self):
        '''
        Return dictionary representation of self object to be used when
            converting to JSON format.
        '''
        cp_dct = dict(self.__dict__)
        cp_dct.pop('_sa_instance_state', None)
        cp_dct['__class__'] = self.__class__.__name__
        cp_dct['updated_at'] = self.updated_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
        cp_dct['created_at'] = self.created_at.strftime("%Y-%m-%dT%H:%M:%S.%f")
