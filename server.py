import os
from flask import Flask, send_from_directory, render_template, redirect, jsonify
from threading import Thread
import time

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

contador = 0

def incrementar_contador():
    global contador
    while True:
        contador += 10
        time.sleep(1)  # Incrementar el contador cada 10 segundos

thread = Thread(target=incrementar_contador)
thread.start()  # Iniciar el hilo para incrementar el contador

@app.route('/')
def index():
    return "<p>Hello, World, me llamou jusemarias10!</p>"

@app.route('/obtener_contador')
def obtener_contador():
    return jsonify({'contador': contador})

@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=port)
