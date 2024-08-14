#!/usr/bin/env python3
"""DB module
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.session import Session
from sqlalchemy.exc import NoResultFound, InvalidRequestError
from typing import Optional, List

from user import Base, User


class DB:
    """DB class
    """

    def __init__(self) -> None:
        """Initialize a new DB instance
        """
        self._engine = create_engine("sqlite:///a.db", echo=True)
        Base.metadata.drop_all(self._engine)
        Base.metadata.create_all(self._engine)
        self.__session = None

    @property
    def _session(self) -> Session:
        """Memoized session object
        """
        if self.__session is None:
            DBSession = sessionmaker(bind=self._engine)
            self.__session = DBSession()
        return self.__session
    
    def add_user(self, email: str, hashed_password: str) -> List[str]:
        """add_user create a user"""
        if email is None or hashed_password is None:
            return None
        
        # adding the requirement in the database described column
        new_user = User(email=email, hashed_password=hashed_password)

        self._session.add(new_user)
        self._session.commit()

        return new_user
    
    def find_user_by(self, **kwargs) -> Optional[User]:
        """find user by get the first user information"""
        try:
            user = self._session.query(User).filter_by(**kwargs).one()

            return user
        # if result not found
        except NoResultFound:
            raise NoResultFound("No user found with the given parameters")
        
        # if the argument is not found
        except InvalidRequestError:
            raise InvalidRequestError("Invalid query parameters")
        
    def update_user(self, user_id: int, **kwargs) -> None:
        """method update user information using user_id and the info"""
        try:
            # find the user by user_id
            user = self.find_user_by(id=user_id)

            # update the user attribute with key-value pairs
            for key, value in kwargs.items():
                if hasattr(user, key):
                    setattr(user, key, value)
                else:
                    raise ValueError()

            self._session.commit()
        except:
            raise ValueError() 