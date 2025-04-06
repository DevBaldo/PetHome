from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson.objectid import ObjectId
import base64

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PetHome"]  # Nombre de tu base de datos
collection = db["Mascotas"]  # colección

@app.route('/')
def inicio():
    return redirect(url_for('bienvenida'))

@app.route('/bienvenida')
def bienvenida():
    mascotas= collection.find()
    return render_template('bienvenida.html', mascotas=mascotas)

@app.route('/index')
def index():
    # Esta es la ruta para la lista de mascotas
    mascotas = collection.find()  # Recupera todas las mascotas
    return render_template('index.html', mascotas=mascotas)

@app.route('/agregar', methods=['GET', 'POST'])
def agregar_mascota():
    if request.method == 'POST':
        nombre = request.form['nombre']
        edad = request.form['edad']
        sexo = request.form['sexo']
        salud = request.form['salud']
        comportamiento = request.form['comportamiento']
        caracteristicas = request.form['caracteristicas']
        color = request.form['color']
        raza = request.form['raza']

        # Verificamos si se subió una imagen
        imagen = request.files.get('imagen')
        if imagen:
            img_bytes = imagen.read()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')
        else:
            img_base64 = "Sin imagen"
        
        # Insertar nueva mascota en la colección
        collection.insert_one({
            'nombre': nombre,
            'edad': edad,
            'sexo': sexo,
            'salud': salud,
            'comportamiento': comportamiento,
            'caracteristicas': caracteristicas,
            'color': color,
            'raza': raza,
            'imagen': img_base64
        })

        return redirect(url_for('index'))
    
    return render_template('agregar_mascota.html')

@app.route('/editar/<id>', methods=['GET', 'POST'])
def editar_mascota(id):
    mascota = collection.find_one({'_id': ObjectId(id)})
    
    if request.method == 'POST':
        # Obtener los datos del formulario
        nombre = request.form['nombre']
        edad = request.form['edad']
        sexo = request.form['sexo']
        salud = request.form['salud']
        comportamiento = request.form['comportamiento']
        caracteristicas = request.form['caracteristicas']
        color = request.form['color']
        raza = request.form['raza']
        
        # Verificar si se subió una nueva imagen
        imagen = request.files.get('imagen')  
        if imagen:
            img_bytes = imagen.read()
            img_base64 = base64.b64encode(img_bytes).decode('utf-8')  # Convertir la imagen a base64
        else:
            # Si no se sube nueva imagen, mantener la imagen actual
            img_base64 = mascota['imagen']  

        # Actualizar la mascota en la base de datos
        collection.update_one(
            {'_id': ObjectId(id)},
            {'$set': {
                'nombre': nombre,
                'edad': edad,
                'sexo': sexo,
                'salud': salud,
                'comportamiento': comportamiento,
                'caracteristicas': caracteristicas,
                'color': color,
                'raza': raza,
                'imagen': img_base64  
            }}
        )

        
        return redirect(url_for('index', id=id))

    return render_template('editar_mascota.html', mascota=mascota)

@app.route('/detalles/<id>')
def detalles_mascota(id):
    mascota = collection.find_one({'_id': ObjectId(id)})
    return render_template('detalles_mascota.html', mascota=mascota)

@app.route('/eliminar/<id>')
def eliminar_mascota(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(debug=True)