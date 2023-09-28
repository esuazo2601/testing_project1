import pytest
from flask import jsonify
from api.dbAPI import app

@pytest.fixture
def client():
    # Crea un cliente de prueba para realizar solicitudes HTTP
    with app.test_client() as client:
        yield client

def test_register_user_valid(client):
    # Define los datos de prueba para el registro
    data = {
        "name": "Estebandidox",
        "email": "esteban21312312321@example.com",
        "password": "password123"
    }

    # Realiza una solicitud POST a la ruta /register con los datos de prueba
    response = client.post('/register', json=data)

    # Verifica que la respuesta tenga un código de estado 200

    # Verifica que la respuesta tenga el formato JSON esperado
    returned = response.get_json()

    # Verifica que los datos en el diccionario sean correctos
    assert "name" in returned
    assert returned["name"]== "Estebandidox"
    assert "email" in returned
    assert returned["email"] == "esteban21312312321@example.com"
    assert response.status_code == 200

def test_register_user_missing_parameters(client):
    # Define datos de prueba con parámetros faltantes
    data = {
        "name": "",
        "email": "esteban@example.com",
        "password": ""
    }

    # Realiza una solicitud POST a la ruta /register con datos de prueba inválidos
    response = client.post('/register', json=data)

    # Verifica que la respuesta tenga un código de estado 200 (porque es un error lógico en la aplicación)
    assert response.status_code == 400

    # Verifica que la respuesta contenga un mensaje de error
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Parámetros faltantes"
