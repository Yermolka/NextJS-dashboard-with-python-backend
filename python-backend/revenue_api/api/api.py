from typing import List
from flask import abort
from flask.views import MethodView
from flask_smorest import Blueprint
from marshmallow import ValidationError

from revenue_api.api.schemas import (
    RevenueSchema,
    GetListRevenueParameters,
    ListRevenueSchema,
    UpdateRevenueSchema,
)
from revenue_api.revenue_service.revenue_service import RevenueService
from revenue_api.repository.revenue_repository import RevenueRepository
from revenue_api.repository.unit_of_work import UnitOfWork

blueprint = Blueprint('revenue', __name__, description='Revenue API')

@blueprint.route('/revenue')
class Revenue(MethodView):

    @blueprint.arguments(GetListRevenueParameters, location='query')
    @blueprint.response(status_code=200, schema=ListRevenueSchema)
    def get(self, params):
        with UnitOfWork() as unit_of_work:
            repo = RevenueRepository(unit_of_work.session)
            service = RevenueService(repo)
            results = service.list_revenue(**params)
        return {'revenue': [result.dict() for result in results]}
    
    @blueprint.arguments(RevenueSchema, location='json')
    @blueprint.response(status_code=201, schema=RevenueSchema)
    def post(self, payload):
        with UnitOfWork() as unit_of_work:
            repo = RevenueRepository(unit_of_work.session)
            service = RevenueService(repo)
            result = service.add_revenue(payload)
            unit_of_work.commit()
        return result
    
@blueprint.route('/revenue/<month>')
class RevenueMonth(MethodView):

    @blueprint.response(status_code=200, schema=RevenueSchema)
    def get(self, month):
        with UnitOfWork() as unit_of_work:
            repo = RevenueRepository(unit_of_work.session)
            service = RevenueService(repo)
            revenue = service.get_revenue(month)
        return revenue.dict()
    
    @blueprint.arguments(UpdateRevenueSchema, location='json')
    @blueprint.response(status_code=200, schema=RevenueSchema)
    def put(self, payload, month):
        with UnitOfWork() as unit_of_work:
            repo = RevenueRepository(unit_of_work.session)
            service = RevenueService(repo)
            result = service.update_revenue(month, payload)
            unit_of_work.commit()
        return result
    
    @blueprint.response(status_code=204)
    def delete(self, month):
        with UnitOfWork() as unit_of_work:
            repo = RevenueRepository(unit_of_work.session)
            service = RevenueService(repo)
            service.delete_revenue(month)
            unit_of_work.commit()