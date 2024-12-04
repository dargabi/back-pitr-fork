import os

from flask import Flask
from blueprints.users import users_bluerprint
from blueprints.test import test_blueprint
from blueprints.stats import stats_bluerprint
from blueprints.tournaments import tournaments_bluerprint
from database import init_db
from errors import register_error_handlers
from env_secrets import secrets
from swagger_generator import generator
from blueprints.swagger_ui import register_swaggerui_blueprint

PREFIX = '/api-rivals/v1'

def create_app():
    # Create and configure the app
    app = Flask(__name__, instance_relative_config=True, static_url_path=f'{PREFIX}/static')
    app.json.sort_keys = False # Disable sorting of JSON keys

    return app



# Create the app
app = create_app()

# Register the blueprints
app.register_blueprint(test_blueprint, url_prefix=f'{PREFIX}/test')
app.register_blueprint(users_bluerprint, url_prefix=f'{PREFIX}/users')
app.register_blueprint(stats_bluerprint, url_prefix=f'{PREFIX}/stats')
app.register_blueprint(tournaments_bluerprint, url_prefix=f'{PREFIX}/tournaments')
register_error_handlers(app)

# Initialize the database
print('Initializing the database')
init_db()

# Generate the Swagger file
print('Generating the Swagger file')
swagger_destination_path = 'static/docs/swagger.yaml'
generator.generate_swagger(app, destination_path=swagger_destination_path, application_name='Pit Rivals API', application_version='1.0.0')
swaggerui_blueprint = register_swaggerui_blueprint(app) 
app.register_blueprint(swaggerui_blueprint)