#!/usr/bin/env python3
"""Handles the authentication of user
"""
import bcrypt
from db import DB
from user import User
from uuid import uuid4
from sqlalchemy.orm.exc import NoResultFound
from typing import TypeVar


T = TypeVar('T')

def _hash_password(password: str) -> bytes:
        """Hash password using bcrypt"""
        password_bytes = password.encode('utf-8')
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password_bytes, salt)
        return hashed_password

def _generate_uuid() -> str:
         """Generating a uuid for users"""
         uuid = uuid4()

         return str(uuid)

class Auth:
    """Auth class to interact with the authentication database.
    """

    def __init__(self):
        self._db = DB()

    def register_user(self, email: str, password: str) -> User:
         """handles authentication of users registration"""
         try:
              user = self._db.find_user_by(email=email)

              if user:
                   raise ValueError(f"User {email} already exists")
         except NoResultFound:
              password_hashed = _hash_password(password)
              new_user = self._db.add_user(email, password_hashed)
              
              return new_user
         
    def valid_login(self, email: str, password: str) -> bool:
         """check the password of the email in database and the password provided"""
         try:
            user = self._db.find_user_by(email=email)
            return bcrypt.checkpw(password.encode('utf-8'), user.hashed_password)
         except NoResultFound:
              return False
         
    def create_session(self, email: str) -> str:
         """Create a uuid for session_id"""
         try:
              user = self._db.find_user_by(email=email)
              
              session_id = _generate_uuid()

              user.session_id = session_id

              self._db._session.commit()
              
              return session_id
         
         except NoResultFound:
              return None
         
    def get_user_from_session_id(self, session_id: str) -> T:
         """get the user session_id of login users"""
         if session_id is None:
              return None
         
         try:
              user = self._db.find_user_by(session_id=session_id)

              return user
         except NoResultFound:
              return None
         
    def destroy_session(self, user_id: int) -> None:
         """Destroyes the user session for user logging out"""
         if user_id is None or user_id <= 0:
              return None 
         
         try:
              user = self._db.find_user_by(id=user_id)
              if user:
                   self._db.update_user(user_id, session_id=None)
         except NoResultFound:
              return None
         
    def get_reset_password_token(self, email: str) -> str:
         """Genrate a unique token for password reset"""
         if email is None:
              return None
         try:
            user = self._db.find_user_by(email=email)

            token_id = _generate_uuid()

            self._db.update_user(user.id, reset_token=token_id)

            return token_id
         
         except NoResultFound:
            raise ValueError()
         
    def update_password(self, reset_token: str, password: str) -> None:
        """method update the password using the reset_token and password"""
        try:
          
          user = self._db.find_user_by(reset_token=reset_token)
          
          password = _hash_password(password)
          
          self._db.update_user(user.id, hashed_password=password)

          self._db.update_user(user.id, reset_token=None)
          
          return user
        
        except NoResultFound:
             raise ValueError