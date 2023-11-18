import pytest
from pytest_bdd import scenario, given, when, then
from data_base.dbmaker import app, db
from api.dbAPI import User, Developer, Report, Software
from flask_bcrypt import generate_password_hash

class ResponseStorage:
    response = None

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
    return {'email': 'user@test.com', 'password': 'password123'}

@pytest.fixture
def registered_user(test_app, user_credentials):
    with test_app.app_context():
        hashed_password = generate_password_hash(user_credentials['password']).decode('utf-8')
        user = User(name='Test User', email=user_credentials['email'], password=hashed_password, type_of_user='user')
        db.session.add(user)
        db.session.commit()
        db.session.refresh(user)  
        return user

@pytest.fixture
def developer_credentials():
    return {'email': 'developer@test.com', 'password': 'secure123'}

@pytest.fixture
def registered_developer(test_app, developer_credentials):
    with test_app.app_context():
        hashed_password = generate_password_hash(developer_credentials['password']).decode('utf-8')
        developer = Developer(name='Test Developer', email=developer_credentials['email'], password=hashed_password, type_of_user='developer')
        db.session.add(developer)
        db.session.commit()
        db.session.refresh(developer) 
        return developer
    
@pytest.fixture
def assign_developer(test_client, registered_developer):
    with test_app.app_context():
        software = Software.query.first()
        data = {
            "software_id": software.id,
            "developer_id": registered_developer.id
        }
        response = test_client.post('/software_dev/associate', json=data)
        assert response.status_code == 200
        return response

@pytest.fixture
def new_report(test_app, test_client, registered_user, registered_developer):
    with test_app.app_context():
        report_data = {
            'title': 'Reporte',
            'description': 'Descripción',
            'user_id': registered_user.id,
            'user_name': registered_user.name,
            'user_email': registered_user.email,
            'dev_id': registered_developer.id,
            'dev_name': registered_developer.name,
            'dev_email': registered_developer.email,
            'software_name': 'Test Software',  
            'urgency': 1,
            'status': 'ToDo'
        }

        response = test_client.post('/reports', json=report_data)
        assert response.status_code == 200

        report_id = response.get_json()['id']
        report = Report.query.get(report_id)
        return report

@scenario('features/reassign_report.feature', 'Un desarrollador solicita la reasignación de un reporte')
def test_reassign_report():
    pass

@pytest.fixture
@given("Un desarrollador con un reporte asignado")
def report_assigned(test_app, registered_developer, new_report):
    return new_report

@when("El desarrollador solicita la reasignación del reporte")
def request_reassignation(test_client, report_assigned, registered_developer):
    reassignation_data = {
        'report_id': report_assigned.id,
        'content': 'Solicito reasignación',
        'dev_id': registered_developer.id,
        'dev_name': registered_developer.name,
        'dev_email': registered_developer.email,
    }
    response = test_client.post('/reassignations', json=reassignation_data)
    assert response.status_code == 200
    ResponseStorage.response = response  

@then("La reasignación se crea correctamente")
def reassignation_created():
    reassignation_response_data = ResponseStorage.response.get_json()
    assert reassignation_response_data['message'] == 'Reasignación creada'