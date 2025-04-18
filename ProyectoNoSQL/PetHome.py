from flask import Flask, render_template, request, redirect, url_for, jsonify
from pymongo import MongoClient
from bson.objectid import ObjectId
import base64

app = Flask(__name__)

# Conexión a MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client["PetHome"]
collection = db["Mascotas"]

@app.route('/')
def inicio():
    return redirect(url_for('bienvenida'))

@app.route('/index')
def index():
    mascotas = list(collection.find())
    return render_template('index.html', mascotas=mascotas)

@app.route('/agregar', methods=['POST'])
def agregar_mascota():
    nombre = request.form['nombre']
    edad = request.form['edad']
    sexo = request.form['sexo']
    salud = request.form['salud']
    comportamiento = request.form['comportamiento']
    caracteristicas = request.form['caracteristicas']
    color = request.form['color']
    raza = request.form['raza']

    imagen = request.files.get('imagen')
    if imagen:
        img_bytes = imagen.read()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    else:
        img_base64 = "Sin imagen"

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

@app.route('/editar/<id>', methods=['POST'])
def editar_mascota(id):
    mascota = collection.find_one({'_id': ObjectId(id)})
    nombre = request.form['nombre']
    edad = request.form['edad']
    sexo = request.form['sexo']
    salud = request.form['salud']
    comportamiento = request.form['comportamiento']
    caracteristicas = request.form['caracteristicas']
    color = request.form['color']
    raza = request.form['raza']

    imagen = request.files.get('imagen')
    if imagen:
        img_bytes = imagen.read()
        img_base64 = base64.b64encode(img_bytes).decode('utf-8')
    else:
        img_base64 = mascota.get('imagen', "Sin imagen")

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
    return redirect(url_for('index'))

@app.route('/eliminar/<id>', methods=['POST'])
def eliminar_mascota(id):
    collection.delete_one({'_id': ObjectId(id)})
    return redirect(url_for('index'))

@app.route('/detalles/<id>')
def detalles_mascota(id):
    mascota = collection.find_one({'_id': ObjectId(id)})
    return render_template('detalles_mascota.html', mascota=mascota)

# Ruta opcional para obtener los datos de una mascota vía AJAX (si lo requieres)
@app.route('/mascota/<id>')
def get_mascota(id):
    mascota = collection.find_one({'_id': ObjectId(id)})
    mascota['_id'] = str(mascota['_id'])
    return jsonify(mascota)

@app.route('/cuidados')
def cuidados():
    return render_template('cuidados.html')

@app.route("/soporte")
def soporte():
    return render_template("soporte.html")

@app.route("/bienvenida")
def bienvenida():
    mascotas = list(collection.find())  
    return render_template("bienvenida.html", mascotas=mascotas)  

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/register')
def register():
    return render_template('register.html')

@app.route('/detalle_mascota/<id>')
def detalle_mascota(id):
    mascota = collection.find_one({'_id': ObjectId(id)})
    return render_template('detalles_mascota.html', mascota=mascota)

if __name__ == '__main__':
    app.run(debug=True)
