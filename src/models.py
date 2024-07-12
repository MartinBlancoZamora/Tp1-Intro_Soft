import datetime
from flask_sqlalchemy import SQLAlchemy

database = SQLAlchemy()

class Usuarios(database.Model):
    __tablename__ = 'usuarios'
    nombre_usuario = database.Column(database.String(255), nullable = False)
    id_usuario = database.Column(database.integer, primary_key = True)
    contraseña = database.Column(database.String(255), nullable = False)
    mail = database.Column(database.String(255), nullable = False)

class Materias(database.Model):
    __tablename__ = 'materias'
    nombre_materias = database.Column(database.String(255), nullable = False)
    id_materia = database.Column(database.integer, primary_key = True)
    horario = database.Column(database.DateTime, nullable = True)
    calificaciones = database.Column(database.String(255), nullable = True)
    id_creador = database.Column(database.interger, database.ForeignKey['id_usuario'])
                           
class Eventos(database.Model):
    __tablename__ = 'eventos'
    nombre_evento = database.Column(database.String(255), nullable = False)
    id_evento = database.Column(database.integer, primary_key = True)
    fecha = database.Column(database.DateTime, nullable = False)
    descripcion_evento = database.Column(database.String(255), nullable = True)
    id_foraneo = database.Column(database.integer, database.ForeignKey['id_materia'], nullable = False)

class Tareas(database.Model):
    __tablename__ = 'tareas'
    nombre_tarea = database.Column(database.String(255), nullable = False)
    id_tarea = database.Column(database.interger, primary_key = True)
    fecha_limite = database.Column(database.DateTime, nullable = True)
    descripcion_tarea = database.Column(database.String(255), nullable = True)
    id_relacion = database.Column(database.interger, database.ForeignKey['id_materia'], nullable = True)