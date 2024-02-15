from typing import List
from invoices_api.invoices_service.invoice import (
    Invoice,
    LatestInvoice,
    FilteredInvoice
    )

from sqlalchemy.orm import Session
from sqlalchemy import desc
from invoices_api.repository.models import InvoiceModel
import requests
import os

class InvoicesRepository:
    def __init__(self, session: Session) -> None:
        self.session = session

    def _get(self, _id, **filters):
        return self.session.query(InvoiceModel) \
            .filter(InvoiceModel.id == _id) \
            .filter_by(**filters) \
            .first()
    
    def get(self, id) -> Invoice:
        record = self._get(id)
        if record is not None:
            return Invoice(**record.dict())
        return None
    
    def add(self, payload) -> Invoice:
        record = InvoiceModel(**payload)
        self.session.add(record)
        return Invoice(**record.dict(), _record=record)
    
    def get_latest(self, **filters) -> List[LatestInvoice]:
        records = self.session.query(InvoiceModel) \
            .order_by(desc(InvoiceModel.date)) \
            .limit(filters.get('limit', 5)) \
            .all()
        
        customers_api_url = 'http://' + os.getenv('CUSTOMERS_API_HOST_URL') + ':' + os.getenv('CUSTOMERS_API_HOST_PORT') + '/customers'
        resp = [
            requests.get(customers_api_url + f'/{record.customer_id}')
            for record in records
        ]

        result = []
        for record, r in zip(records, resp):
            data = {
                'amount': record.amount,
                'id': record.id
            }
            if r.status_code == 200:
                data.update({
                    'name': r.json()['name'],
                    'image_url': r.json()['image_url'],
                    'email': r.json()['email']
                })
            result.append(LatestInvoice(**data))
        return result

    def get_filtered(self, **filters) -> List[Invoice]:
        query = filters.get('query', '')
        offset = filters.get('offset', 0)
        items_per_page = filters.get('items_per_page', 6)

        records = self.session.query(InvoiceModel) \
                .order_by(desc(InvoiceModel.date)) \
                .filter(InvoiceModel.amount.contains(query) | \
                        InvoiceModel.date.contains(query) | \
                        InvoiceModel.status.contains(query)) \
                .limit(items_per_page).offset(offset) \
                .all()
        
        return [Invoice(**record.dict()) for record in records]

    def get_count(self, **filters) -> int:
        records = self.session.query(InvoiceModel)

        if 'minAmount' in filters:
            records = records.filter(InvoiceModel.amount >= filters.pop('minAmount'))

        return records.filter_by(**filters).count()

    def get_total(self, **filters) -> int:
        records = self.session.query(InvoiceModel.amount)

        if 'minAmount' in filters:
            records = records.filter(InvoiceModel.amount >= filters.pop('minAmount'))

        records = records.filter_by(**filters).all()

        total = sum([record.t[0] for record in records])

        return total

    def list(self, **filters) -> List[Invoice]:
        records = self.session.query(InvoiceModel)

        if 'minAmount' in filters:
            records = records.filter(InvoiceModel.amount >= filters.pop('minAmount'))

        records = records.filter_by(**filters).all()

        return [Invoice(**record.dict()) for record in records]
    
    def update(self, id, **payload) -> Invoice:
        record = self._get(id)
        if record is None:
            return None
        
        for key, value in payload.items():
            setattr(record, key, value)
        return Invoice(**record.dict())
    
    def delete(self, id):
        record = self._get(id)
        if record is None:
            return None
        self.session.delete(record)
        return 'OK'