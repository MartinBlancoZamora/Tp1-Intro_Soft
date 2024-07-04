from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
from models import db, User
from config import Config
import os

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)
CORS(app)

@app.before_first_request
def create_tables():
    db.create_all()
    
@app.route('/users', methods=['GET'])
def get_users():
    users = User.query.all()
    return jsonify([user.as_dict() for user in users])

@app.route('/user', methods=['POST'])
def add_user():
    data = request.json
    new_user = User(
        nombre_usuario=data['nombre_usuario'],
        contraseña=data['contraseña'],
        mail=data['mail']
    )
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.as_dict()), 201

@app.route('/login', methods=['POST'])
def login():
    data = request.json
    identifier = data.get('identifier')
    password = data.get('password')
    
    user = User.query.filter((User.nombre_usuario == identifier) | (User.mail == identifier)).first()
    
    if user and user.contraseña == password:
        return jsonify(user.as_dict()), 200
    else:
        return jsonify({"error": "Invalid username/email or password"}), 401

# Rutas de las paginas html
@app.route('/login.html')
def serve_login():
    return send_from_directory(os.path.join(app.root_path, 'frontend/login_signup'), 'login.html')

@app.route('/signup.html')
def serve_signup():
    return send_from_directory(os.path.join(app.root_path, 'frontend/login_signup'), 'signup.html')

@app.route('/index.html')
def serve_index():
    return send_from_directory(os.path.join(app.root_path, 'frontend'), 'index.html')

if __name__ == '__main__':
    app.run(debug=True)