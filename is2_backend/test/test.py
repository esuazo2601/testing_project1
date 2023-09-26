from flask import Flask, jsonify, request
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///example.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)

    def __repr__(self):
        return '<User %r>' % self.name
    
    
with app.app_context():
    db.create_all()

@app.route('/users', methods=['GET', 'POST'])
def users():
    if request.method == 'GET':
        users = User.query.all()
        return jsonify([user.__dict__ for user in users])
    elif request.method == 'POST':
        name = request.json.get('name')
        email = request.json.get('email')
        user = User(name=name, email=email)
        db.session.add(user)
        db.session.commit()
        return jsonify(user.__dict__)

@app.route('/users/<int:user_id>', methods=['GET', 'PUT', 'DELETE'])
def user(user_id):
    user = User.query.get(user_id)
    if not user:
        return jsonify({'error': 'User not found'}), 404
    if request.method == 'GET':
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    elif request.method == 'PUT':
        name = request.json.get('name')
        email = request.json.get('email')
        user.name = name
        user.email = email
        db.session.commit()
        return jsonify({'id': user.id, 'name': user.name, 'email': user.email})
    elif request.method == 'DELETE':
        db.session.delete(user)
        db.session.commit()
        return '', 204


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run()
