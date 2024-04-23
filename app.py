from flask import Flask, session, render_template, request, redirect, url_for
import mysql.connector

def obtener_nombre_usuario(user_id):
    try:
        # Obtain the user name from the database
        cursor.execute("SELECT nombre FROM clientes WHERE id = %s", (user_id,))
        # Fetch one record
        usuario = cursor.fetchone()
        # Return the user name
        if usuario:
            return usuario
        else:
            return None
    except mysql.connector.Error as error:
        # Render an error page with the error message
        return render_template('error.html', message=error)

# Create Flask app
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)
app.secret_key = 'bookshop56420'

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="db-libros.mysql.database.azure.com",
    user="Admin123",
    password="321nimdA",
    database="db_libros" 
)
cursor = db_connection.cursor(dictionary=True)

@app.route('/') 
@app.route('/home')
def home():
    if 'user_id' in session:
        nombre_usuario = obtener_nombre_usuario(session['user_id'])
        return render_template('index.html', nombre_usuario=nombre_usuario)
    else:
        return render_template('index.html')

@app.route('/catalogo')
def catalogo():
    if 'user_id' in session:
        nombre_usuario = obtener_nombre_usuario(session['user_id'])
    else:
        nombre_usuario = None
    
    # Consulta para obtener todas las categorías
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    # Consulta para obtener los libros por categoría
    libros_por_categoria = {}
    for categoria in categorias:
        cursor.execute("SELECT * FROM libros WHERE categoria_id = %s", (categoria['id'],))
        libros_por_categoria[categoria['nombre']] = cursor.fetchall()

    return render_template('catalogo.html', libros_por_categoria=libros_por_categoria, nombre_usuario=nombre_usuario)

@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        # Check if the request method is POST
        if request.method == 'POST':
            # Get email and password from the form
            email = request.form['email']
            contrasena = request.form['contrasena']
            # Check if the email and password are correct
            try:
                cursor.execute("SELECT * FROM clientes WHERE email = %s AND contrasena = %s", (email, contrasena,))
            except mysql.connector.Error as error:
                print(error)

            # Fetch one record
            cliente = cursor.fetchone()
            if cliente:
                # Storage the user id in a session
                # session['user_id'] = cliente['id']
                #return redirect(url_for('error.html', message=cliente))
                # If the user does not exist, render the login page again
                print(cliente)
            else:
                message="Usuario o contraseña incorrectos"
                return render_template('login.html', message=message)
        else:
            return render_template('login.html')
    except mysql.connector.Error as error:
        # Render an error page with the error message
        return render_template('error.html', message=error)


@app.route('/register', methods=['GET', 'POST'])
def register():
    try:
        if request.method == 'POST':
            # Get the data from the form
            nombre = request.form['nombre']
            email = request.form['email']
            contrasena = request.form['contrasena']
            direccion = request.form['direccion']
            ciudad = request.form['ciudad']
            codigo_postal = request.form['codigo_postal']
            pais = request.form['pais']
            # Insert the data into the database
            cursor.execute("INSERT INTO clientes (nombre, email, direccion, ciudad, codigo_postal, pais, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, email, direccion, ciudad, codigo_postal, pais, contrasena))
            # Commit the transaction
            db_connection.commit()
            # Redirect to the login page
            message="Usuario registrado correctamente. Pasa a Iniciar Sesión."
            return render_template('register.html', message=message)
        else:
            return render_template('register.html')
    except mysql.connector.Error as error:
        # Render an error page with the error message
        return render_template('error.html', message=error)

@app.route('/mensaje')
def mensaje():
    if 'user_id' in session:
        nombre_usuario = obtener_nombre_usuario(session['user_id'])
    else:
        nombre_usuario = None

    return render_template('mensaje.html', nombre_usuario=nombre_usuario)

@app.route('/pedido/<int:libro_id>', methods=['GET', 'POST'])
def pedido(libro_id):
    if 'user_id' not in session:
        message = "Por favor inicia sesión para realizar un pedido"
        return render_template('login.html', message=message)
    
    try:
        if request.method == 'POST':
            cursor.execute("INSERT INTO pedidos (cliente_id, fecha_pedido, estado) VALUES (%s, NOW(), %s)", (session['user_id'], "pendiente",))
            db_connection.commit()
            pedido_id = cursor.lastrowid
            cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
            libro = cursor.fetchone()
            precio_unitario = libro['precio']
            cursor.execute("INSERT INTO detalles_pedido (pedido_id, libro_id, cantidad, precio_unitario, total) VALUES (%s, %s, 1, %s, %s)", (pedido_id, libro_id, precio_unitario, precio_unitario))
            db_connection.commit()
            return redirect(url_for('mensaje'))
        else:
            cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
            libro = cursor.fetchone()
            return render_template('pedido.html', libro=libro)
    except mysql.connector.Error as error:
        # Render an error page with the error message
        return render_template('error.html', message=error)

@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect(url_for('home'))



if __name__ == '__main__':
    app.run(debug=True)