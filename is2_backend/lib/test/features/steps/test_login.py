import sys
import os

# Ajustar sys.path para incluir el directorio que contiene dbmaker.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from data_base.dbmaker import User, db
import pytest
from pytest_bdd import scenario, given, when, then

@scenario('../login.feature', 'Inicio sesion')
def test_login():
    pass

@given("Puedo crear una cuenta")
def registered_user(test_app):
    with test_app.app_context():
        user = User(name='Prueba', email='prueba@test.com', password='secreto', type_of_user='some_type')
        db.session.add(user)
        db.session.commit()

@given("Me sé mis datos para inciar sesión")
def credentials():
    return {'email': 'prueba@test.com', 'password': 'secreto'}

@when("Ingreso mis datos")
def login(test_client):
    response = test_client.post('/login', data=credentials())
    return response

@pytest.fixture
@then("Se crea una cookie de sesion")
def session_cookie(test_client):
    response = test_client.get('/@me')
    
    # Verificar que la solicitud fue exitosa
    assert response.status_code == 200
    
    # Verificar que la respuesta contiene datos JSON
    assert response.is_json
    
    response_data = response.get_json()
    print(response_data)
    
    # Asegurarse de que la clave 'message' está presente en la respuesta JSON
    assert 'message' in response_data
    assert response_data['message'] == 'Hay cookies presentes'
