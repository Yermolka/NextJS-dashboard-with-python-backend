from invoices_api.repository.invoices_repository import InvoicesRepository
from invoices_api.invoices_service.exceptions import InvoiceNotFoundError

class InvoicesService:
    def __init__(self, repository: InvoicesRepository) -> None:
        self.repository = repository

    def get_invoice(self, id: int):
        record = self.repository.get(id)
        if record:
            return record
        raise InvoiceNotFoundError(f'Invoice with ID {id} not found')
    
    def list_invoices(self, **filters):
        return self.repository.list(**filters)
    
    def get_invoices_count(self, **filters):
        return self.repository.get_count(**filters)
    
    def get_invoices_total(self, **filters):
        return self.repository.get_total(**filters)

    def add_invoice(self, payload):
        record = self.repository.add(payload)
        return record
    
    def get_invoices_latest(self, **filters):
        return self.repository.get_latest(**filters)
    
    def get_invoices_filtered(self, **filters):
        return self.repository.get_filtered(**filters)

    def update_invoice(self, id: str, payload):
        record = self.repository.update(id, **payload)
        if record:
            return record
        raise InvoiceNotFoundError(f'Invoice with ID {id} not found')
    
    def pay_invoice(self, id: str):
        return self.update_invoice(id, {'status': 'paid'})
    
    def delete_invoice(self, id: str):
        resp = self.repository.delete(id)
        if resp:
            return
        raise InvoiceNotFoundError(f'Invoice with ID {id} not found')