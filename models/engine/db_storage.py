#!/usr/bin/python3
"""A DBstorage engine definition"""

from os import getenv
from models.base_model import BaseModel, Base
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from sqlalchemy import create_engine
from sqlalchemy.orm import relationship
from sqlalchemy.orm import scoped_session
from sqlalchemy.orm import sessionmaker


classes = {
    'BaseModel': BaseModel, 'User': User, 'Place': Place,
    'State': State, 'City': City, 'Amenity': Amenity,
    'Review': Review
}


class DBStorage:
    """The BDStorage class definition"""
    __engine = None
    __session = None

    def __init__(self):
        """A construction that creates an engine via environment variables"""
        user = getenv('HBNB_MYSQL_USER')
        password = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        database = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine(
            f'mysql+mysqldb://{user}:{password}@{host}/{database}',
            pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadate.drop_all(self.__engine)

    def all(self, cls=None):
        """A method to query on the database session"""
        objects = {}
        for clas in classes:
            if cls is None or cls is classes[clas] or cls is clas:
                objects_1 = self.__session.query(classes[clas]).all()
                for obj in objects_1:
                    key = "{}.{}".format(type(obj).__name__, obj.id)
                    objects[key] = obj
        return objects

    def new(self, obj):
        """A method that adds session to current db"""
        self.__session.add(obj)

    def save(self):
        """A method to commit changes to current db session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Deletes obj from current database session"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """A reload method to create al tables"""
        Base.metadata.create_all(self.__engine)
        session_factory = sessionmaker(bind=self.__engine,
                                       expire_on_commit=False)
        Session = scoped_session(session_factory)
        self.__session = Session()
