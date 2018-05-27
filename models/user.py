#!/usr/bin/python3
"""
Module that creates a User class
"""
from models.base_model import Base
from sqlalchemy import Column, String, DateTime


class User(BaseModel, Base):
    """
    Class for Users
    """
    __tablename__ = "users"


    markers = relationship('Marker', backref='user')
