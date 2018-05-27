#!/usr/bin/python3
"""
Creates the DBStorage class
"""
from models.user import Base
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage(Base):
    """
    Class that handles the set up and storage of information in a database
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes an instance of DBStorage
        """
        self.__engine = create_engine(mysql+mysqldb://{}:{}@{}/{}'.format(
            os.environ.get('TRASHY_MYSQL_USER'),
            os.environ.get('TRASHY_MYSQL_PWD'),
            os.environ.get('TRASHY_MYSQL_HOST'),
            os.environ.get('TRASHY_MYSQL_DB')))

    def all(self, cls=None):
        """
        Grabs all markers if class is not User
        """

    def reload(self):
        """
        Binds the current session to the instance
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
                sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))
