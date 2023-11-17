import pytest
from pytest_bdd import scenario, given, when, then
from data_base.dbmaker import app, db
from api.dbAPI import User

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

@scenario('features/registration_without_name.feature', 'Intento de registro sin nombre')
def test_registration_without_name():
    pass

@pytest.fixture
def incomplete_user_credentials():
    return {'email': 'nuevo@test.com', 'password': 'nuevaclave123'}

@given('Quiero registrarme como nuevo usuario')
def new_user_intent():
    pass

@given('No ingreso mi nombre')
def no_name():
    pass

@pytest.fixture
@when('Intento registrarme')
def attempt_to_register(test_client, incomplete_user_credentials):
    return test_client.post('/register', json=incomplete_user_credentials)

@then('Recibo un mensaje de error indicando que todo los parámetros son obligatorios')
def registration_error_message(attempt_to_register):
    assert 'error' in attempt_to_register.get_json()
    assert attempt_to_register.get_json()['error'] == 'Parámetros faltantes'