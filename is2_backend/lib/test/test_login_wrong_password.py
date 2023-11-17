import pytest
from pytest_bdd import scenario, given, when, then
from data_base.dbmaker import app, db  
from api.dbAPI import User  
from flask_bcrypt import generate_password_hash

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

@scenario('features/login_wrong_password.feature', 'Intento de inicio de sesión con contraseña dudosa')
def test_login_with_doubtful_password():
    pass

@pytest.fixture
def user_credentials():
    return {'email': 'usuario@test.com', 'password': 'contraseñasegura123'}

@given('Tengo mis credenciales de usuario')
def user_credentials_ready(user_credentials):
    pass

@given('Soy un usuario registrado')
def registered_user(user_credentials, test_app):
    with test_app.app_context():
        hashed_password = generate_password_hash(user_credentials['password']).decode('utf-8')
        user = User(
            name='Nombre de Usuario',
            email=user_credentials['email'],
            password=hashed_password,
            type_of_user='user'
        )
        db.session.add(user)
        db.session.commit()

@pytest.fixture
@when('Intento iniciar sesión con una contraseña que no recuerdo bien')
def attempt_to_login(test_client, user_credentials):
    wrong_password_credentials = {'email': user_credentials['email'], 'password': 'contraseñaErronea'}
    return test_client.post('/login', json=wrong_password_credentials)

@then('Se muestra un error de "Contraseña incorrecta"')
def incorrect_password_error_message(attempt_to_login):
    assert 'error' in attempt_to_login.get_json()
    assert attempt_to_login.get_json()['error'] == 'Contraseña incorrecta'