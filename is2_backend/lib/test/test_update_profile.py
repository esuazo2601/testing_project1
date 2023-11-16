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
def laura_credentials():
    return {'email': 'laura@example.com', 'password': 'password123'}

@pytest.fixture
def registered_laura(test_app, laura_credentials):
    with test_app.app_context():
        hashed_password = generate_password_hash(laura_credentials['password']).decode('utf-8')
        laura = User(name='Laura', email=laura_credentials['email'], password=hashed_password, type_of_user='user')
        db.session.add(laura)
        db.session.commit()

@scenario('features/update_profile.feature', 'Un usuario actualiza su perfil')
def test_update_profile():
    pass

@pytest.fixture
@given("Soy el usuario 'Laura' y he iniciado sesión")
def laura_logged_in(test_client, registered_laura, laura_credentials):
    response = test_client.post('/login', json=laura_credentials)
    assert response.status_code == 200
    return response

@when("Actualizo mi perfil con un nuevo nombre 'Laura Cid' y cambio mi dirección de correo a 'lauracid@example.com'")
def update_profile(test_client):
    update_data = {'name': 'Laura Cid', 'email': 'lauracid@example.com'}
    response = test_client.put('/users/laura@example.com', json=update_data)
    assert response.status_code == 200
    return response

@then("Mi perfil se actualiza correctamente con el nuevo nombre y correo")
def profile_updated(test_client):
    response = test_client.get('/users/lauracid@example.com')
    assert response.status_code == 200
    user_data = response.get_json()
    assert user_data['name'] == 'Laura Cid'
    assert user_data['email'] == 'lauracid@example.com'