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
cursor = db_connection.cursor(dictionary=True)

@app.route('/') 
def home():
    return render_template('index.html')

@app.route('/home')
def home_page():
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

    return render_template('catalogo.html', libros_por_categoria=libros_por_categoria)

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/registro')
def register():
    return render_template('register.html')

@app.route('/mensaje')
def mensaje():
    return render_template('mensaje.html')

@app.route('/pedido/<int:libro_id>', methods=['GET', 'POST'])
def pedido(libro_id):
    if request.method == 'POST':
        cursor.execute("INSERT INTO pedidos (usuario_id, fecha) VALUES (%s, NOW())", (1,))
        pedido_id = cursor.lastrowid
        cursor.execute("INSERT INTO detalles_pedido (pedido_id, libro_id, cantidad) VALUES (%s, %s, 1)", (pedido_id, libro_id))
        db_connection.commit()
        return redirect(url_for('mensaje'))

    else:
        cursor.execute("SELECT * FROM libros WHERE id = %s", (libro_id,))
        libro = cursor.fetchone()
        return render_template('pedido.html', libro=libro)

if __name__ == '__main__':
    app.run(debug=True)
