from sqlalchemy import Column, String, UUID
from sqlalchemy.ext.declarative import declarative_base
import uuid

def generate_uuid():
    return str(uuid.uuid4())

Base = declarative_base()

class UserModel(Base):
    __tablename__ = 'users'

    id = Column(String, primary_key=True, autoincrement=False, default=generate_uuid)
    name = Column(String(30), nullable=False)
    email = Column(String, nullable=False, unique=True)
    password = Column(String(30), nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }