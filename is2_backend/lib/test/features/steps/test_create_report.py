import sys
import os

# Ajustar sys.path para incluir el directorio que contiene dbmaker.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from data_base.dbmaker import User, db
from behave import given, when, then

@given("Que existe un software")
def create_software(context):
    with context.test_app.app_context():
        software_data = {'name': 'Softwarecito'}
        context.response = context.test_client.post('/create_software', json=software_data)


@given("Soy un usuario registrado en la base de datos")
def register_user(context):
    with context.test_app.app_context():
        user = User(name='UsuarioPrueba', email='usuario@test.com', password='secreto', type_of_user='User')
        db.session.add(user)
        db.session.commit()

@given("El software existe en la base de datos")
def check_software_exists(context):
    with context.test_app.app_context():
        context.response = context.test_client.get('/software/1')
        context.json_data = context.response.get_json()
        assert context.json_data[1] == 'Softwarecito' 
    

@when("Intento crear un reporte")
def create_report(context):
    # Assuming you have a route for creating a report, you can use the test client to send a request
    title = 'reporte'
    description = 'estoy reportando'
    user_name = "UsuarioPrueba"
    user_email = "usuario@test.com"

    context.response = context.test_client.get(f'/users/{user_email}')
    user_id = context.response.get_json()['id']
    
    software_name = 'Softwarecito'
    urgency = 1
    status = "ToDo"
    data = {'title': title, 'description':description, "user_id":user_id, "user_name":user_name, "user_email":user_email, "dev_id":None, "dev_name":None,"dev_email":None, "software_name":software_name, "urgency":urgency, "status":status}

    context.response = context.test_client.post('/create_report', json=data)

@then("Se crea un reporte asociado a ese software")
def check_report_created(context):
    context.response = context.test_client.get('/software_report/1')
    assert context.response.get_json()['report_list'][0]['title'] == 'reporte'