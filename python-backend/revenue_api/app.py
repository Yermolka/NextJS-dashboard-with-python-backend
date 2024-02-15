from pathlib import Path
import yaml
from dotenv import load_dotenv
import os

from apispec import APISpec
from flask import Flask
from flask_smorest import Api
from flask_cors import CORS

from revenue_api.api.api import blueprint
from revenue_api.config import BaseConfig

from revenue_api.revenue_service.exceptions import RevenueAlreadyExists, RevenueNotFound

load_dotenv(Path(__file__).parent.parent / '.env', override=True)

app = Flask(__name__)
cors = CORS(app)
app.config.from_object(BaseConfig)
app.config['CORS_HEADERS'] = 'Content-Type'

revenue_api = Api(app)
revenue_api.register_blueprint(blueprint)

@app.errorhandler(RevenueAlreadyExists)
def custom_RevenueAlreadyExists(error: RevenueAlreadyExists):
    return {'code': 405, 'status': str(error)}, 405

@app.errorhandler(RevenueNotFound)
def custom_RevenueNotFound(error: RevenueNotFound):
    return {'code': 404, 'status': str(error)}, 404

api_spec = yaml.safe_load((Path(__file__).parent / 'oas.yaml').read_text())
spec = APISpec(
    title=api_spec['info']['title'],
    version=api_spec['info']['version'],
    openapi_version=api_spec['openapi']
)
spec.to_dict = lambda: api_spec
revenue_api.spec = spec

# Function for usability from utility.py
def run_app():
    app.run(host=os.getenv('REVENUE_API_HOST_URL', '0.0.0.0'), 
            port=os.getenv('REVENUE_API_HOST_PORT', 8001),
            debug=os.getenv('API_DEBUG', False)
            )
    
if __name__=='__main__':
    run_app()