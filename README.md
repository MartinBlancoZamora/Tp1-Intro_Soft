Documento de diseño de software
Nombre(s): Fiuba to-do. / Camejo-do / Intro-do (Nombre sujeto a cambio) 
Fecha límite: Julio (a confirmar)
Integrantes: Juan Pedro Basualdo (109792), Fabricio Daniel García (112064), Martin Pablo Blanco Zamora (112447).
 
Concepto:
App to-do-list para estudiante, con tareas, eventos y materias (tables en data base). Si se llega con el tiempo,agregar tareas diarias y/o integrar calendario de google y/o integración con Notion

Overview del sistema:
El sistema permite agregar materias al usuario, y a partir de las materias agregar eventos o tareas correspondientes a las materias agregadas. (A partir de llave foránea)

Consideraciones generales:
Solo se pueden crear eventos si existen materias. Las tareas pueden estar o no asociadas a una materia (se puede hacer a partir de un sistema de tags)

Las tablas de la base de datos son; 
usuario:
nombre (única)
id (única)
contraseña
mail (google)
materia:
nombre materia (única)
id (única)
horario
calificaciones
eventos:
nombre
id (único)
fecha límite 
descripción
materia (clave foránea) (tareas puede ser null)
 tareas:
nombre
id (único)
fecha límite 
descripción
materia (clave foránea) (tareas puede ser null)

Función:
El usuario crea una cuenta, luego crea una materia, luego crea un evento o una tarea y la página le avisa cuando se acerca la fecha límite de tarea/evento.
