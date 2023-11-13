import sys
import os
import pytest

# Ajustar sys.path para incluir el directorio que contiene dbmaker.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from data_base.dbmaker import app, db
from data_base.dbmaker import User, Software, Developer, Admin, Report, Comment, Reassignation

@pytest.fixture(scope='function')
def test_app():
    # Configuración de la aplicación para las pruebas
    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///test.db',  # Base de datos de prueba
        'TESTING': True,
    })

    # Asegúrate de utilizar la instancia 'db' que ya importaste
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
