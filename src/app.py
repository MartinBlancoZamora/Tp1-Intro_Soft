from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)


materias = []


@app.route('/', methods=['GET'])
def base():
    return render_template('base.html')

@app.route('/home', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/eventos', methods=['GET'])
def eventos():
    return render_template('eventos.html')

@app.route('/tareas', methods=['GET'])
def tareas():
    return render_template('tareas.html')

@app.route('/profile')
def profile():
    usuario = {
        'nombre': 'Juan Pérez',
        'email': 'juan.perez@ejemplo.com',
        'password': 'hola123'  
    }      

    return render_template('profile.html', usuario=usuario)

@app.route('/usuario', methods=['GET'])
def usuario():
    return render_template('usuario.html')

@app.route('/registro', methods=['GET'])
def registro():
    return render_template('registro.html')

@app.route('/gestion_materias', methods=['GET', 'POST'])
def gestionmaterias():
    if request.method == 'POST':
        nombre = request.form['nombreMateria'].strip()
        horario = request.form['horarioMateria'].strip()
        calificaciones = request.form['calificacionesMateria'].strip()
        
        materia = {
            'nombre': nombre,
            'horario': horario,
            'calificaciones': calificaciones,
            'tareas': [],
            'eventos': []
        }
        materias.append(materia)
        
    return render_template('gestion_materias.html', materias=materias)

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

@app.route('/materia/<nombre>/eliminar-evento/<int:evento_id>', methods=['POST'])
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
    app.run(host="0.0.0.0", port=5000, debug=True)


