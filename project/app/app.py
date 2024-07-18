from flask import Flask, render_template, request, redirect, url_for, flash, jsonify,session
#from data import *
from datetime import date, datetime
from db import *
from dbcdt import *
#from controller_db import *

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/')
def index():
    return render_template('index.html')

#CRUD - Read ITEMS | tipo_categoria = Libro
@app.route('/libros')
def libro ():
    connection = get_cdt_connection()
    libro=[]
    try:
        with connection.cursor() as cursor:
            #sql = "SELECT * FROM items WHERE tipo_categoria = 'Libro'"
            sql = """
            SELECT items.id_item, items.nombre, items.detalle, items.tipo_categoria, usuarios.nombre as user_name
            FROM items
            JOIN usuarios ON items.id_usuario = usuarios.id_usuario
            WHERE items.tipo_categoria = 'Libro'
            """

            cursor.execute(sql)
            libro = cursor.fetchall()
            print("Fetched libros:", libro)
    finally:
        connection.commit()
        connection.close()
    
    return render_template('libros.html', items=libro)
    #return libro

#CRUD - Read ITEMS | tipo_categoria = Disco
@app.route('/discos')
def disco ():
    connection = get_cdt_connection()
    disco=[]
    try:
        with connection.cursor() as cursor:
            #sql = "SELECT * FROM items WHERE tipo_categoria = 'Disco'"
            sql = """
            SELECT items.id_item, items.nombre, items.detalle, items.tipo_categoria, usuarios.nombre as user_name
            FROM items
            JOIN usuarios ON items.id_usuario = usuarios.id_usuario
            WHERE items.tipo_categoria IN ('Disco','CD','DVD')
            ORDER BY items.id_item ASC
            """

            cursor.execute(sql)
            disco = cursor.fetchall()
            print("Fetched Discos:", disco)
    finally:
        connection.commit()
        connection.close()
    
    return render_template('discos.html', items=disco)
    #return 

#CRUD - Read ITEMS | tipo_categoria = Ropa
@app.route('/ropa')
def ropa ():
    connection = get_cdt_connection()
    ropa=[]
    try:
        with connection.cursor() as cursor:
            #sql = "SELECT * FROM items WHERE tipo_categoria = 'Ropa'"
            sql = """
            SELECT items.id_item, items.nombre, items.detalle, items.tipo_categoria, usuarios.nombre as user_name
            FROM items
            JOIN usuarios ON items.id_usuario = usuarios.id_usuario
            WHERE items.tipo_categoria = 'Ropa'
            """

            cursor.execute(sql)
            ropa = cursor.fetchall()
            print("Fetched Ropa:", ropa)
    finally:
        connection.commit()
        connection.close()
    
    return render_template('ropa.html', items=ropa)
    #return 

#CRUD - Read ITEMS | tipo_categoria = Videojuego
@app.route('/videojuegos')
def videojuego():
    connection = get_cdt_connection()
    videojuego=[]
    try:
        with connection.cursor() as cursor:
            #sql = "SELECT * FROM items WHERE tipo_categoria = 'Videojuego'"
            sql = """
            SELECT items.id_item, items.nombre, items.detalle, items.tipo_categoria, usuarios.nombre as user_name
            FROM items
            JOIN usuarios ON items.id_usuario = usuarios.id_usuario
            WHERE items.tipo_categoria IN ('Videojuego','Consola')
            ORDER BY items.id_item ASC
            """

            cursor.execute(sql)
            videojuego = cursor.fetchall()
            print("Fetched Videojuegos:", videojuego)
    finally:
        connection.commit()
        connection.close()
    
    return render_template('videojuegos.html', items=videojuego)
    #return 

#CRUD - INSERT MESSAGE IN CONTACT US DB
@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    nombre = request.form['name']
    email = request.form['email']
    mensaje = request.form['message']

    # Validate and sanitize inputs (basic example)
    if not nombre or not email or not mensaje:
        #return "All fields are required."
        flash("Todos los campos son obligatorios.", "error")
        return redirect(url_for('index'))

    connection = get_db_connection()
    try:
        with connection.cursor() as cursor:
            sql = "INSERT INTO contacts (nombre, email, mensaje) VALUES (%s, %s, %s)"
            cursor.execute(sql, (nombre, email, mensaje))
        connection.commit()
        flash("Tu mensaje ha sido enviado!", "success")
    finally:
        connection.close()

    #return "New record created successfully"
    return redirect(url_for('index', _anchor='contacto'))


