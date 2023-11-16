import pytest
from pytest_bdd import scenario, given, when, then
from data_base.dbmaker import app, db  
from api.dbAPI import User  
from flask_bcrypt import generate_password_hash

# Configuración para realizar la prueba 
@pytest.fixture
def test_app():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'  
    })
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

# Fixture para las credenciales del usuario
@pytest.fixture
def user_credentials():
    return {'email': 'prueba@test.com', 'password': 'secreto123'}

# Fixture para crear un usuario en la base de datos
@pytest.fixture
def registered_user(test_app, user_credentials):
    with test_app.app_context():
        hashed_password = generate_password_hash(user_credentials['password']).decode('utf-8')
        user = User(name='Test User', email=user_credentials['email'], password=hashed_password, type_of_user='user')
        db.session.add(user)
        db.session.commit()

@scenario('features/login.feature', 'Inicio sesion')
def test_login():
    pass

@given('Tengo mis credenciales de usuario')
def credentials(user_credentials):
    return user_credentials

@given('Soy un usuario registrado')
def user_registered(registered_user):
    pass

@pytest.fixture
@when('Ingreso mis datos')
def login_response(test_client, user_credentials):
    response = test_client.post('/login', json=user_credentials)
    return response

@then('Se crea una cookie de sesión')
def session_cookie(login_response):
    assert 'set-cookie' in login_response.headers

@then('Puedo acceder a mis bug reports')
def access_bug_reports(test_client, user_credentials):
    response = test_client.get(f"/user_reports/{user_credentials['email']}")
    assert response.status_code == 200
    reports = response.get_json()
    assert isinstance(reports, list)  