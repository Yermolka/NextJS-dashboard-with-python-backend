from typing import List
from customers_api.customers_service.customer import Customer
from sqlalchemy.orm import Session
from customers_api.repository.models import CustomerModel

class CustomerRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get(self, _id, **filters):
        return self.session.query(CustomerModel) \
            .filter(CustomerModel.id == _id) \
            .filter_by(**filters) \
            .first()
    
    def get(self, id) -> Customer:
        record = self._get(id)
        if record is not None:
            return Customer(**record.dict())
        return None
    
    def add(self, payload) -> Customer:
        if self.session.query(CustomerModel).filter(CustomerModel.email == payload['email']).first():
            return None
        record = CustomerModel(**payload)
        self.session.add(record)
        return Customer(**record.dict(), _record=record)
    
    def get_count(self, **filters) -> List[Customer]:
        return self.session.query(CustomerModel).filter_by(**filters).count()

    def list(self, **filters) -> List[Customer]:
        records = self.session.query(CustomerModel)

        if 'query' in filters:
            records = records.filter(CustomerModel.email.contains(filters['query'])) \
                            .filter(CustomerModel.name.contains(filters['query']))
            filters.pop('query')

        records = records.all()

        return [Customer(**record.dict()) for record in records]
    
    def update(self, id, **payload) -> Customer:
        record = self._get(id)
        if record is None:
            return None
        
        for key, value in payload.items():
            setattr(record, key, value)
        return Customer(**record.dict())
    
    def delete(self, id):
        record = self._get(id)
        if record is None:
            return None
        self.session.delete(record)
        return 'OK'