# Login route
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Mock user authentication (replace with your actual authentication logic)
        if username == 'admin' and password == 'password':
            session['logged_in'] = True
            flash('Login successful!', 'success')
            return redirect(url_for('items'))
        else:
            flash('Invalid username or password', 'error')
            return redirect(url_for('login'))

    return render_template('login.html')

#CRUD - READ ALL ITEMS
@app.route('/items')
def items():
    if not session.get('logged_in'):
        flash('Please login first.', 'error')
        return redirect(url_for('login'))

    connection = get_cdt_connection()
    try:
        with connection.cursor() as cursor:
            #sql = "SELECT * FROM items"
            sql = "SELECT * FROM items ORDER BY id_item ASC"
            #sql = """
            #SELECT items.id_item, items.nombre, items.detalle, items.tipo_categoria, usuarios.nombre as user_name
            #FROM items
            #JOIN usuarios ON items.id_usuario = usuarios.id_usuario
            #"""
            cursor.execute(sql)
            items = cursor.fetchall()
    finally:
        connection.close()

    return render_template('items.html', items=items)

# Route to display edit form for a specific item
"""@app.route('/edit_item/<int:id_item>', methods=['GET', 'POST'])
def edit_item(id_item):
    connection = get_cdt_connection()
    try:
        with connection.cursor() as cursor:
            # Fetch item details
            sql = "SELECT * FROM items WHERE id_item = %s"
            cursor.execute(sql, ('id_item',))
            item = cursor.fetchone()
        
        if request.method == 'POST':
            # Process form submission to update item
            nombre = request.form['nombre']
            detalle = request.form['detalle']
            tipo_categoria = request.form['tipo_categoria']

            with connection.cursor() as cursor:
                sql = "UPDATE items SET nombre = %s, detalle = %s, tipo_categoria = %s WHERE id_item = %s"
                cursor.execute(sql, (nombre, detalle, tipo_categoria, id_item))
                connection.commit()
            
            flash("Item updated successfully!", "success")
            return redirect(url_for('items'))

    finally:
        connection.close()

    return render_template('edit_item.html', item=item)

# Route to delete a specific item
@app.route('/delete_item/<int:id_item>', methods=['GET'])
def delete_item(id_item):
    connection = get_cdt_connection()
    try:
        with connection.cursor() as cursor:
            # Delete item from database
            sql = "DELETE FROM items WHERE id_item = %s"
            cursor.execute(sql, ('id_item',))
            connection.commit()
        
        flash("Item deleted successfully!", "success")
    finally:
        connection.close()

    return redirect(url_for('items'))"""

@app.route('/create_item', methods=['GET', 'POST'])
def create_item():
    if request.method == 'POST':
        nombre = request.form['nombre']
        detalle = request.form['detalle']
        tipo_categoria = request.form['tipo_categoria']

        connection = get_cdt_connection()
        try:
            with connection.cursor() as cursor:
                sql = "INSERT INTO items (nombre, detalle, tipo_categoria, id_usuario) VALUES (%s, %s, %s, %s)"
                cursor.execute(sql, (nombre, detalle, tipo_categoria,5))
                connection.commit()
                flash("Item creado exitosamente!", "success")
        finally:
            connection.close()

        return redirect(url_for('items'))

    return render_template('create_item.html')


# Route to update item
@app.route('/update_item/<int:id_item>', methods=['POST'])
def update_item(id_item):
    data = request.json
    id_item = data ['id_item']
    nombre = data['nombre']
    detalle = data['detalle']
    tipo_categoria = data['tipo_categoria']

    connection = get_cdt_connection()
    try:
        with connection.cursor() as cursor:
            sql = "UPDATE items SET nombre=%s, detalle=%s, tipo_categoria=%s WHERE id_item=%s"
            cursor.execute(sql, ('nombre', 'detalle', 'tipo_categoria', 'id_item'))
        connection.commit()
        return jsonify({"success": True})
    except Exception as e:
        print(e)
        return jsonify({"success": False}), 500
    finally:
        connection.close()

# Route to delete item
@app.route('/delete_item/<int:id_item>', methods=['POST'])
def delete_item(id_item):
    connection = get_cdt_connection()
    try:
        with connection.cursor() as cursor:
            sql = "DELETE FROM items WHERE id_item=%s"
            cursor.execute(sql, (id_item,))
        connection.commit()
        #return jsonify({"success": True})
        return redirect(url_for('items'))
    except Exception as e:
        print(e)
        return jsonify({"success": False}), 500
    finally:
        connection.close()
    

if __name__ == '__main__':
    app.run(debug=True)
