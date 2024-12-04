from flask import Blueprint, request, abort
from models.user import User
from models.user_stats import User_stats
from flaskapp.auth import login_required
from swagger_generator import generator
import bcrypt

users_bluerprint = Blueprint('users', __name__)

def get_hashed_password(plain_text_password):
    # Hash a password for the first time
    #   (Using bcrypt, the salt is saved into the hash itself)
    return bcrypt.hashpw(plain_text_password, bcrypt.gensalt())

def check_password(plain_text_password, hashed_password):
    # Check hashed password. Using bcrypt, the salt is saved into the hash itself
    return bcrypt.checkpw(plain_text_password, hashed_password)



# Register
@generator.request_body(schema={'username': 'jutjuan', 'email': 'jutjuan@gmail.com', 'password': 'awdf12#AF12df', 'confPassword': 'awdf12#AF12df'})
@generator.response(status_code=200, schema={'id': 10, 'username': 'jutjuan', 'email': 'jutjuan@gmail.com', 'riot_id': 'jutjuan#EUW', 'puuid': 'qHn0uNkpA1T-NqQ0zHTEqNh1BhH5SAsGWwkZsacbeKBqSdkUEaYOcYNjDomm60vMrLWHu4ulYg1C5Q'})
@users_bluerprint.post('/register')
def register():
    username = request.json.get('username')
    email = request.json.get('email')
    password = request.json.get('password')
    conf_password = request.json.get('confPassword')

    if password != conf_password:
        abort(400, 'Passwords do not match')
    
    if User.query.filter_by(username=username).first() is not None:
        abort(400, 'Username already exists')

    # Create user
    secure_password = get_hashed_password(bytes(password, 'utf-8'))
    user = User(username, email, secure_password)
    user.save()

    # Create user stats
    user_stats = User_stats(user_id=user.id)
    user_stats.save()

    # Return 200
    return user.json(), 200


# Login
@generator.request_body(schema={'username': 'jutjuan', 'password': 'awdf12#AF12df'})
@generator.response(status_code=200, schema={'id': 10, 'username': 'jutjuan', 'email': 'jutjuan@gmail.com', 'riot_id': 'jutjuan#EUW', 'puuid': 'qHn0uNkpA1T-NqQ0zHTEqNh1BhH5SAsGWwkZsacbeKBqSdkUEaYOcYNjDomm60vMrLWHu4ulYg1C5Q'})
@users_bluerprint.post('/login')
def login():
    username = request.json.get('username')
    password = request.json.get('password')

    user = User.query.filter_by(username=username).first()
    if user is None:
        abort(404, 'User not found')
    if not check_password(bytes(password, 'utf-8'), bytes(user.password, 'utf-8')):
        abort(401, 'Password is incorrect')

    # Return 200
    return user.json(), 200


#Retrieve persnal info
@generator.response(status_code=200, schema={'id': 10, 'username': 'jutjuan', 'email': 'jutjuan@gmail.com', 'riot_id': 'jutjuan#EUW', 'puuid': 'qHn0uNkpA1T-NqQ0zHTEqNh1BhH5SAsGWwkZsacbeKBqSdkUEaYOcYNjDomm60vMrLWHu4ulYg1C5Q'})
@users_bluerprint.get('/account/<int:user_id>')
@login_required
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404, 'User not found')

    return user.json(), 200


#Update field
@generator.request_body(schema={'field': 'username', 'value': 'newName'})
@generator.response(status_code=200, schema={'id': 10, 'username': 'jutjuan', 'email': 'jutjuan@gmail.com', 'riot_id': 'jutjuan#EUW', 'puuid': 'qHn0uNkpA1T-NqQ0zHTEqNh1BhH5SAsGWwkZsacbeKBqSdkUEaYOcYNjDomm60vMrLWHu4ulYg1C5Q'})
@users_bluerprint.put('/update-field/<int:user_id>')
@login_required
def update_field(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404, 'User not found')

    field = request.json.get('field')
    value = request.json.get('value')

    if field == 'username':
        user.username = value
    elif field == 'email':
        user.email = value
    elif field == 'riot_id':
        user.riot_id = value
    else:
        abort(400, 'Invalid field')

    user.save()
    return user.json(), 200


#Delete user
@generator.response(status_code=200, schema={})
@users_bluerprint.delete('/delete/<int:user_id>')
@login_required
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    if user is None:
        abort(404, 'User not found')

    user.delete()
    return '', 200