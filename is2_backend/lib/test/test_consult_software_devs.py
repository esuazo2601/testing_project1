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
def setup_environment(test_app, test_client):
    with test_app.app_context():
        hashed_password = generate_password_hash('password123').decode('utf-8')
        devs = [
            Developer(name='Desarrollador 1', email='dev1@ejemplo.com', password=hashed_password, type_of_user='developer'),
            Developer(name='Desarrollador 2', email='dev2@ejemplo.com', password=hashed_password, type_of_user='developer'),
            Developer(name='Desarrollador 3', email='dev3@ejemplo.com', password=hashed_password, type_of_user='developer')
        ]
        db.session.add_all(devs)
        db.session.commit()

        softwares = [
            Software(name="Software A"),
            Software(name="Software B"),
            Software(name="Software C"),
            Software(name="Software D")
        ]
        db.session.add_all(softwares)
        db.session.commit()

        # Desarrollador 1 asignado a los softwares A, B, y C
        for software in softwares[:3]:
            asignar_desarrollador_a_software(test_client, software.id, devs[0].id)

        # Desarrollador 2 asignado a los softwares B y C
        for software in softwares[1:3]:
            asignar_desarrollador_a_software(test_client, software.id, devs[1].id)

        # Desarrollador 3 asignado a los softwares C y D
        for software in softwares[2:]:
            asignar_desarrollador_a_software(test_client, software.id, devs[2].id)

def asignar_desarrollador_a_software(test_client, software_id, developer_id):
    data = {
        "software_id": software_id,
        "developer_id": developer_id
    }
    response = test_client.post('/software_dev/associate', json=data)
    assert response.status_code == 200


@scenario('features/consult_software_devs.feature', 'Un administrador consulta en qué softwares están trabajando los desarrolladores')
def test_software_dev_assignments():
    pass


@given("existen tres desarrolladores: Desarrollador 1, Desarrollador 2, Desarrollador 3")
def three_developers(setup_environment):
    # Listo en setup_environment
    pass


@given("existen cuatro softwares: Software A, Software B, Software C, Software D")
def four_softwares(setup_environment):
    # Listo en setup_environment
    pass


@given("cada desarrollador está asignado a dos softwares, y uno de ellos está asignado a tres")
def developers_assigned_to_softwares(setup_environment):
    # Listo en setup_environment
    pass


@pytest.fixture
@when("el administrador solicita la lista de asignaciones de software a desarrolladores")
def admin_requests_assignments(test_client):
    response = test_client.get('/software_dev_names')
    assert response.status_code == 200
    return response.get_json()

@then("se muestra correctamente en qué softwares está trabajando cada desarrollador")
def check_assignments(admin_requests_assignments):
    # Asignaciones esperadas
    expected_assignments = {
        "Desarrollador 1": ["Software A", "Software B", "Software C"],
        "Desarrollador 2": ["Software B", "Software C"],
        "Desarrollador 3": ["Software C", "Software D"]
    }

    # Crear un diccionario para rastrear las asignaciones actuales
    actual_assignments = {dev_name: [] for dev_name in expected_assignments.keys()}
    for entry in admin_requests_assignments['software_dev']:
        actual_assignments[entry['developer_name']].append(entry['software_name'])

    # Verificar que cada desarrollador esté asignado a los softwares correctos
    for dev, softwares in expected_assignments.items():
        assert dev in actual_assignments, f"Desarrollador {dev} no encontrado en las asignaciones."
        assert sorted(actual_assignments[dev]) == sorted(softwares), f"Asignaciones incorrectas para {dev}. Esperado: {softwares}, Obtenido: {actual_assignments[dev]}"