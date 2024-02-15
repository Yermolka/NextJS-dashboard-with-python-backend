import os
from flask.views import MethodView
from flask_smorest import Blueprint
import requests

from customers_api.api.schemas import (
    CustomerSchema,
    CustomersFilteredParameters,
    GetCustomerSchema,
    ListCustomersFilteredSchema,
    ListCustomersParameters,
    ListCustomersSchema,
    CustomerCountSchema,
    GetCustomerParameters,
    UpdateCustomerSchema,
)
from customers_api.customers_service.customers_service import CustomersService
from customers_api.repository.customers_repository import CustomerRepository
from customers_api.repository.unit_of_work import UnitOfWork

blueprint = Blueprint('customers', __name__, description='Customers API')

@blueprint.route('/customers')
class Customers(MethodView):

    @blueprint.arguments(ListCustomersParameters, location='query')
    @blueprint.response(status_code=200, schema=ListCustomersSchema)
    def get(self, params):
        with UnitOfWork() as unit_of_work:
            repo = CustomerRepository(unit_of_work.session)
            service = CustomersService(repo)
            results = service.list_customers(**params)
        return {'customers': [result.dict() for result in results]}
    
    @blueprint.arguments(CustomerSchema, location='json')
    @blueprint.response(status_code=201, schema=GetCustomerSchema)
    def post(self, payload):
        with UnitOfWork() as unit_of_work:
            repo = CustomerRepository(unit_of_work.session)
            service = CustomersService(repo)
            result = service.add_customer(payload)
            unit_of_work.commit()
            return result.dict()
        
@blueprint.route('/customers/count')
class CustomersCount(MethodView):

    @blueprint.arguments(ListCustomersParameters, location='query')
    @blueprint.response(status_code=200, schema=CustomerCountSchema)
    def get(self, params):
        with UnitOfWork() as unit_of_work:
            repo = CustomerRepository(unit_of_work.session)
            service = CustomersService(repo)
            result = service.get_customers_count(**params)
            return {'count': result}
        
@blueprint.route('/customers/<customer_id>')
class Customer(MethodView):

    @blueprint.arguments(GetCustomerParameters, location='query')
    @blueprint.response(status_code=200, schema=GetCustomerSchema)
    def get(self, params, customer_id):
        with UnitOfWork() as unit_of_work:
            repo = CustomerRepository(unit_of_work.session)
            service = CustomersService(repo)
            result = service.get_customer(customer_id)
            return result.dict()
        
    @blueprint.arguments(UpdateCustomerSchema, location='json')
    @blueprint.response(status_code=201, schema=GetCustomerSchema)
    def put(self, payload, customer_id):
        with UnitOfWork() as unit_of_work:
            repo = CustomerRepository(unit_of_work.session)
            service = CustomersService(repo)
            result = service.update_customer(customer_id, payload)
            unit_of_work.commit()
            return result.dict()
        
    @blueprint.response(status_code=204)
    def delete(self, customer_id):
        with UnitOfWork() as unit_of_work:
            repo = CustomerRepository(unit_of_work.session)
            service = CustomersService(repo)
            service.delete_customer(customer_id)
            unit_of_work.commit()

@blueprint.route('/customers/filtered')
class CustomersFiltered(MethodView):

    @blueprint.arguments(CustomersFilteredParameters, location='query')
    @blueprint.response(status_code=200, schema=ListCustomersFilteredSchema)
    def get(self, query):
        with UnitOfWork() as unit_of_work:
            repo = CustomerRepository(unit_of_work.session)
            service = CustomersService(repo)
            customers = service.list_customers(**query)
            result = []
            invoices_url = 'http://' + os.getenv('INVOICES_API_HOST_URL') + ':' + os.getenv('INVOICES_API_HOST_PORT') + '/invoices'
            for c in customers:
                count = requests.get(invoices_url + '/for_customer/' + c.id + '/count').json()['count']
                total_pending = requests.get(invoices_url + '/for_customer/' + c.id + '/pending').json()['total']
                total_paid = requests.get(invoices_url + '/for_customer/' + c.id + '/paid').json()['total']
                result.append({
                    'id': c.id,
                    'name': c.name,
                    'email': c.email,
                    'image_url': c.image_url,
                    'total_invoices': count,
                    'total_pending': total_pending / 100.0,
                    'total_paid': total_paid / 100.0
                })
            return { 'customers': result }
            