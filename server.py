import os
from flask import Flask, send_from_directory, render_template, redirect
#ini
from flask import Blueprint, jsonify
from threading import Thread
import time
import multiprocessing
#end
app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

#ini
contador = multiprocessing.Value('i', 0) # Crear un valor compartido para el contador
def incrementar_contador():
    global contador
    while True:
        with contador.get_lock():
            contador.value += 10
        time.sleep(10)
thread = Thread(target=incrementar_contador)
@app.route('/')
def index():
    return "<p>Hello, World, me llamou jusss!</p>"

@app.route('/add/<username>')
def add_user(username):
    return "<p>Hello, " + username + ", me llamou jseeu!</p>"

@app.route('/mostrar_num')
def obtener_contador():
    with contador.get_lock():
        return jsonify({'contador': contador.value})
#end

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
   return render_template('index.html')

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=port)
