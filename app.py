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

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/home')
def home_page():
    return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    return render_template('catalogo.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def register():
    return render_template('register.html')

@app.route('/mensaje')
def mensaje():
    return render_template('mensaje.html')

@app.route('/pedido')
def pedido():
    return render_template('pedido.html')

if __name__ == '__main__':
    app.run(debug=True)
