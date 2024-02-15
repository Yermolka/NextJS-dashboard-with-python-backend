from pathlib import Path
import yaml
from dotenv import load_dotenv
import os

from apispec import APISpec
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from customers_api.api.api import blueprint
from customers_api.config import BaseConfig

from customers_api.customers_service.exceptions import CustomerAlreadyExistsError, CustomerNotFoundError

load_dotenv(Path(__file__).parent.parent / '.env', override=True)

app = Flask(__name__)
cors = CORS(app)
app.config.from_object(BaseConfig)
app.config['CORS_HEADERS'] = 'Content-Type'

customers_api = Api(app)
customers_api.register_blueprint(blueprint)

@app.errorhandler(CustomerAlreadyExistsError)
def custom_RevenueAlreadyExists(error: CustomerAlreadyExistsError):
    return {'code': 405, 'status': str(error)}, 405

@app.errorhandler(CustomerNotFoundError)
def custom_RevenueNotFound(error: CustomerNotFoundError):
    return {'code': 404, 'status': str(error)}, 404

api_spec = yaml.safe_load((Path(__file__).parent / 'oas.yaml').read_text())
spec = APISpec(
    title=api_spec['info']['title'],
    version=api_spec['info']['version'],
    openapi_version=api_spec['openapi']
)
spec.to_dict = lambda: api_spec
customers_api.spec = spec

# Function for usability from utility.py
def run_app():
    app.run(host=os.getenv('CUSTOMERS_API_HOST_URL', '0.0.0.0'), 
            port=os.getenv('CUSTOMERS_API_HOST_PORT', 8000),
            debug=os.getenv('API_DEBUG', False)
            )
    
if __name__=='__main__':
    run_app()