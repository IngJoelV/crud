from flask import Flask, render_template, request, redirect, url_for
from flask_mysqldb import MySQL

app = Flask(__name__, template_folder='.')

# Configuración de MySQL
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''  # Cambia si tienes contraseña
app.config['MYSQL_DB'] = 'crud'
mysql = MySQL(app)

# Ruta principal para mostrar los datos
@app.route('/')
def index():
    cursor = mysql.connection.cursor()
    cursor.execute("SELECT * FROM items")
    items = cursor.fetchall()
    return render_template('index.html', items=items)

# Ruta para crear un nuevo registro
@app.route('/create', methods=['POST'])
def create():
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO items (name, description) VALUES (%s, %s)", (name, description))
        mysql.connection.commit()
        return redirect(url_for('index'))

# Ruta para actualizar un registro existente
@app.route('/update/<id>', methods=['POST'])
def update(id):
    if request.method == 'POST':
        name = request.form['name']
        description = request.form['description']
        cursor = mysql.connection.cursor()
        cursor.execute("""
            UPDATE items
            SET name = %s, description = %s
            WHERE id = %s
        """, (name, description, id))
        mysql.connection.commit()
        return redirect(url_for('index'))

# Ruta para eliminar un registro
@app.route('/delete/<id>')
def delete(id):
    cursor = mysql.connection.cursor()
    cursor.execute("DELETE FROM items WHERE id = %s", [id])
    mysql.connection.commit()
    return redirect(url_for('index'))

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run(debug=True)
