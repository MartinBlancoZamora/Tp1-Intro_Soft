from flask import Flask, render_template, request, redirect, url_for

app = Flask(__name__)

# Lista para almacenar materias
materias = []

@app.route('/', methods=['GET'])
def home():
    return render_template('home.html')

@app.route('/gestion_materias', methods=['GET', 'POST'])
def gestionmaterias():
    if request.method == 'POST':
        nombre = request.form['nombreMateria'].strip()
        horario = request.form['horarioMateria'].strip()
        calificaciones = request.form['calificacionesMateria'].strip()
        
        materia = {
            'nombre': nombre,
            'horario': horario,
            'calificaciones': calificaciones
        }
        materias.append(materia)
        
    return render_template('gestion_materias.html', materias=materias)

@app.route('/usuario', methods=['GET'])
def usuario():
    return render_template('usuario.html')

@app.route('/registro', methods=['GET'])
def registro():
    return render_template('registro.html')

@app.route('/materia/<nombre>', methods=['GET', 'PATCH'])
def materia_detail(nombre):
    nombre = nombre.strip()  # Eliminar espacios innecesarios
    for materia in materias:
        if materia['nombre'] == nombre:
            return render_template('materia.html', materia=materia)
    return 'Materia no encontrada', 404

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000, debug=True)
