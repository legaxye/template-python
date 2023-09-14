import os
from flask import Flask, send_from_directory, render_template, redirect, jsonify
from threading import Thread
import time
import multiprocessing

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

contador = multiprocessing.Value('i', 0)  # Crear un valor compartido para el contador
contador_queue = multiprocessing.Queue()  # Crear una cola para comunicar el valor del contador

def incrementar_contador():
    global contador
    while True:
        with contador.get_lock():
            contador.value += 10
            contador_queue.put(contador.value)  # Agregar el valor actual del contador a la cola
        time.sleep(1)

thread = Thread(target=incrementar_contador)

@app.route('/')
def index():
    return "<p>Hello, World, me llamou jusss!1</p>"

@app.route('/add/<username>')
def add_user(username):
    return "<p>Hello, " + username + ", me llamou jseeu!</p>"

@app.route('/mostrar_num')
def obtener_contador():
    with contador.get_lock():
        return jsonify({'contador': contador.value})

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    thread.start()  # Iniciar el hilo para incrementar el contador
    app.run(port=port)
