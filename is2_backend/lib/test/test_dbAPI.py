import pytest
from flask import Flask
from api.dbAPI import app
from api.dbAPI import *
from data_base.dbmaker import *

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

def test_create_software(client):
    data = {
        "name": "Postman"
    }
    response = client.post("/software", json=data)
    returned = response.get_json()
    assert returned['message'] == "Software creado"
    assert response.status_code == 200

def test_create_report(client):
    user = client.get("/users/esteban21312312321@example.com")
    returned = user.get_json()
    returned_id = returned['id']
    returned_name = returned['name']

    data = {
        "title" : "No pasan mis test",        
        "description" : "Los test no estan pasando",
        "user_id" : returned_id,
        "user_name" : returned_name,
        "user_email" : "esteban21312312321@example.com",
        "dev_id" : None,
        "dev_name" : None,
        "dev_email" : None,    
        "software_name" : "Postman",
        "urgency" : 1,
        "status" : "ToDo"
    }

    response = client.post("/reports", json = data)
    assert response.status_code == 200
    returned = response.get_json()
    assert returned['message'] == "Reporte creado"

#Test para incluir un comentario en un reporte
def test_post_comment(client):
    user = client.get("/users/esteban21312312321@example.com")
    returned = user.get_json()
    returned_id = returned['id']
    returned_name = returned['name']
    data = {
        "content" : "Estoy creando un comentario en mi reporte",
        "report_id" : 1,
        "commenter_id" : returned_id,
        "commenter_name" : returned_name
    }
    response = client.post("/comments", json=data)
    assert response.status_code == 200
    returned = response.get_json()
    assert returned['message'] == "Comentario creado"

#Test para recuperar el comentario ingresado
def test_get_comment_from_report(client):
    user = client.get("/users/esteban21312312321@example.com")
    returned = user.get_json()
    returned_id = returned['id']
    returned_name = returned['name']
    
    response = client.get("/comments_in/1")
    assert response.status_code == 200
    returned = response.get_json()
    assert returned[0]['commenter_id'] == returned_id
    assert returned[0]['commenter_name'] == returned_name
    assert returned[0]['content'] == "Estoy creando un comentario en mi reporte"
    
def test_assign_dev_to_software(client):
    #Se crea un dev
    dev_data = {
        "name":"soydev",
        "email":"soydev@soydev.cl",
        "password":"123"
    }
    dev = client.post("/devs",json = dev_data)
    #assert dev.status_code == 200
    #se crea un software
    software_data = {
        "name":"Flask"
    }
    sof = client.post("/software",json=software_data)
    assert sof.status_code == 200
    #Se asigna al software de Flask creado anteriormente
    sof_dev_data = {
        "id":"2",
        "email":"soydev@soydev.cl"
    }
    sof_append = client.put("/software/append",json = sof_dev_data)
    returned = sof_append.get_json()
    assert returned['software'] == "Flask"
    assert returned['developer'] == "soydev"
