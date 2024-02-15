class Customer:
    def __init__(self, id: str, name: str, email: str, image_url: str, _record = None) -> None:
        self._id = id
        self.name = name
        self.email = email
        self.image_url = image_url
        self._record = _record

    @property
    def id(self):
        return self._id or self._record.id
    
    def dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'email': self.email,
            'image_url': self.image_url
        }