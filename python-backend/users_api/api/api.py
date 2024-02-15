from flask.views import MethodView
from flask_smorest import Blueprint

from users_api.api.schemas import (
    UserSchema,
    GetUserSchema,
    UpdateUserSchema
)
from users_api.users_service.users_service import UsersService
from users_api.repository.users_repository import UsersRepository
from users_api.repository.unit_of_work import UnitOfWork

blueprint = Blueprint('users', __name__, description='Users API')

@blueprint.route('/users')
class Users(MethodView):

    @blueprint.response(status_code=200)
    def get(self):
        with UnitOfWork() as unit_of_work:
            repo = UsersRepository(unit_of_work.session)
            service = UsersService(repo)
            results = service.list_users()
            return [result.dict() for result in results]

    @blueprint.arguments(UserSchema, location='json')
    @blueprint.response(status_code=201, schema=GetUserSchema)
    def post(self, payload):
        with UnitOfWork() as unit_of_work:
            repo = UsersRepository(unit_of_work.session)
            service = UsersService(repo)
            result = service.add_user(payload)
            unit_of_work.commit()
            return result.dict()
        
@blueprint.route('/users/<user_email>')
class User(MethodView):

    @blueprint.response(status_code=200, schema=GetUserSchema)
    def get(self, user_email):
        with UnitOfWork() as unit_of_work:
            repo = UsersRepository(unit_of_work.session)
            service = UsersService(repo)
            result = service.get_user_by_email(user_email)
            return result.dict()
        
    @blueprint.arguments(UpdateUserSchema, location='json')
    @blueprint.response(status_code=201, schema=GetUserSchema)
    def put(self, payload, user_email):
        with UnitOfWork() as unit_of_work:
            repo = UsersRepository(unit_of_work.session)
            service = UsersService(repo)
            result = service.update_user(user_email, payload)
            unit_of_work.commit()
            return result.dict()
        
    @blueprint.response(status_code=204)
    def delete(self, user_email):
        with UnitOfWork() as unit_of_work:
            repo = UsersRepository(unit_of_work.session)
            service = UsersService(repo)
            service.delete_invoice(user_email)
            unit_of_work.commit()
            return