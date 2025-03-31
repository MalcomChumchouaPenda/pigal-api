
import json
from flask import jsonify
from core.utils import login_required
from services.auth.routes import api
from services.auth.models import User


def test_login_success(client):
    """Test de connexion réussie avec des identifiants valides."""
    response = client.post('/auth/login', json={"id": "admin1", "password": "adminpass"})
    assert response.status_code == 200
    assert response.json["message"] == "Logged in successfully"

def test_login_failure(client):
    """Test de connexion échouée avec un mauvais mot de passe."""
    response = client.post('/auth/login', json={"id": "admin1", "password": "wrongpass"})
    assert response.status_code == 401
    assert response.json["message"] == "Invalid credentials"

def test_logout(client):
    """Test de déconnexion après une connexion réussie."""
    client.post('/auth/login', json={"id": "admin1", "password": "adminpass"})
    response = client.post('/auth/logout')
    assert response.status_code == 200
    assert response.json["message"] == "Logged out successfully"



@api.route('/some_protected_route')
@login_required
def some_protected_route():
    return jsonify({'message': 'Hi'}), 200

@api.route('/admin/protected')
@api.roles_accepted('admin')
def admin_protected():
    return jsonify({'message': 'Hi admin'}), 200

@api.route('/teacher/protected')
@api.roles_accepted('teacher')
def teacher_protected():
    return jsonify({'message': 'Hi teacher'}), 200


def test_protected_route_without_login(client):
    """Test d'accès à une route protégée sans connexion."""
    response = client.get('/auth/some_protected_route')
    assert response.status_code == 401

def test_admin_access(client):
    """Test d'accès à une route réservée aux admins."""
    client.post('/auth/login', json={"id": "admin1", "password": "adminpass"})
    response = client.get('/auth/admin/protected')
    assert response.status_code == 200

def test_teacher_access(client):
    """Test d'accès à une route réservée aux enseignants."""
    client.post('/auth/login', json={"id": "teacher1", "password": "teacherpass"})
    response = client.get('/auth/teacher/protected')
    assert response.status_code == 200

def test_user_forbidden(client):
    """Test qu'un utilisateur standard ne peut pas accéder à une route admin."""
    client.post('/auth/login', json={"id": "user1", "password": "userpass"})
    response = client.get('/auth/admin/protected')
    assert response.status_code == 403


def test_get_users(client):
    response = client.get("/auth/users")
    assert response.status_code == 200
    assert len(response.json) == 3

def test_get_users_by_role(client):
    response = client.get("/auth/users?role=teacher")
    assert response.status_code == 200
    assert len(response.json) == 1

def test_get_user_by_id(client):
    response = client.get("/auth/users/teacher1")
    assert response.status_code == 200
    user = response.json
    assert user['id'] == 'teacher1'

def test_add_user(client):
    data = {"lang":"fr", "password":"test"}
    response = client.post("/auth/users/test1", 
                           data=json.dumps(data), 
                           content_type="application/json")
    
    assert response.status_code == 200
    assert "user added" in response.json["message"]
    user = User.query.filter_by(id='test1').one()
    assert user.lang == "fr"
    assert user.check_password("test")
    
def test_update_user_password(client):
    data = {"password":"test"}
    response = client.put("/auth/users/teacher1", 
                           data=json.dumps(data), 
                           content_type="application/json")
    
    assert response.status_code == 200
    assert "user updated" in response.json["message"]
    user = User.query.filter_by(id='teacher1').one()
    assert user.check_password("test")
    assert user.lang == "fr"

def test_update_user_lang(client):
    data = {"lang":"en"}
    response = client.put("/auth/users/teacher1", 
                           data=json.dumps(data), 
                           content_type="application/json")
    
    assert response.status_code == 200
    assert "user updated" in response.json["message"]
    user = User.query.filter_by(id='teacher1').one()
    assert user.check_password("teacherpass")
    assert user.lang == "en"

def test_delete_user(client):
    response = client.delete("/auth/users/teacher1")
    assert response.status_code == 204
