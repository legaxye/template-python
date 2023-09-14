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
contador = multiprocessing.Value('i', 0)
#end

@app.route('/add/<username>')
def add_user(username):
    return "<p>Hello, " + username + ", me llamou jseeu!</p>"
    
@app.route('/static/<path:path>')
def serve_static(path):
    return send_from_directory('static', path)

@app.route('/')
def home():
   return "<p>Hello, World, me llamou jusss!</p>"

@app.route('/<path:path>')
def all_routes(path):
    return redirect('/')

if __name__ == "__main__":
    app.run(port=port)
