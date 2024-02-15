from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class RevenueModel(Base):
    __tablename__ = 'revenue'

    id = Column(Integer, primary_key=True, autoincrement=True)
    month = Column(String(4), nullable=False)
    revenue = Column(Integer, default=0)

    def dict(self):
        return {
            'month': self.month,
            'revenue': self.revenue
        }