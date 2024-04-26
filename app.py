from flask import Flask, render_template, request, redirect, url_for, session
import mysql.connector

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
        nombre_usuario = session['user_name']
        return render_template('index.html', nombre_usuario=nombre_usuario)
    else:
        return render_template('index.html')

@app.route('/catalogo')
def catalogo():    
    # Consulta para obtener todas las categorías
    cursor.execute("SELECT * FROM categorias")
    categorias = cursor.fetchall()

    # Consulta para obtener los libros por categoría
    libros_por_categoria = {}
    for categoria in categorias:
        cursor.execute("SELECT * FROM libros WHERE categoria_id = %s", (categoria['id'],))
        libros_por_categoria[categoria['nombre']] = cursor.fetchall()

    if 'user_id' in session:
        nombre_usuario = session['user_name']
        return render_template('catalogo.html', libros_por_categoria=libros_por_categoria, nombre_usuario=nombre_usuario)
    else:
        return render_template('catalogo.html', libros_por_categoria=libros_por_categoria)

@app.route('/login', methods=['GET', 'POST'])
def login(message=None):
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
                session['user_id'] = cliente['id']
                session['user_name'] = cliente['nombre']
                return redirect(url_for('catalogo'))
            else:
                message="Usuario o contraseña incorrectos"
                return render_template('login.html', message=message)
        else:
            return render_template('login.html', message=message)
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
            # Verify if email already exists
            cursor.execute("SELECT * FROM clientes WHERE email = %s", (email,))
            user = cursor.fetchone()
            if user:
                message="El email ingresado ya se encuentra registrado."
            else:
                # Insert the data into the database
                cursor.execute("INSERT INTO clientes (nombre, email, direccion, ciudad, codigo_postal, pais, contrasena) VALUES (%s, %s, %s, %s, %s, %s, %s)", (nombre, email, direccion, ciudad, codigo_postal, pais, contrasena))
                # Commit the transaction
                db_connection.commit()
                # Redirect to the login page
                message="Usuario registrado correctamente. Pasa a iniciar sesión."
            
            return render_template('register.html', message=message)
        else:
            return render_template('register.html')
    except mysql.connector.Error as error:
        # Render an error page with the error message
        return render_template('error.html', message=error)

@app.route('/mensaje')
def mensaje():
    if 'user_id' in session:
        nombre_usuario = session['user_name']
        return render_template('mensaje.html', nombre_usuario=nombre_usuario)
    else:
        return render_template('mensaje.html')

    

@app.route('/pedido/<int:libro_id>', methods=['GET', 'POST'])
def pedido(libro_id):
    id_usuario = session['user_id']
    nombre_usuario = session['user_name']
    
    try:
        if request.method == 'POST':
            cursor.execute("INSERT INTO pedidos (cliente_id, fecha_pedido, estado) VALUES (%s, NOW(), %s)", (id_usuario, "pendiente",))
            db_connection.commit()
            pedido_id = cursor.lastrowid
            cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
            libro = cursor.fetchone()
            if libro['stock'] < 1:
                return render_template('pedido.html', libro=libro, nombre_usuario=nombre_usuario, message="No hay stock disponible")
            else:
                precio_unitario = libro['precio']
                cursor.execute("INSERT INTO detalles_pedido (pedido_id, libro_id, cantidad, precio_unitario, total) VALUES (%s, %s, 1, %s, %s)", (pedido_id, libro_id, precio_unitario, precio_unitario))
                # Update stock of book
                cursor.execute("UPDATE libros SET stock = stock - 1 WHERE id = %s", (libro_id,))
                db_connection.commit()
                return redirect(url_for('mensaje'))
        else:
            cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
            libro = cursor.fetchone()
            return render_template('pedido.html', libro=libro, nombre_usuario=nombre_usuario)
    except mysql.connector.Error as error:
        # Render an error page with the error message
        return render_template('error.html', message=error, nombre_usuario=nombre_usuario)

@app.route('/historial')
def historial():
    if 'user_id' in session:
        id_usuario = session['user_id']
        nombre_usuario = session['user_name']
        try:    
            cursor.execute("SELECT pedidos.id, pedidos.fecha_pedido, libros.titulo, detalles_pedido.precio_unitario, pedidos.estado FROM pedidos INNER JOIN detalles_pedido ON pedidos.id = detalles_pedido.pedido_id INNER JOIN libros ON detalles_pedido.libro_id = libros.id WHERE pedidos.cliente_id = %s", (id_usuario,))
            pedidos = cursor.fetchall()
            return render_template('historial.html', pedidos=pedidos, nombre_usuario=nombre_usuario)
        except mysql.connector.Error as error:
            return render_template('error.html', message=error, nombre_usuario=nombre_usuario)
        
    else:
        return redirect(url_for('login', message="Inicia sesión para ver tu historial de pedidos"))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('home'))


if __name__ == '__main__':
    app.run(debug=True)