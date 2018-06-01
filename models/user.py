#!/usr/bin/python3
"""
Module that creates a User class
"""
from flask_login import UserMixin
from models.base_model import Base, BaseModel
from sqlalchemy import Column, String, DateTime, Text, Boolean
from sqlalchemy.orm import relationship
from werkzeug import generate_password_hash, check_password_hash


class User(BaseModel, Base, UserMixin):
    """
    Class for Users
    """
    __tablename__ = "users"

    name = Column(String(60), nullable=True)
    tokens = Column(Text)
    email = Column(String(60), nullable=False, unique=True)
    active = Column(Boolean, default=False)
    markers = relationship('Marker', backref='user')
