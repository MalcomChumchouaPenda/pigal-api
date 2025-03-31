from flask import request, jsonify, current_app
from flask_login import login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed

from core.config import db
from core.utils import create_api
from services.auth.models import User, Role
from services.auth.schemas import user_schema, users_schema


api = create_api('auth_api', __name__)


# AUTHENTIFICATIOM / AUTHORIZATION ROUTES

@api.route('/login', methods=['POST'])
def login():
    data = request.json
    user = User.query.filter_by(id=data['id']).first()
    if user and user.check_password(data['password']):
        login_user(user)
        identity_changed.send(
            current_app._get_current_object(), 
            identity=Identity(user.id)
        )
        return jsonify({'message': 'Logged in successfully'}), 200
    return jsonify({'message': 'Invalid credentials'}), 401

@api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(), 
        identity=AnonymousIdentity()
    )
    return jsonify({'message': 'Logged out successfully'}), 200


# USER ROUTES

@api.route('/users', methods=['GET'])
def get_users():
    query = User.query
    role_id = request.args.get('role')
    if role_id:
        query = query.join(User.roles)
        query = query.filter(Role.id == role_id)
    users = query.all()
    return users_schema.dump(users)

@api.route('/users/<user_id>', methods=['GET'])
def get_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    return user_schema.dump(user)

@api.route('/users/<user_id>', methods=['POST'])
def add_user(user_id):
    data = request.json
    pwd = data.pop('password')
    user = User(**data)
    user.id = user_id
    user.set_password(pwd)
    session = db.session
    session.add(user)
    session.commit()
    print(data)
    return {"message": "user added"}, 200

@api.route('/users/<user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    data = request.json
    password = data.get('password')
    print('get pwd', password)
    if password:
        print(user, user.password_hash)
        user.set_password(password)
        print(user, user.password_hash)

    lang = data.get('lang')
    if lang:
        user.lang = lang
    db.session.commit()
    return {"message": "user updated"}, 200

@api.route('/users/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.filter_by(id=user_id).first()
    session = db.session
    session.delete(user)
    session.commit()
    return "", 204
