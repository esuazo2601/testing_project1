import sys
import os

# Ajustar sys.path para incluir el directorio que contiene dbmaker.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../../')))

from data_base.dbmaker import User, db
from pytest_bdd import scenario, given, when, then

@scenario('../login.feature', 'Inicio sesion')
def test_login():
    pass

@given("Soy un usuario registrado")
def registered_user(test_app):
    with test_app.app_context():
        user = User(name='Prueba', email='prueba@test.com', password='secreto', type_of_user='some_type')
        db.session.add(user)
        db.session.commit()

@given("Tengo mis credenciales de usuario")
def credentials():
    return {'email': 'prueba@test.com', 'password': 'secreto'}

@when("Ingreso mis datos")
def login(test_client, user_credentials):
    response = test_client.post('/login', data=user_credentials)
    return response

@then("Se crea una cookie de sesion")
def session_cookie(response):
    assert 'session' in response.headers.get('Set-Cookie')

@then("Puedo acceder a mis bug reports")
def access_bug_reports(response):
    assert 'Mis Reportes de Bugs' in response.data