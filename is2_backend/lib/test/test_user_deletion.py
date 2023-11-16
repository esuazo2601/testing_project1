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

@pytest.fixture
def carlos_credentials():
    return {'email': 'carlos@test.com', 'password': 'password123'}

@pytest.fixture
def registered_carlos(test_app, carlos_credentials):
    with test_app.app_context():
        hashed_password = generate_password_hash(carlos_credentials['password']).decode('utf-8')
        carlos = User(name='Carlos', email=carlos_credentials['email'], password=hashed_password, type_of_user='user')
        db.session.add(carlos)
        db.session.commit()

@scenario('features/user_deletion.feature', 'Un usuario elimina su cuenta')
def test_user_deletion():
    pass

@pytest.fixture
@given("Soy el usuario 'Carlos' y he iniciado sesión")
def carlos_logged_in(test_client, registered_carlos, carlos_credentials):
    response = test_client.post('/login', json=carlos_credentials)
    assert response.status_code == 200
    return response

@when("Elijo eliminar mi cuenta")
def delete_account(test_client, carlos_credentials):
    response = test_client.delete(f"/users/{carlos_credentials['email']}")
    assert response.status_code == 200
    return response

@then("Mi cuenta se elimina correctamente y ya no puedo iniciar sesión")
def account_deleted(test_client, carlos_credentials):
    login_response = test_client.post('/login', json=carlos_credentials)
    assert login_response.status_code == 401  