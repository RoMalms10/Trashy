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

    first_name = Column(String(60), nullable=True)
    last_name = Column(String(60), nullable=True)
    username = Column(String(60), nullable=False)
    password = Column(String(60), nullable=False)

    markers = relationship('Marker', backref='user')
