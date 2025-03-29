from flask import request, jsonify, current_app
from flask_login import login_user, logout_user, login_required
from flask_principal import Identity, AnonymousIdentity, identity_changed
from core.utils import create_api
from services.auth.schemas import User


auth_api = create_api('auth_api', __name__)


@auth_api.route('/login', methods=['POST'])
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

@auth_api.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    identity_changed.send(
        current_app._get_current_object(), 
        identity=AnonymousIdentity()
    )
    return jsonify({'message': 'Logged out successfully'}), 200


@auth_api.route('/some_protected_route')
@login_required
def some_protected_route():
    return jsonify({'message': 'Hi'}), 200

@auth_api.route('/admin/protected')
@auth_api.roles_accepted('admin')
def admin_protected():
    return jsonify({'message': 'Hi admin'}), 200

@auth_api.route('/teacher/protected')
@auth_api.roles_accepted('teacher')
def teacher_protected():
    return jsonify({'message': 'Hi teacher'}), 200
