from flask import Flask, url_for
from flask_swagger_ui import get_swaggerui_blueprint

def register_swaggerui_blueprint(app):
    with app.app_context(), app.test_request_context():
        SWAGGER_URL = '/api-rivals/docs'  # URL for exposing Swagger UI (without trailing '/')
        API_URL = url_for('static', filename='docs/swagger.yaml')  # Our API url (can of course be a local resource)

    # Call factory function to create our blueprint
    swaggerui_blueprint = get_swaggerui_blueprint(
        SWAGGER_URL,  # Swagger UI static files will be mapped to '{SWAGGER_URL}/dist/'
        API_URL,
        config={  # Swagger UI config overrides
            'app_name': "Test application"
        },
    )

    return swaggerui_blueprint