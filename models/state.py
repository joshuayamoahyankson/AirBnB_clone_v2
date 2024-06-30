#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship
from os import getenv


class State(BaseModel, Base):
    """The state class containing name and relationship"""

    __tablename__ = 'states'

    name = Column(String(128), nullable=False)

    cities = relationship('City', backref='state', cascade='all, delete')

    if getenv('HBNB_TYPE_STORAGE') != "db":
        @property
        def cities(self):
            """cities getter method"""
            city_list = []
            for city in models.storage.all(City).values():
                if city.state_id == self.id:
                    city_list.append(city)
            return city_list
