from flask import Flask, render_template
import mysql.connector

# Create Flask app
app = Flask(__name__)

# Connect to MySQL database
db_connection = mysql.connector.connect(
    host="your_host",
    user="your_username",
    password="your_password",
    database="db_bookshop"  # Change to your database name
)
cursor = db_connection.cursor()

# Route to display books
@app.route('/')
def show_books():
    # Query database to get book information
    cursor.execute("SELECT * FROM libros")
    books = cursor.fetchall()
    return render_template('books.html', books=books)

if __name__ == '__main__':
    app.run(debug=True)
