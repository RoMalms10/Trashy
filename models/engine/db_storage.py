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
        self.__engine = create_engine('mysql+pymysql://{}:{}@{}/{}'.format(
            getenv('TRASHY_MYSQL_USER'),
            getenv('TRASHY_MYSQL_PWD'),
            getenv('TRASHY_MYSQL_HOST'),
            getenv('TRASHY_MYSQL_DB')))

    def all(self, cls=None):
        """
        Grabs all markers if class is not User and returns a dict of them
        cls is a string
        """
        class_list = []
        if cls is None:
            for key, value in models.classes.items():
                class_list.append(value)
        else:
            class_list.append(models.classes[cls])
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

    def proximity(self, latitude=None, longitude=None, radius=.02):
        """
        Search for closest 20 trash can near the user
        """
        new_list = []
        query = """
                SELECT id, latitude, longitude, name, ( 6371 * acos( cos( radians({}) ) * cos( radians( latitude ) ) 
                * cos( radians( longitude ) - radians({}) ) + sin( radians({}) ) * sin(radians(latitude)) ) ) AS distance 
                FROM markers 
                HAVING distance < {}
                ORDER BY distance
                LIMIT 0, 20; 
                """.format(latitude, longitude, latitude, radius)
        capture = self.__session.execute(query)
        for objects in capture:
            new_dict = {}
            new_dict["latitude"] = objects[1]
            new_dict["longitude"] = objects[2]
            new_dict["name"] = objects[3]
            new_list.append(new_dict)
        return (new_list)

    def g_auth_user(self, cls, email=None):
        """
        Method used to retrieve the user stored in the database
        cls is a string
        """
        if email is not None:
            user_dict = self.all(cls)
            for key, value in user_dict.items():
                if value.email == email:
                    return (value)
        else:
            return None

    def g_auth_user_id(self, cls, user_id=None):
        """
        """
        if user_id is not None:
            user_dict = self.all(cls)
            print(user_dict)
            for key, value in user_dict.items():
                if value.id == user_id:
                    return (value)
        else:
            return None
        # elif email is not None:
        #     self.__session.query().filter_by(email=email)
