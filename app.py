from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Create Flask app
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)


# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="db-libros.mysql.database.azure.com",
    user="Admin123",
    password="321nimdA",
    database="db_libros" 
)
cursor = db_connection.cursor()

# Route to display books
@app.route('/')
# def index():
#     return render_template('index.html')    
def show_books():
    #Query database to get book information
    cursor.execute("SELECT * FROM libros")
    books = cursor.fetchall()
    return render_template('index.html', books=books)

@app.route('/client', methods=['GET', 'POST'])
def new_client():
    cursor.execute("SELECT * FROM clientes")
    clients = cursor.fetchall()

    if request.method == 'POST':
        nombre = request.form['nombre']
        email = request.form['email']
        direccion = request.form['direccion']
        ciudad = request.form['ciudad']
        codigo_postal = request.form['codigo_postal']
        pais = request.form['pais']
        # Insertar los datos del cliente en la base de datos
        cursor.execute("INSERT INTO clientes (nombre, email, direccion, ciudad, codigo_postal, pais) VALUES (%s, %s, %s, %s, %s, %s)", (nombre, email, direccion, ciudad, codigo_postal, pais))
        db_connection.commit()
    return render_template('client.html', clients=clients)


if __name__ == '__main__':
    app.run(debug=True)
