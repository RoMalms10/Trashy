#!/usr/bin/python3
"""
Creates the DBStorage class
"""
from models.user import Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session


class DBStorage():
    """
    Class that handles the set up and storage of information in a database
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes an instance of DBStorage
        """
        print(getenv('TRASHY_MYSQL_USER'))
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('TRASHY_MYSQL_USER'),
            getenv('TRASHY_MYSQL_PWD'),
            getenv('TRASHY_MYSQL_HOST'),
            getenv('TRASHY_MYSQL_DB')))

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
