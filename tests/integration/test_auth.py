
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