from pytest_bdd import scenario,given,when,then
from ..data_base.dbmaker import User

@scenario('login.feature', 'Inicio sesion')
def test_login():
    pass

@given("Soy un usuario registrado")
def registered_user(test_app):
    with test_app.app_context():
        user = User(name='Prueba', email='prueba@test.com', password='secreto')
        db.session.add(user)
        db.session.commit()

@given("Me sé mis datos para inciar sesión")
def user_credentials():
    return {'email': 'prueba@test.com', 'password': 'secreto'}

@when("Ingreso mis datos")
def login(test_client, user_credentials):
    return test_client.post('/login', data=user_credentials)

@then("Se crea una cookie de sesion")
def session_cookie(response):
    assert 'session' in response.headers.get('Set-Cookie')

@then("Puedo acceder a mis bug reports")
def access_bug_reports(response):
    # Verificar si la respuesta indica que el usuario puede acceder a sus bug reports
    assert 'Mis Reportes de Bugs' in response.data