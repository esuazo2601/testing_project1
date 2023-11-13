# conftest.py
import sys
import os

import pytest
# Agregar el directorio raíz del proyecto al sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from lib.data_base.dbmaker import app, db  # Importar la aplicación y base de datos
from lib.data_base.dbmaker import User, Software, Developer, Admin, Report, Comment, Reassignation

# Importar los modelos que necesitas

@pytest.fixture(scope='function')
def test_app():
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',  # Usar una base de datos de prueba
        'TESTING': True,
    })
    db = SQLAlchemy(app)

    with app.app_context():
        db.create_all()  # Crear todas las tablas para la prueba
        yield app  # Esto permite usar la aplicación en el contexto de la prueba
        db.session.remove()
        db.drop_all()  # Limpiar la base de datos después de las pruebas

@pytest.fixture(scope='function')
def test_client(test_app):
    with test_app.test_client() as testing_client:
        with test_app.app_context():
            yield testing_client  # Esto proporciona un cliente de prueba para las pruebas
