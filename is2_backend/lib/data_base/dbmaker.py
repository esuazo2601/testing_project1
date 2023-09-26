import os
import sys
from datetime import datetime
from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy
from dataclasses import dataclass
from config import ApplicationConfig
from uuid import uuid4

def get_uuid():
    return uuid4().hex

sys.path.append(os.path.abspath(
    os.path.join(os.path.dirname(__file__), '../api')))


app = Flask(__name__)
app.config.from_object(ApplicationConfig)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

@dataclass
class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.String(32), primary_key=True, default=get_uuid)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.Text, nullable=False)
    reports = db.relationship('Report', backref='user')
    notifications = db.relationship('Notification', backref='user', primaryjoin='User.id == Notification.user_id')
    type_of_user = db.Column('type', db.String(20), default=lambda: User.__table__.name)
    
    def __init__(self, name, email, password, type_of_user):
        self.name = name
        self.email = email
        self.password = password
        self.type_of_user = type_of_user
    
    @property
    def notification_counter(self):
        return len(self.notifications)


software_dev = db.Table('software_dev',
                    db.Column('software_id', db.String(32), db.ForeignKey('software.id')),
                    db.Column('dev_id', db.String(32), db.ForeignKey('developer.id'))
                    )

class Software (db.Model):
    __tablename__ = ('software')
    id = db.Column (db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    devs = db.relationship('Developer', secondary = software_dev, backref='software')

class Developer(User):
    __tablename__= ('developer')
    id = db.Column (db.String(32), db.ForeignKey('user.id'),primary_key=True, default=get_uuid)
    reports = db.relationship('Report', backref = 'developer')
    __mapper_args__ = { 
        'polymorphic_identity': 'developer'
    }
    def __init__ (self, name, email, password, type_of_user):
        super().__init__(name=name,email=email,password=password,type_of_user=type_of_user)
    
class Admin(User):
    __tablename__ = ('admin')
    id = db.Column(db.String(32), db.ForeignKey('user.id'), primary_key=True, default=get_uuid)
    
    __mapper_args__ = { 
        'polymorphic_identity': 'admin'
    }
    def __init__ (self, name, email, password, type_of_user):
        super().__init__(name=name,email=email,password=password, type_of_user=type_of_user)

class Report (db.Model):
    __tablename__ = ('report')
    id = db.Column (db.Integer, primary_key=True)
    title = db.Column (db.String(80), nullable=False)
    description = db.Column (db.Text, nullable = False)
    date = db.Column (db.DateTime, default=datetime.utcnow)
    user_id = db.Column (db.Integer, db.ForeignKey('user.id'))
    user_name = db.Column(db.String(30))
    user_email = db.Column (db.String(80), nullable=True)
    dev_id = db.Column (db.Integer, db.ForeignKey('developer.id'), nullable=True)
    dev_name = db.Column(db.String(30), nullable=True)
    dev_email = db.Column (db.String(80), nullable=True)
    software = db.Column (db.Integer, db.ForeignKey('software.id'))
    software_name= db.Column(db.String(80))
    urgency = db.Column (db.String(80), nullable=True )
    status = db.Column (db.String(80),nullable=True)
    attachment = db.Column(db.LargeBinary, nullable=True)
    reassign = db.Column(db.Boolean, default=False)

class Comment (db.Model):
    __tablename__ = ('comment')
    id = db.Column (db.Integer, primary_key=True)
    content = db.Column (db.Text, nullable = False)
    date = db.Column (db.DateTime, default=datetime.utcnow)
    report_id = db.Column (db.Integer, db.ForeignKey('report.id'), nullable=False)
    commenter_id = db.Column (db.Integer, db.ForeignKey('user.id'), nullable=False)
    commenter_name = db.Column (db.String(80), db.ForeignKey('user.name'), nullable=False)

class Notification(db.Model):
    __tablename__ = 'notification'
    id = db.Column(db.Integer, primary_key=True)
    content = db.Column(db.Text, nullable=True)
    user_id = db.Column(db.String(32), db.ForeignKey('user.id'), nullable=False)
    user_name = db.Column(db.String(80), db.ForeignKey('user.name'), nullable=False)
    developer_id = db.Column(db.String(32), db.ForeignKey('developer.id'))
    developer_name = db.Column(db.String(32))
    type = db.Column(db.String(20), nullable=False)
    software = db.Column(db.String(30))
    
class Reassignation(db.Model):
    __tablename__ = 'reassignation'
    id = db.Column (db.Integer, primary_key=True)
    content = db.Column (db.Text, nullable=True)
    report_id = db.Column (db.Integer, db.ForeignKey('report.id'), nullable=False)
    dev_id = db.Column (db.String(32), db.ForeignKey('user.id'), nullable=False)
    dev_name = db.Column (db.String(80), db.ForeignKey('user.name'), nullable=False)
    dev_email = db.Column (db.String(80), db.ForeignKey('user.email'), nullable=False)
    date = db.Column (db.DateTime, default=datetime.utcnow)

with app.app_context():
    db.create_all()
    