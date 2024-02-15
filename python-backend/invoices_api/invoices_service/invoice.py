from datetime import date

class Invoice:
    def __init__(self, id: int, customer_id: str, amount: int, status: str, date = date.today(), _record=None):
        self._id = id
        self.customer_id = customer_id
        self.amount = amount
        self._status = status
        self._date = date
        self._record = _record

    @property
    def id(self):
        return self._id or self._record.id
    
    @property
    def date(self):
        return self._date or self._record.date

    @property
    def status(self):
        return self._status or self._record.status

    def dict(self):
        return {
            'id': self.id,
            'customer_id': self.customer_id,
            'amount': self.amount,
            'status': self.status,
            'date': self.date
        }
    
class LatestInvoice:
    def __init__(self, id: int, amount:int, name: str = '', image_url: str = '', email: str = ''):
        self.id = id
        self.name = name
        self.image_url = image_url
        self.email = email
        self.amount = amount

    def dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'name': self.name or 'Could not load customer name',
            'email': self.email or 'Could not load customer email',
            'image_url': self.image_url or '/'
        }
    
class FilteredInvoice:
    def __init__(self, id: int, amount: int, date: str, status: str, name: str = '', email: str = '', image_url: str = ''):
        self.id = id
        self.amount = amount
        self.date = date
        self.status = status
        self.name = name
        self.email = email
        self.image_url = image_url

    def dict(self):
        return {
            'id': self.id,
            'amount': self.amount,
            'date': date.fromisoformat(self.date),
            'status': self.status,
            'name': self.name or 'Could not load customer name',
            'email': self.email or 'Could not load customer email',
            'image_url': self.image_url or '/'
        }