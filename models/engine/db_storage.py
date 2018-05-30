#!/usr/bin/python3
"""
Creates the DBStorage class
"""
import models
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
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.format(
            getenv('TRASHY_MYSQL_USER'),
            getenv('TRASHY_MYSQL_PWD'),
            getenv('TRASHY_MYSQL_HOST'),
            getenv('TRASHY_MYSQL_DB')))

    def all(self, cls=None):
        """
        Grabs all markers if class is not User
        """
        class_list = []
        if cls is None:
            for key, value in models.classes.items():
                class_list.append(value)
        else:
            pass
        new_dict = {}
        for search in class_list:
            try:
                capture = self.__session.query(search).all()
            except:
                continue
            for objects in capture:
                key = str(objects.__class__.__name__) + '.' + objects.id
                new_dict[key] = objects
        return new_dict

    def new(self, obj):
        """
        Adds the object to the database
        """
        self.__session.add(obj)

    def delete(self, obj=None):
        """
        Deletes the object from the database
        """
        if (obj):
            self.__session.delete(obj)
            self.save()

    def save(self):
        """
        Saves the current session to the database
        """
        self.__session.commit()


    def reload(self):
        """
        Binds the current session to the instance
        """
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(
                sessionmaker(
                bind=self.__engine,
                expire_on_commit=False))
