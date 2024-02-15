class User:
    def __init__(self, id: str, name: str, email: str, password: str, _record = None):
        self._id = id
        self.name = name
        self.email = email
        self.password = password
        self._record = _record

    @property
    def id(self):
        return self._id or self._record.id
    
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'password': self.password
        }