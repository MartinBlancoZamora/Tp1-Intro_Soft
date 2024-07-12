from flask import Flask, render_template, request, redirect, url_for
from models import database, Usuarios, Materias, Eventos, Tareas

app = Flask(__name__)
port = 5000
#app.config["SQLALCHEMY_DATABASE_URI"] = 
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/usuario', methods=['GET'])
def usuario(id):
    try:
        usuario = Usuarios.query.where(Usuarios.id_usuario == id).all()
        usuario_data = {
            'usuario_nombre' : usuario.nombre_usuario,
            'usuario_contraseña' : usuario.contraseña,
            'usuario_mail' : usuario.mail
        }
        return usuario_data, 200
    except Exception:
        return jsonify({"Error" : {"Tipo" : "SERVER ERROR", "Detalles" : "No se encontró el usuario"}}), 500

@app.route('/registro', methods=['POST'])
def registro():
    try:
        data = request.json
        nombre_usuario_nuevo = data.get('usuario_nombre')
        contraseña_nueva = data.get('usuario_contraseña')
        mail_nuevo = data.get('usuario_mail')
        nuevo_usuario = Usuarios(nombre_usuario = nombre_usuario_nuevo, contraseña = contraseña_nueva, mail = mail_nuevo)
        database.session.add(nuevo_usuario)
        database.session.commit()
        return render_template('home.html'), 201
    except Exception:
        print("Debug: Ocurrio un error a la hora de crear un usuario, forzando la finalización del código")
        return jsonify({"Error": {"Tipo" : "SERVER ERROR", "Detalles" : "No se creó el usuario"}}), 500

@app.route('/gestion_materias', methods=['GET', 'POST'])
def gestionmaterias():
    if request.method == 'POST':
        try:
            nombre = request.form['nombreMateria'].strip()
            horario = request.form['horarioMateria'].strip()
            calificaciones = request.form['calificacionesMateria'].strip()
            
            materia = {
                'nombre': nombre,
                'horario': horario,
                'calificaciones': calificaciones,
            }
            materias.append(materia)
        except Exception:
            return jsonify({"Error" : {"Tipo": "", "Detalle": ""}}), 500
    else:
        try:
            return render_template('gestion_materias.html', materias=Materias)
        except Exception: 
            return jsonify({"Error" : {"Tipo": "", "Detalle": ""}}), 500

@app.route('/materia/<nombre>', methods=['GET', 'POST'])
def materia_detail(nombre):
    nombre = nombre.strip()
    materia = next((m for m in materias if m['nombre'] == nombre), None)
    if not materia:
        return 'Materia no encontrada', 404
    
    if request.method == 'POST':
        if 'tarea' in request.form:
            nueva_tarea = {
                'nombre': request.form['tarea'].strip(),
                'descripcion': request.form['descripcion'].strip(),
                'fecha_limite': request.form['fecha_limite'].strip()
            }
            if nueva_tarea['nombre']:
                materia['tareas'].append(nueva_tarea)
        elif 'evento' in request.form:
            nuevo_evento = {
                'nombre': request.form['evento'].strip(),
                'fecha': request.form['fecha_evento'].strip(),
                'descripcion': request.form['descripcion_evento'].strip()
            }
            if nuevo_evento['nombre']:
                materia['eventos'].append(nuevo_evento)
    
    return render_template('materia.html', materia=materia)

@app.route('/materia/<nombre>/eliminar', methods=['POST'])
def eliminar_materia(nombre):
    try:
        nombre = nombre.strip()
        global materias
        materias = [m for m in materias if m['nombre'] != nombre]
        return redirect(url_for('gestionmaterias'))
    except Exception as e:
        app.logger.error(f"Error en eliminar_materia: {e}")
        return "Error interno del servidor", 500

@app.route('/materia/<nombre>/eliminar-tarea/<int:tarea_id>', methods=['POST'])
def eliminar_tarea(nombre, tarea_id):
    nombre = nombre.strip()
    materia = next((m for m in materias if m['nombre'] == nombre), None)
    if not materia:
        return 'Materia no encontrada', 404
    
    if 0 <= tarea_id < len(materia['tareas']):
        del materia['tareas'][tarea_id]
    
    return redirect(url_for('materia_detail', nombre=nombre))

@app.route('/materia/<nombre>/eliminar-evento/<int:evento_id>', methods=['DELETE'])
def eliminar_evento(nombre, evento_id):
    nombre = nombre.strip()
    materia = next((m for m in materias if m['nombre'] == nombre), None)
    if not materia:
        return 'Materia no encontrada', 404
    
    if 0 <= evento_id < len(materia['eventos']):
        del materia['eventos'][evento_id]
    
    return redirect(url_for('materia_detail', nombre=nombre))

@app.route('/materia/<nombre>/editar', methods=['GET', 'POST'])
def editar_materia(nombre):
    try:
        nombre = nombre.strip()
        materia = next((m for m in materias if m['nombre'] == nombre), None)
        if not materia:
            return 'Materia no encontrada', 404
        
        if request.method == 'POST':
            nuevo_nombre = request.form['nombre'].strip()
            nuevo_horario = request.form['horario'].strip()
            nuevas_calificaciones = request.form['calificaciones'].strip()

            materia['nombre'] = nuevo_nombre
            materia['horario'] = nuevo_horario
            materia['calificaciones'] = nuevas_calificaciones
            
            return redirect(url_for('materia_detail', nombre=nuevo_nombre))
        
        return render_template('editar_materia.html', materia=materia)
    except Exception as e:
        app.logger.error(f"Error en editar_materia: {e}")
        return "Error interno del servidor", 500

if __name__ == '__main__':
    print("Info: Initiating Database...")
    database.inst_app[app]
    print("Info: Database started.")
    print("Info: Initiating Server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
    print("Info: Server started.")
