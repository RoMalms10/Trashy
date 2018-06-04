#!/usr/bin/python3
"""
Creates the DBStorage class
"""
import models
from models.user import Base
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlite3 import dbapi2 as sqlite
from math import cos, acos, sin, radians

class DBStorage():
    """
    Class that handles the set up and storage of information in a database
    """

    __engine = None
    __session = None
    raw_conn = None

    def __init__(self):
        """
        Initializes an instance of DBStorage
        """
        self.__engine = create_engine(
        'sqlite+pysqlite:///trashy_db.db',
        native_datetime=True,
        module=sqlite,
        pool_pre_ping=True, echo=False)

        self.raw_conn = self.__engine.raw_connection()
        self.raw_conn.create_function("acos", 1, acos)
        self.raw_conn.create_function("cos", 1, cos)
        self.raw_conn.create_function("sin", 1, sin)
        self.raw_conn.create_function("radians", 1, radians)

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
                pass
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

    # def rollback(self):
    #     """
    #     """
    #     self.__session.rollback()

    def proximity(self, latitude=None, longitude=None, radius=.02):
        """
        Search for closest 20 trash can near the user
        """
        new_list = []
        query = """
                SELECT id, latitude, longitude, name, ( 6371 * acos( cos( radians({}) ) * cos( radians( latitude ) ) 
                * cos( radians( longitude ) - radians({}) ) + sin( radians({}) ) * sin(radians(latitude)) ) ) AS distance 
                FROM markers
                GROUP BY id 
                HAVING distance < {}
                ORDER BY distance
                LIMIT 0, 20; 
                """.format(latitude, longitude, latitude, radius)
        capture = self.raw_conn.execute(query)
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
                print(email, "==", value.email, "is: ", value.email == email)
                print(u'squidcarroll@gmail.com' == value.email)
                print(value.email)
                if value.email == email:
                    print("found something")
                    return value
            print("Right after loop")
            return None
        else:
            print("email doesn't exist")
            return None

    def g_auth_user_id(self, cls, user_id=None):
        """
        """
        if user_id is not None:
            user_dict = self.all(cls)
            for key, value in user_dict.items():
                if value.id == user_id:
                    return value
            return None
        else:
            return None
        # elif email is not None:
        #     self.__session.query().filter_by(email=email)
