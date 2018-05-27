#!/usr/bin/python3
"""
Module for Base Model
"""
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
