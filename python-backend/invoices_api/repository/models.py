from sqlalchemy import Column, String, Integer, Date
from sqlalchemy.ext.declarative import declarative_base
from datetime import date

Base = declarative_base()

class InvoiceModel(Base):
    __tablename__ = 'invoices'

    id = Column(Integer, primary_key=True, autoincrement=True)
    customer_id = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    status = Column(String(7), nullable=False, default='pending')
    date = Column(Date, nullable=False, default=date.today)

    def dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'amount': self.amount,
            'status': self.status,
            'date': self.date
        }