from users_api.repository.users_repository import UsersRepository
from users_api.users_service.exceptions import UserNotFoundError

class UsersService:
    def __init__(self, repository: UsersRepository):
        self.repository = repository

    def get_user_by_id(self, id: int):
        record = self.repository.get_by_id(id)
        if record:
            return record
        raise UserNotFoundError(f'User with ID {id} not found.')
    
    def get_user_by_email(self, email: str):
        record = self.repository.get_by_email(email)
        if record:
            return record
        raise UserNotFoundError(f'User with email {email} not found.')
    
    def list_users(self):
        return self.repository.list()

    def add_user(self, payload):
        return self.repository.add(payload)

    def update_user(self, email: str, payload):
        record = self.repository.update(email, **payload)
        if record:
            return record
        raise UserNotFoundError(f'User with ID {email} not found.')
    
    def delete_invoice(self, email: str):
        resp = self.repository.delete(email)
        if resp:
            return
        raise UserNotFoundError(f'User with ID {email} not found.')