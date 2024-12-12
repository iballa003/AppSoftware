from flask import Flask
import psycopg2
app = Flask(__name__)

@app.route("/")
def hello():
    return "Hello, World!"

def ejecutar_sql():
    # Datos base de datos
    host = "localhost"