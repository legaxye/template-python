import os
from flask import Flask, send_from_directory, render_template, redirect, jsonify
from threading import Thread
import time
#ini
import sys
from bs4 import BeautifulSoup
import cloudscraper
import mysql.connector
#end

app = Flask(__name__)

port = int(os.environ.get("PORT", 5000))

contador = 0
previous_data = []
#ini
# Crear el scraper
scraper = cloudscraper.create_scraper()

# Configurar la conexión a MySQL
db_config = {
    "host": "aws.connect.psdb.cloud",
    "user": "h2vv32vi9ys4q5ng68ej",
    "password": "pscale_pw_LfdWgDZPn2RfBzxP653ngJdowhaJaatgdpDjVGJdynK",
    "database": "clanwarxye"
}

# Crear la conexión a MySQL
conn = mysql.connector.connect(**db_config)
cursor = conn.cursor()
# Función para borrar el contenido de la tabla MySQL
def clear_table():
    query = "DELETE FROM NBTF"
    cursor.execute(query)
    conn.commit()

# Función para insertar datos en la tabla de MySQL
def insert_data_to_mysql(data):
    query = "INSERT INTO NBTF (Name, Level, Reputation, RepChange) VALUES (%s, %s, %s, %s) ON DUPLICATE KEY UPDATE  Reputation=VALUES(Reputation), RepChange=VALUES(RepChange)"
    cursor.executemany(query, data)
    conn.commit()

# Función para actualizar los datos de reputación y Rep Change
def update_data():
    # Obtener la resderpuesta
    response = scraper.get("https://ninjalegends.net/detail_clan.php?clan_id=3042")

    # Parsear la respuesta con Beautiful Soup
    soup = BeautifulSoup(response.text, 'html.parser')

    # Encontrar la tabla de datos
    table = soup.find('table', class_='tt-cln table-vw-clan')

    if table:
        current_data = []
        total_rep_change = 0
        
        # Iterar a través de las filas de la tabla
        for row in table.find_all('tr'):
            cells = row.find_all('td')
            if len(cells) >= 3:  # Asegurarse de que hay suficientes celdas en la fila
                name = cells[0].text
                level = cells[1].text
                reputation = int(cells[2].text)
                rep_change = 0
                
                # Buscar el elemento correspondiente en el estado anterior y calcular el cambio de reputación
                for prev_entry in previous_data:
                    if prev_entry[0] == name:
                        rep_change = reputation - prev_entry[2]
                        total_rep_change += rep_change
                        break
                
                current_data.append([name, level, reputation, rep_change])
        
        
        
        # Insertar o actualizar datos en la tabla MySQL
        insert_data_to_mysql(current_data)
        
        # Actualizar la lista de datos anteriores
        previous_data.clear()
        previous_data.extend(current_data)
    
    else:
        print("No data available")
#end

def incrementar_contador():
    global contador
    while True:
        update_data()
        time.sleep(10)  # Incrementar el contador cada 10 segundos

thread = Thread(target=incrementar_contador)
thread.start()  # Iniciar el hilo para incrementar el contador

clear_table()

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
