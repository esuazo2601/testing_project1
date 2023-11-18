import pytest
from pytest_bdd import scenario, given, when, then
from data_base.dbmaker import db, app
from api.dbAPI import Software, Developer
from flask_bcrypt import generate_password_hash


@pytest.fixture
def test_app():
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    with app.app_context():
        db.create_all()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture
def felipe_credentials():
    return {'email': 'felipe@ejemplo.com', 'password': 'password123'}

@pytest.fixture
def registered_felipe(test_app, felipe_credentials):
    with test_app.app_context():
        hashed_password = generate_password_hash(felipe_credentials['password']).decode('utf-8')
        felipe = Developer(name='Felipe', email=felipe_credentials['email'], password=hashed_password, type_of_user='developer')
        db.session.add(felipe)
        db.session.commit()
        return felipe.id
    


@scenario('features/assign_developer.feature', 'Un administrador asigna un desarrollador a un software')
def test_assign_developer():
    pass


@pytest.fixture
@given('existe un software llamado "Software de prueba"')
def software_existente(test_app):
    with test_app.app_context():
        software = Software(name="Software de prueba")
        db.session.add(software)
        db.session.commit()
        return software.id

@pytest.fixture
@given('existe un desarrollador llamado Felipe')
def desarrollador_existente(registered_felipe):
    return registered_felipe


@pytest.fixture
@when('el administrador asigna a Felipe al "Software de prueba"')
def asignar_desarrollador(test_client, software_existente, desarrollador_existente):
    data = {
        "software_id": software_existente,
        "developer_id": desarrollador_existente
    }
    response = test_client.post('/software_dev/associate', json=data)
    assert response.status_code == 200
    return response
    
@then('se confirma que Felipe ha sido asignado correctamente al "Software de prueba"')
def confirmar_asignacion(test_client, asignar_desarrollador):
    response = asignar_desarrollador
    returned_text = response.data.decode('utf-8') 

    assert returned_text == 'Developer associated with software successfully.'