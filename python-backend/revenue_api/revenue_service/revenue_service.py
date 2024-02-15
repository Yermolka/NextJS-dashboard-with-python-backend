from revenue_api.repository.revenue_repository import RevenueRepository
from revenue_api.revenue_service.exceptions import RevenueAlreadyExists, RevenueNotFound

class RevenueService:
    def __init__(self, repository: RevenueRepository) -> None:
        self.repository = repository

    def get_revenue(self, month: str):
        record = self.repository.get(month)
        if record:
            return record
        raise RevenueNotFound(f'Revenue for {month} not found')

    def list_revenue(self, **filters):
        return self.repository.list(**filters)
    
    def add_revenue(self, payload):
        record = self.repository.get(payload['month'])
        if record:
            raise RevenueAlreadyExists(f'Revenue for {payload['month']} already exists. Please use an update method')
        return self.repository.add(payload)
    
    def update_revenue(self, month, payload):
        record = self.repository.update(month, **payload)
        if record:
            return record
        raise RevenueNotFound(f'Revenue for {month} not found')
    
    def delete_revenue(self, month):
        resp = self.repository.delete(month)
        if resp:
            return
        raise RevenueNotFound(f'Revenue for {month} not found')