from pathlib import Path
import yaml
from dotenv import load_dotenv
import os

from apispec import APISpec
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from invoices_api.api.api import blueprint
from invoices_api.config import BaseConfig

from invoices_api.invoices_service.exceptions import InvoiceNotFoundError

load_dotenv(Path(__file__).parent.parent / '.env', override=True)

app = Flask(__name__)
cors = CORS(app)
app.config.from_object(BaseConfig)
app.config['CORS_HEADERS'] = 'Content-Type'

invoices_api = Api(app)
invoices_api.register_blueprint(blueprint)

@app.errorhandler(InvoiceNotFoundError)
def custom_RevenueNotFound(error: InvoiceNotFoundError):
    return {'code': 404, 'status': str(error)}, 404

api_spec = yaml.safe_load((Path(__file__).parent / 'oas.yaml').read_text())
spec = APISpec(
    title=api_spec['info']['title'],
    version=api_spec['info']['version'],
    openapi_version=api_spec['openapi']
)
spec.to_dict = lambda: api_spec
invoices_api.spec = spec

# Function for usability from utility.py
def run_app():
    app.run(host=os.getenv('INVOICES_API_HOST_URL', '0.0.0.0'), 
            port=os.getenv('INVOICES_API_HOST_PORT', 8002),
            debug=os.getenv('API_DEBUG', False)
            )
    
if __name__=='__main__':
    run_app()