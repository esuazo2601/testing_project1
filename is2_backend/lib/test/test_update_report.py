import pytest
from pytest_bdd import scenario, given, when, then
from data_base.dbmaker import app, db
from api.dbAPI import User, Report, Software
from flask_bcrypt import generate_password_hash

@pytest.fixture
def test_app():
    app.config.update({
        'TESTING': True,
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///:memory:'
    })
    with app.app_context():
        db.create_all()
        test_software = Software(name='Test Software')
        db.session.add(test_software)
        db.session.commit()
    yield app
    with app.app_context():
        db.drop_all()

@pytest.fixture
def test_client(test_app):
    return test_app.test_client()

@pytest.fixture
def user_credentials():
    return {'email': 'usuario@test.com', 'password': 'secreto123'}

@pytest.fixture
def registered_user(test_app, user_credentials):
    with test_app.app_context():
        hashed_password = generate_password_hash(user_credentials['password']).decode('utf-8')
        user = User(name='Test User', email=user_credentials['email'], password=hashed_password, type_of_user='user')
        db.session.add(user)
        db.session.commit()
        return user.id, user.name, user.email

@pytest.fixture
def new_report(test_app, registered_user):
    user_id, _, _ = registered_user
    with test_app.app_context():
        software = Software.query.first()
        report = Report(title="Reporte Original", description="Descripción Original", user_id=user_id, software_name=software.name)
        db.session.add(report)
        db.session.commit()
        return report.id

@scenario('features/update_report.feature', 'Un usuario crea y luego actualiza la información de un reporte')
def test_update_report():
    pass

@pytest.fixture
@given("Soy un usuario registrado y he iniciado sesión")
def user_logged_in(test_client, registered_user, user_credentials):
    response = test_client.post('/login', json=user_credentials)
    assert response.status_code == 200
    user_data = response.get_json()
    return user_data['id']  

@pytest.fixture
@given("He creado un nuevo reporte")
def report_created(test_app, registered_user, new_report):
    return new_report

@when("Actualizo el título y la descripción de mi reporte")
def update_report(test_client, new_report, user_logged_in):
    update_data = {
        'title': 'Nuevo Título',
        'description': 'Nueva Descripción',
        'user_id': user_logged_in, 
        'user_name': 'Test User',
        'user_email': 'usuario@test.com',
        "dev_id": None,
        "dev_name": None,
        "dev_email": None,
        "software": "Test Software",
        "software": 1,
        "urgency": 1,
        "status": "ToDo"
    }
    response = test_client.put(f'/reports/{new_report}', json=update_data)
    assert response.status_code == 200
    assert response.status_code == 200
    returned = response.get_json()
    assert returned["message"] == "Reporte actualizado"

@then("El reporte se actualiza correctamente con el nuevo título y descripción")
def report_updated(test_client, new_report):
    response = test_client.get(f'/reports/{new_report}')
    assert response.status_code == 200
    report_data = response.get_json()['report']  
    assert report_data['title'] == 'Nuevo Título'  
    assert report_data['description'] == 'Nueva Descripción' 