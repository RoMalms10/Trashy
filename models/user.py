#!/usr/bin/python3
"""
Module that creates a User class
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, DateTime
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """
    Class for Users
    """
    __tablename__ = "users"


    markers = relationship('Marker', backref='user')
