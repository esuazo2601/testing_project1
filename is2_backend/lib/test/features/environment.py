import sys
import os
import pytest

# Ajustar sys.path para incluir el directorio que contiene dbmaker.py
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../')))

from data_base.dbmaker import app, db
from data_base.dbmaker import User, Software, Developer, Admin, Report, Comment, Reassignation

def before_all(context):
    print("Running before_all hook in environment.py")

    app.config.update({
        'SQLALCHEMY_DATABASE_URI': 'sqlite:///example.db',
        'TESTING': True,
        'SESSION_COOKIE_DOMAIN': 'localhost',
        'SESSION_COOKIE_PATH': '/'
    })

    with app.app_context():
        db.create_all()
        context.test_app = app
        context.db = db

def after_all(context):
    with context.test_app.app_context():
        context.db.session.remove()
        context.db.drop_all()  # Limpiar la base de datos después de las pruebas

def before_scenario(context, scenario):
    context.test_client = context.test_app.test_client()

def after_scenario(context, scenario):
    with context.test_app.app_context():
        context.db.session.remove()
        context.db.drop_all()  # Limpiar la base de datos después de cada escenario