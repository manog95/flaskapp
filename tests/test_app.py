import pytest
from app import app, db, User

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF for testing convenience
    
    with app.test_client() as client:
        with app.app_context():
            db.create_all()
            yield client
            db.session.remove()
            db.drop_all()

def test_home_page(client):
    """Test that the home page loads successfully."""
    response = client.get('/home')
    assert response.status_code == 200
    assert b"Welcome" in response.data or b"Home" in response.data

def test_login_page_loads(client):
    """Test that the login page loads."""
    response = client.get('/login')
    assert response.status_code == 200
    assert b"Login" in response.data

def test_register_page_loads(client):
    """Test that the register page loads."""
    response = client.get('/register')
    assert response.status_code == 200
    assert b"Register" in response.data

def test_404_page(client):
    """Test that a non-existent route returns 404."""
    response = client.get('/non_existent_route')
    assert response.status_code == 404
