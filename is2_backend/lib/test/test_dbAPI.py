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
    assert response.status_code == 200

    # Verifica que la respuesta tenga el formato JSON esperado
    data = response.get_json()
    
    # Accede al primer elemento de la lista y verifica si 'name' está en ese diccionario
    assert data["name"] == "Estebandidox"
    assert data["password"] == "password123"
    assert data["email"] == "esteban21312312321@example.com"

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
    assert response.status_code == 200

    # Verifica que la respuesta contenga un mensaje de error
    data = response.get_json()
    assert "error" in data
    assert data["error"] == "Parámetros faltantes"
