from flask import Flask, jsonify, request
import psycopg2
app = Flask(__name__)

# Lista de métodos TODO
# Login *
# Crear proyecto *
# Asignar gestor a proyecto. ?
# Asignar cliente a proyecto.
# Crear tareas a proyecto(debe estar asignado)
# Asignar programador a proyecto
# asignar programadores a tareas.
# obtener programadores *
# obtener proyectos(activos o todos) *
# obtener tareas de un proyecto(sin asignar o asignado)

def ejecutar_sql(sql_text):
    # Datos base de datos
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "csas1234"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )
        # Crear un cursor para ejecutar
        cursor = connection.cursor()

        # Consulta SQL (por ejemplo, selecciona todos los registros de una tabla llamada usuarios)
        cursor.execute(sql_text)

        # Obtener columnas para contruir claves del JSON
        columnas = [desc[0] for desc in cursor.description]

        # Convertir resultados a JSON
        resultados = cursor.fetchall()
        empleados = [dict(zip(columnas, fila)) for fila in resultados]
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        return jsonify(empleados)

    except psycopg2.Error as e:
        print("Error", e)

@app.route("/")
def hello():
    return "Hello, World!"

@app.route('/empleado/empleados', methods=['GET'])
def obtener_empleados():
        result = ejecutar_sql('SELECT e.nombre, CASE WHEN g.empleado IS NOT NULL THEN \'Es gestor\' WHEN p.empleado IS NOT NULL THEN \'Es programador\' ELSE \'Otro puesto\' END AS tipo_puesto FROM public."Empleado" e LEFT JOIN public."Gestor" g ON e.id = g.empleado LEFT JOIN public."Programador" p ON e.id = p.empleado;')
        return result

@app.route('/programador/programadores', methods=['GET'])
def obtener_programadores():
        result = ejecutar_sql('SELECT * FROM public."Programador"')
        return result

@app.route('/Hola_mundo', methods=['GET'])
def hola_mundo():
        holaMundo = [{'msg': 'Hola, mundo!'}]
        return jsonify(holaMundo)

@app.route('/proyecto', methods=['POST'])
def crear_proyecto():
    body_request = request.json

    name = body_request["nombre"]
    description = body_request["descripcion"]
    init_date = body_request["fecha_inicio"]
    client = body_request["cliente"]

    # Datos base de datos
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "csas1234"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )
        # Crear un cursor para ejecutar
        cursor = connection.cursor()
        query = f"INSERT INTO public.\"Proyecto\" (nombre, descripcion, fecha_creacion, fecha_inicio, fecha_finalizacion, cliente) VALUES ('{name}', '{description}', NOW(), '{init_date}', null, '{client}');"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"Resultado": "Se ha creado el registro"})

    except psycopg2.Error as e:
        print("Error", e)

@app.route('/gestorproyecto', methods=['POST'])
def asignar_gestor_proyecto():
    body_request = request.json

    gestor = body_request["gestor"]
    proyecto = body_request["proyecto"]
    #fecha_asignacion = body_request["fecha_asignacion"]

    # Datos base de datos
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "csas1234"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )
        # Crear un cursor para ejecutar
        cursor = connection.cursor()
        gestor_exist = ejecutar_sql(
            f"SELECT * FROM public.\"Gestor\" WHERE id = '{gestor}';")

        if len(gestor_exist.json) == 0:
            return jsonify({"error": "No existe el gestor"}), 404

        proyecto_exist = ejecutar_sql(
            f"SELECT * FROM public.\"Proyecto\" WHERE id = '{proyecto}';")

        if len(proyecto_exist.json) == 0:
            return jsonify({"error": "No existe el proyecto"}), 404

        query = f"INSERT INTO public.\"GestoresProyecto\" (gestor, proyecto, fecha_asignacion) VALUES ('{gestor}', '{proyecto}', NOW());"
        cursor.execute(query)
        connection.commit()
        cursor.close()
        connection.close()

        return jsonify({"Resultado": "Se ha asignado el gestor al proyecto deseado"})

    except psycopg2.Error as e:
        print("Error", e)


@app.route('/proyecto/proyectos', methods=['GET'])
def obtener_proyectos():
        result = ejecutar_sql('SELECT * FROM public."Proyecto";')
        return result

@app.route('/proyecto/proyectos_activos', methods=['GET'])
def obtener_proyectos_activos():
        result = ejecutar_sql('SELECT * FROM public."Proyecto" WHERE fecha_finalizacion IS NOT NULL;')
        return result

@app.route('/proyecto/proyectos_gestor', methods=['GET'])
def obtener_proyectos_gestor_id():
    gestor_id = request.args.get('id')
    if not gestor_id:
        return jsonify({"error": "El parámetro 'id' es obligatorio"}), 500

    # Datos base de datos
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "csas1234"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )
        # Crear un cursor para ejecutar
        cursor = connection.cursor()
        query = 'SELECT * FROM public."GestoresProyecto" gp JOIN public."Proyecto" p ON gp."proyecto" = p."id" WHERE gp."gestor" = %s;'
        # gp JOIN public."Proyecto" p ON gp."proyecto" = p."id" WHERE gp."gestor" = %s
        # Consulta SQL (por ejemplo, selecciona todos los registros de una tabla llamada usuarios)
        cursor.execute(query, (gestor_id))

        # Obtener columnas para contruir claves del JSON
        columnas = [desc[0] for desc in cursor.description]

        # Convertir resultados a JSON
        resultados = cursor.fetchall()
        empleados = [dict(zip(columnas, fila)) for fila in resultados]
        # Cerrar el cursor y la conexión
        cursor.close()
        connection.close()

        return jsonify(empleados)

    except psycopg2.Error as e:
        print("Error", e)

@app.route('/login', methods=['POST'])
def gestor_login():
    body_request = request.json

    username = body_request["usuario"]
    passwd = body_request["passwd"]

    # Datos base de datos
    host = "localhost"
    port = "5432"
    dbname = "alexsoft"
    user = "postgres"
    password = "csas1234"

    try:
        connection = psycopg2.connect(
            host=host,
            port=port,
            dbname=dbname,
            user=user,
            password=password,
            options="-c search_path=public"
        )
        # Crear un cursor para ejecutar
        cursor = connection.cursor()
        query = f"SELECT * FROM public.\"Gestor\" WHERE usuario = '{username}' AND passwd = '{passwd}';"
        #
        cursor.execute(query)
        is_logged = ejecutar_sql(f"SELECT * FROM public.\"Gestor\" WHERE usuario = '{username}' AND passwd = '{passwd}';")

        if len(is_logged.json) == 0:
            return jsonify({"error": "Error en el login"}), 404

        empleado = ejecutar_sql(f"SELECT * FROM public.\"Empleado\" WHERE id = '{is_logged.json[0]["empleado"]}';")

        resultado = {
            "id": empleado.json[0]["id"],
            "id_gestor": is_logged.json[0]["id"],
            "nombre": empleado.json[0]["nombre"],
            "email": empleado.json[0]["email"],
        }
        cursor.close()
        connection.close()

        return jsonify(resultado)

    except psycopg2.Error as e:
        print("Error", e)

if __name__=='__main__':
    app.run(debug=True)