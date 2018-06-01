#!/usr/bin/python3
"""
"""
from models.base_model import BaseModel
from models.engine.db_storage import DBStorage
from models.markers import Marker
from models.user import User
from models.auth import Auth

classes = {"User": User, "Marker": Marker, "BaseModel": BaseModel, "Auth": Auth}
storage = DBStorage()
storage.reload()
