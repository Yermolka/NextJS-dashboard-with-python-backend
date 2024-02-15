import uuid
from sqlalchemy import Column, String
from sqlalchemy.ext.declarative import declarative_base

def generate_uuid() -> str:
    return str(uuid.uuid4())

Base = declarative_base()

class CustomerModel(Base):
    __tablename__ = 'customers'

    id = Column(String, primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    email = Column(String(255), nullable=False, unique=True)
    image_url = Column(String(255), nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'image_url': self.image_url
        }