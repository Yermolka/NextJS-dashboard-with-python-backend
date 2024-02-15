from typing import List
from revenue_api.revenue_service.revenue import Revenue
from sqlalchemy.orm import Session
from revenue_api.repository.models import RevenueModel

class RevenueRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get(self, month, **filters):
        return self.session.query(RevenueModel) \
            .filter(RevenueModel.month == month) \
            .filter_by(**filters) \
            .first()

    def get(self, month) -> Revenue:
        record = self._get(month)
        if record is not None:
            return Revenue(**record.dict())
        return None

    def add(self, revenue) -> Revenue:
        record = RevenueModel(**revenue)
        self.session.add(record)
        return Revenue(**record.dict())

    def list(self, **filters) -> List[Revenue]:
        records = self.session.query(RevenueModel)

        if 'minValue' in filters:
            records = records.filter(RevenueModel.revenue >= filters['minValue'])

        records = records.all()

        return [Revenue(**record.dict()) for record in records]
    
    def update(self, month, **payload) -> Revenue:
        record = self._get(month)
        if record is None:
            return None
        
        for key, value in payload.items():
            setattr(record, key, value)
        return Revenue(**record.dict())
    
    def delete(self, month):
        record = self._get(month)
        if record is None:
            return None
        self.session.delete(record)
        return 'OK'
