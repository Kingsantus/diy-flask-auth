#!/usr/bin/env python3
""" Module of User Model for database
"""
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


# instantiating declarative base to Base
Base = declarative_base()


class User(Base):
    """Class User for User model"""
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    email = Column(String(250), nullable=False)
    hashed_password = Column(String(250), nullable=False)
    session_id = Column(String(250), nullable=True)
    reset_token = Column(String(250), nullable=True)

    def __repr__(self):
        return "<User(email='%s)>" % (self.email)