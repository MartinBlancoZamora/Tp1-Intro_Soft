from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash

database = SQLAlchemy()

class Usuarios(database.Model):
    __tablename__ = 'usuarios'
    id = database.Column(database.Integer, primary_key=True)
    nombre_usuario = database.Column(database.String(80), unique=True, nullable=False)
    contraseña = database.Column(database.String(200), nullable=False)
    mail = database.Column(database.String(120), unique=True, nullable=False)
    materias = database.relationship('Materias', backref='usuario', lazy=True)


class Materias(database.Model):
    __tablename__ = 'materias'
    id = database.Column(database.Integer, primary_key=True)
    nombre = database.Column(database.String(80), nullable=False)
    horario = database.Column(database.String(80), nullable=True)
    calificaciones = database.Column(database.String(80), nullable=True)
    usuario_id = database.Column(database.Integer, database.ForeignKey('usuarios.id'), nullable=False)
    tareas = database.relationship('Tareas', backref='materia', lazy=True)
    eventos = database.relationship('Eventos', backref='materia', lazy=True)


class Tareas(database.Model):
    __tablename__ = 'tareas'
    id = database.Column(database.Integer, primary_key=True)
    nombre = database.Column(database.String(80), nullable=False)
    fecha_limite = database.Column(database.String(255), nullable=False)
    descripcion = database.Column(database.String(200), nullable=True)
    materia_id = database.Column(database.Integer, database.ForeignKey('materias.id'), nullable=True)


class Eventos(database.Model):
    __tablename__ = 'eventos'
    id = database.Column(database.Integer, primary_key=True)
    nombre = database.Column(database.String(80), nullable=False)
    fecha_limite = database.Column(database.String(255), nullable=False)
    descripcion = database.Column(database.String(200), nullable=True)
    materia_id = database.Column(database.Integer, database.ForeignKey('materias.id'), nullable=False)