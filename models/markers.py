#!/usr/bin/python3
"""
Module for Markers
"""
from models.base_model import Base, BaseModel
from sqlalchemy import Column, Integer, String, Float, ForeignKey


class Marker(BaseModel, Base):
    """
    Class for markers on Google Map
    """

    __tablename__ = "markers"

    latitude = Column(Float, nullable=False, default=0)
    longitude = Column(Float, nullable=False, default=0)
    user_id = Column(String(60), ForeignKey("users.id"), nullable=True)
    upvote = Column(Integer, nullable=False, default=0)
    city = Column(String(60), nullable=True, default="SF")
    country = Column(String(60), nullable=True, default="USA")
    name = Column(String(60), nullable=False, default="Trash Can")
