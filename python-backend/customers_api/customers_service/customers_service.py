from customers_api.repository.customers_repository import CustomerRepository
from customers_api.customers_service.exceptions import CustomerAlreadyExistsError, CustomerNotFoundError

class CustomersService:
    def __init__(self, repository: CustomerRepository) -> None:
        self.repository = repository

    def get_customer(self, id: str):
        record = self.repository.get(id)
        if record:
            return record
        raise CustomerNotFoundError(f'Customer with ID {id} not found')
    
    def list_customers(self, **filters):
        return self.repository.list(**filters)
    
    def get_customers_count(self, **filters):
        return self.repository.get_count(**filters)
    
    def add_customer(self, payload):
        record = self.repository.add(payload)
        if record:
            return record
        raise CustomerAlreadyExistsError(f'Customer with email {payload['email']} already exists')
    
    def update_customer(self, id: str, payload):
        record = self.repository.update(id, **payload)
        if record:
            return record
        raise CustomerNotFoundError(f'Customer with ID {id} not found')
    
    def delete_customer(self, id: str):
        resp = self.repository.delete(id)
        if resp:
            return
        raise CustomerNotFoundError(f'Customer with ID {id} not found')