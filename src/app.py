from flask import Flask, render_template, request, redirect, url_for, flash, session
from werkzeug.security import generate_password_hash, check_password_hash
from models import database, Usuarios, Materias, Eventos, Tareas

app = Flask(__name__)
port = 5000
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config['SECRET_KEY'] = 'chopperino'
print("Info: Initiating Database...")
database.init_app(app)
print("Info: Database started.")

@app.route("/")
def base():
    return render_template('base.html')

@app.route('/home')
def home():
    return render_template('home.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['input_nombre']
        password = request.form['input_pass']
            
        user = Usuarios.query.filter_by(nombre_usuario=username).first()
            
        if user and user.contraseña==password:
            session['user_id'] = user.id
            flash('Inicio de sesión exitoso', 'success')
            return redirect(url_for('profile'))  # Redirige a la página deseada después del inicio de sesión
        else:
            flash('Usuario o contraseña incorrectos', 'error')
        
    return render_template('usuario.html')

@app.route('/profile')
def profile():
    # Obtener el ID del usuario desde la sesión
    user_id = session.get('user_id')
    
    if user_id:
        # Cargar datos del perfil
        user = Usuarios.query.get(user_id)
        if user:
            return render_template('profile.html', usuario=user)
        else:
            flash('Usuario no encontrado', 'error')
            return redirect(url_for('login'))
    else:
        flash('Debe iniciar sesión primero', 'error')
        return redirect(url_for('login'))

@app.route('/signup', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['input_nombre']
        email = request.form['input_mail']
        password = request.form['input_pass']
        confirm_password = request.form['input_confirm']

        # Verificar si el usuario ya existe en la base de datos
        existing_user = Usuarios.query.filter_by(nombre_usuario=username).first()
        if existing_user:
            flash('El nombre de usuario ya está en uso.', 'error')
            return redirect(url_for('registro'))

        # Verificar si el correo electrónico ya está en uso
        existing_email = Usuarios.query.filter_by(mail=email).first()
        if existing_email:
            flash('El correo electrónico ya está en uso.', 'error')
            return redirect(url_for('registro'))

        # Crear una nueva instancia de Usuario
        new_user = Usuarios(nombre_usuario=username, mail=email, contraseña=generate_password_hash(password))

        # Agregar el nuevo usuario a la base de datos
        database.session.add(new_user)
        database.session.commit()

        flash('Registro exitoso. Ahora puedes iniciar sesión.', 'success')
        return redirect(url_for('login'))

    return render_template('registro.html')

@app.route('/gestion_materias', methods = ['GET', 'POST'])
def gestion_materias():
    if request.method == 'POST':
        if 'user_id' not in session:
            flash('Debes iniciar sesión para agregar una materia', 'error')
            return redirect(url_for('login')), 307
    
        user_id = session['user_id']
        nombre_materia = request.form['nombre_materia']
        horario = request.form['horario_materia']
        calificaciones = request.form['calificaciones_materia']
    
        # Crear y guardar la nueva materia en la base de datos
        nueva_materia = Materias(nombre=nombre_materia, horario=horario, usuario_id=user_id)
        database.session.add(nueva_materia)
        database.session.commit()
        
        flash('Materia agregada correctamente', 'success')
        return redirect(url_for('gestion_materias'))

    if 'user_id' not in session:
        flash('Debes iniciar sesión para acceder a esta página', 'error')
        return redirect(url_for('login')), 307
    
    # Obtener el usuario actual
    id_usuario = session['user_id']
    user = Usuarios.query.get(id_usuario)
    
    # Obtener las materias del usuario actual
    materias = Materias.query.filter_by(usuario_id=id_usuario).all()
    
    return render_template('gestion_materias.html', materias=materias), 200

@app.route('/materia_detalle/<int:materia_id>')
def detalle_materia(materia_id):
    materia = Materias.query.get(materia_id)
    if not materia:
        flash('La materia no existe', 'error')
        return redirect(url_for('gestion_materias'))
        
    # Obtener las tareas asociadas a esta materia
    tareas = Tareas.query.filter_by(materia_id=materia.id).all()
    eventos = Eventos.query.filter_by(materia_id=materia.id).all()
        
    return render_template(
        'materia.html', 
        materia=materia, 
        tareas=tareas, 
        eventos=eventos, 
        agregar_tarea=url_for('agregar_tarea', materia_id=materia_id)
    )

# Ruta para agregar una nueva tarea
@app.route('/agregar_tarea/<int:materia_id>', methods=['POST'])
def agregar_tarea(materia_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para agregar una tarea', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    materia = Materias.query.filter_by(id=materia_id, usuario_id=user_id).first()
    
    if not materia:
        flash('No tienes permiso para agregar tareas a esta materia', 'error')
        return redirect(url_for('gestion_materias'))
    
    nombre_tarea = request.form['nombre_tarea']
    fecha_limite = request.form['fecha_limite']
    descripcion = request.form['descripcion']
    
    nueva_tarea = Tareas(nombre=nombre_tarea, fecha_limite=fecha_limite, descripcion=descripcion, materia_id=materia_id)
    database.session.add(nueva_tarea)
    database.session.commit()
    
    flash('Tarea agregada correctamente', 'success')
    return redirect(url_for('gestion_materias', materia_id=materia_id))

# Ruta para agregar un nuevo evento
@app.route('/agregar_evento/<int:materia_id>', methods=['POST'])
def agregar_evento(materia_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para agregar un evento', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    materia = Materias.query.filter_by(id=materia_id, usuario_id=user_id).first()
    
    if not materia:
        flash('No tienes permiso para agregar eventos a esta materia', 'error')
        return redirect(url_for('gestion_materias'))
    
    nombre_evento = request.form['nombre_evento']
    fecha_limite = request.form['fecha_limite']
    descripcion = request.form['descripcion']
    
    nuevo_evento = Eventos(nombre=nombre_evento, fecha_limite=fecha_limite, descripcion=descripcion, materia_id=materia_id)
    database.session.add(nuevo_evento)
    database.session.commit()
    
    flash('Evento agregado correctamente', 'success')
    return redirect(url_for('gestion_materia', materia_id=materia_id))

# Ruta para editar una materia
@app.route('/editar_materia/<int:materia_id>', methods=['GET' , 'POST'])
def editar_materia(materia_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para editar una materia', 'error')
        return redirect(url_for('login'))
    if request.method == 'POST':
        user_id = session['user_id']
        materia = Materias.query.filter_by(id=materia_id, usuario_id=user_id).first()
        
        if not materia:
            flash('No tienes permiso para editar esta materia', 'error')
            return redirect(url_for('gestion_materias'))
        
        materia.nombre = request.form['nombre_materia']
        materia.horario = request.form['horario']
        materia.calificaciones = request.form['calificaciones']
        database.session.commit()
        
        flash('Materia editada correctamente', 'success')
        return redirect(url_for('gestion_materias', materia_id=materia_id))
    
    return render_template('editar_materia.html')

@app.route('/eliminar_materia/<int:materia_id>', methods=['POST'])
def eliminar_materia(materia_id):
    if 'user_id' not in session:
        flash('Debes iniciar sesión para eliminar una materia', 'error')
        return redirect(url_for('login'))
    
    # Verificar si la materia pertenece al usuario actual
    user_id = session['user_id']
    materia = Materias.query.filter_by(id=materia_id, usuario_id=user_id).first()
    
    if not materia:
        flash('No tienes permiso para eliminar esta materia', 'error'), 404, 308
    else:
        # Eliminar la materia de la base de datos
        database.session.delete(materia)
        database.session.commit()
        flash('Materia eliminada correctamente', 'success'), 200
    
    return redirect(url_for('gestion_materias')), 200

# Ruta para listar todos los eventos de un usuario
@app.route('/eventos')
def eventos():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver tus tareas', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    eventos = Eventos.query.join(Materias).filter(Materias.usuario_id == user_id).all()
    
    return render_template('eventos.html', eventos=eventos)

# Ruta para listar todas las tareas de un usuario
@app.route('/tareas')
def tareas():
    if 'user_id' not in session:
        flash('Debes iniciar sesión para ver tus tareas', 'error')
        return redirect(url_for('login'))
    
    user_id = session['user_id']
    tareas = Tareas.query.join(Materias).filter(Materias.usuario_id == user_id).all()
    
    return render_template('mistareas.html', tareas=tareas)

@app.route('/eliminar_tarea/<int:tarea_id>', methods=['POST'])
def eliminar_tarea(tarea_id):
    tarea = Tareas.query.get(tarea_id)
    if not tarea:
        flash('La tarea no existe', 'error')
        return redirect(url_for('gestion_materias'))
    
    database.session.delete(tarea)
    database.session.commit()
    flash('Tarea eliminada exitosamente', 'success')
    return redirect(url_for('detalle_materia', materia_id=tarea.materia_id))


@app.route('/eliminar_evento/<int:evento_id>', methods=['POST'])
def eliminar_evento(evento_id):
    evento = Eventos.query.get(evento_id)
    if not evento:
        flash('La tarea no existe', 'error')
        return redirect(url_for('gestion_materias'))
    
    database.session.delete(evento)
    database.session.commit()
    flash('Tarea eliminada exitosamente', 'success')
    return redirect(url_for('detalle_materia', materia_id=evento.materia_id))

print("Info: Checking database...")
with app.app_context():
        print("Info: Creating database...")
        database.create_all()

if __name__ == '__main__':
    print("Info: Initiating Server...")
    app.run(host="0.0.0.0", port=5000, debug=True)
    print("Info: Server started.")
