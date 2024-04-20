from flask import Flask, render_template
import mysql.connector

# Create Flask app
app = Flask(
    __name__,
    template_folder='templates',
    static_folder='static'
)


# Connect to MySQL database
# db_connection = mysql.connector.connect(
#     host="db-libros.mysql.database.azure.com",
#     user="Admin123",
#     password="321nimdA",
#     database="db_bookshop"  # Change to your database name
# )
# cursor = db_connection.cursor()

# Route to display books
@app.route('/')
def index():
    return render_template('index.html')    
# def show_books():
#     Query database to get book information
#     cursor.execute("SELECT * FROM libros")
#     books = cursor.fetchall()
#     return render_template('index.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
