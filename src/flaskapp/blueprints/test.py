from flask import Blueprint, request, abort
from swagger_generator import generator
import bcrypt

test_blueprint = Blueprint('test', __name__)


# Tests
@generator.response(status_code=200, schema={})
@test_blueprint.get('/test')
def test():
    return 'Hello, World!'

@generator.response(status_code=200, schema={})
@test_blueprint.post('/test-post')
def test_post():
    return 'Hello, World!'