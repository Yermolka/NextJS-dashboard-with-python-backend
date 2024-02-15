from typing import List
from users_api.users_service.user import User
from users_api.repository.models import UserModel

from sqlalchemy.orm import Session
import os
import bcrypt

class UsersRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get_by_id(self, _id: str):
        return self.session.query(UserModel).filter(UserModel.id == _id).first()
    
    def _get_by_email(self, email: str):
        return self.session.query(UserModel).filter(UserModel.email == email).first()
    
    def get_by_email(self, email: str) -> User:
        record = self._get_by_email(email)
        if record is not None:
            return User(**record.dict())
        return None
    
    def list(self) -> List[User]:
        records = self.session.query(UserModel).all()
        return [User(**record.dict()) for record in records]

    def get_by_id(self, id: str) -> User:
        record = self._get_by_id(id)
        if record is not None:
            return User(**record.dict())
        return None

    def add(self, payload) -> User:
        # payload['password'] = bcrypt.hashpw(
        #     bytes(payload['password'], 'UTF-8'), 
        #     bytes(os.getenv('AUTH_SECRET'), 'UTF-8'))
        record = UserModel(**payload)
        self.session.add(record)
        return User(**record.dict(), _record=record)
    
    def update(self, email, **payload) -> User:
        record = self._get_by_email(email)
        if record is None:
            return None
        
        for key, value in payload.items():
            setattr(record, key, value)
        return User(**record.dict())
    
    def delete(self, email):
        record = self._get_by_email(email)
        if record is None:
            return None
        self.session.delete(record)
        return 'OK'