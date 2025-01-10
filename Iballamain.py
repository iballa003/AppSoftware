from flask import Flask, jsonify, request
import psycopg2
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

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

@app.route('/empleado/empleados', methods=['GET'])
def obtener_empleados():
        result = ejecutar_sql('SELECT e.nombre, CASE WHEN g.empleado IS NOT NULL THEN \'Es gestor\' WHEN p.empleado IS NOT NULL THEN \'Es programador\' ELSE \'Otro puesto\' END AS tipo_puesto FROM public."Empleado" e LEFT JOIN public."Gestor" g ON e.id = g.empleado LEFT JOIN public."Programador" p ON e.id = p.empleado;')
        return result

if __name__=='__main__':
    app.run(debug=True)