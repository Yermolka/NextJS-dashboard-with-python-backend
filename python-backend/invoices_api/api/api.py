import os
from flask.views import MethodView
from flask_smorest import Blueprint
from datetime import date

import requests

from invoices_api.api.schemas import (
    InvoiceSchema,
    InvoicesCountSchema,
    GetInvoiceSchema,
    ListInvoicesParameters,
    ListInvoicesSchema,
    InvoicesTotalSchema,
    LatestInvoicesParameters,
    ListLatestInvoicesSchema,
    ListInvoicesFilteredParameters,
    ListInvoicesFilteredSchema,
    UpdateInvoiceSchema
)
from invoices_api.invoices_service.invoices_service import InvoicesService
from invoices_api.repository.invoices_repository import InvoicesRepository
from invoices_api.repository.unit_of_work import UnitOfWork

blueprint = Blueprint('invoices', __name__, description='Invoices API')

@blueprint.route('/invoices')
class Invoices(MethodView):

    @blueprint.arguments(ListInvoicesParameters, location='query')
    @blueprint.response(status_code=200, schema=ListInvoicesSchema)
    def get(self, params):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            results = service.list_invoices(**params)
            return {'invoices': [result.dict() for result in results]}
        
    @blueprint.arguments(InvoiceSchema, location='json')
    @blueprint.response(status_code=201, schema=GetInvoiceSchema)
    def post(self, payload):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            result = service.add_invoice(payload)
            unit_of_work.commit()
            return result.dict()
        
@blueprint.route('/invoices/for_customer/<customer_id>')
class InvoicesForCustomer(MethodView):
    
    @blueprint.response(status_code=200, schema=ListInvoicesSchema)
    def get(self, customer_id):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            results = service.list_invoices(customer_id=customer_id)
            return {'invoices': [result.dict() for result in results]}

@blueprint.route('/invoices/for_customer/<customer_id>/count')
class InvoicesCountForCustomer(MethodView):
    
    @blueprint.response(status_code=200, schema=InvoicesCountSchema)
    def get(self, customer_id):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            results = service.get_invoices_count(customer_id=customer_id)
            return {'count': results}

@blueprint.route('/invoices/for_customer/<customer_id>/<invoice_status>')
class InvoicesTotalForCustomer(MethodView):
    
    @blueprint.response(status_code=200, schema=InvoicesTotalSchema)
    def get(self, customer_id, invoice_status):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            results = service.get_invoices_total(customer_id=customer_id, status=invoice_status)
            return {'total': results}

@blueprint.route('/invoices/filtered')
class InvoicesFiltered(MethodView):

    ITEMS_PER_PAGE = 6

    @blueprint.arguments(ListInvoicesFilteredParameters, location='query')
    @blueprint.response(status_code=200, schema=ListInvoicesFilteredSchema)
    def get(self, params: ListInvoicesFilteredParameters):
        query = params.get('query', '')
        offset = (params.get('currentPage', 1) - 1) * self.ITEMS_PER_PAGE
        with UnitOfWork() as unit_of_work:
            results = []
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            invoices = service.get_invoices_filtered(query=query, offset=offset, items_per_page=self.ITEMS_PER_PAGE)
            customers_url = 'http://' + os.getenv('CUSTOMERS_API_HOST_URL') + ':' + os.getenv('CUSTOMERS_API_HOST_PORT')
            
            for invoice in invoices:
                customer = requests.get(customers_url + f'/customers/{invoice.customer_id}').json()
                results.append({
                    'id': invoice.id,
                    'amount': invoice.amount,
                    'date': invoice.date,
                    'status': invoice.status,
                    'name': customer['name'],
                    'email': customer['email'],
                    'image_url': customer['image_url']
                })
            return {'invoices': results}

@blueprint.route('/invoices/<invoice_id>')
class Invoice(MethodView):

    @blueprint.response(status_code=200, schema=GetInvoiceSchema)
    def get(self, invoice_id):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            result = service.get_invoice(invoice_id)
            return result
        
    @blueprint.arguments(UpdateInvoiceSchema, location='json')
    @blueprint.response(status_code=201, schema=GetInvoiceSchema)
    def put(self, payload, invoice_id):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            result = service.update_invoice(invoice_id, payload)
            unit_of_work.commit()
            return result

    @blueprint.response(status_code=204)
    def delete(self, invoice_id):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            service.delete_invoice(invoice_id)
            unit_of_work.commit()
            return
        
@blueprint.route('/invoices/latest')
class InvoicesLatest(MethodView):

    @blueprint.arguments(LatestInvoicesParameters, location='query')
    @blueprint.response(status_code=200, schema=ListLatestInvoicesSchema)
    def get(self, params):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            results = service.get_invoices_latest(**params)
            return {'invoices': results}

@blueprint.route('/invoices/count')
class InvoicesCount(MethodView):

    @blueprint.arguments(ListInvoicesParameters, location='query')
    @blueprint.response(status_code=200, schema=InvoicesCountSchema)
    def get(self, params):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            result = service.get_invoices_count(**params)
            return {'count': result}
        
@blueprint.route('/invoices/total')
class InvoicesTotal(MethodView):

    @blueprint.arguments(ListInvoicesParameters, location='query')
    @blueprint.response(status_code=200, schema=InvoicesTotalSchema)
    def get(self, params):
        with UnitOfWork() as unit_of_work:
            repo = InvoicesRepository(unit_of_work.session)
            service = InvoicesService(repo)
            result = service.get_invoices_total(**params)
            return {'total': result}