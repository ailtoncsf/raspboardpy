#!/usr/bin/env python
from flask import Flask, render_template, request, jsonify, json
import sqlite3
import random

app = Flask(__name__)

dbname='sensores.db'
sensor_list = [{'id': 1, 'nome': sr04}, {'id':2, 'nome': sr05}, {'id':3, 'nome': dht11}]


@app.route('/')
@app.route('/index')
def index(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
    chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
    series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
    title = {"text": 'My Title'}
    xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
    yAxis = {"title": {"text": 'yAxis Label'}}
    rs = display_data(None)
    return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis, rs=rs)


@app.route('/list_sensors')
def get_list_sensors():
	return json.dumps(sensor_list)

@app.route('/sr00', methods=('GET', 'POST'))
def addsensor00():
	tipo_sensor = request.args.get('tipo_sensor')
	echo = request.args.get('echo')
	trigger = request.args.get('trigger')

	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
	title = {"text": 'SR-04'}
	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	yAxis = {"title": {"text": 'yAxis Label'}}

    #sr04 = new sr04()
	return tipo_sensor + ' '+ trigger

@app.route('/sr0', methods=('GET', 'POST'))
def addsensor():
	tipo_sensor = request.args.get('tipo_sensor')
	echo = request.args.get('echo')
	trigger = request.args.get('trigger')

    #sr04 = new sr04()
	return tipo_sensor + ' '+ trigger

@app.route('/sr04', methods=('GET', 'POST'))
def add_sr04():
	id_tipo_sensor = request.args.get('id_tipo_sensor')
	echo = request.args.get('echo')
	trigger = request.args.get('trigger')

	cont = 0
	while (cont < 10):
		distancia = get_distance()
		gravar_dados_sensor((id_tipo_sensor, distancia, 'cm', 'Distancia', 'datetime("now")'))
		cont = cont + 1

	dados = display_data(None)
	return jsonify(dados)

def get_distance():
	random.uniform(1.5, 1.9)


@app.route('/create')
def create_objects():
	createLog()
	createTipoSensor()
	createSensor()
	return 'Tabelas criadas com sucesso.'

# store the temperature in the database
def gravar_dados_sensor(values=()):
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    query = 'INSERT INTO log (tipo_sensor, valor, unidade, variavel, data) VALUES (%s)' % (
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    g.db.commit()
    id = cur.lastrowid
    cur.close()
    return id

# store the temperature in the database
def gravar_dados(tipo_sensor, valor, unidade, variavel, data):

	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute('''INSERT INTO log (id_tipo_sensor, valor, unidade, variavel, data)
	values (%s, %s, %s, %s, %s)''',
	(tipo_sensor, valor, unidade, variavel, data))         		  
	# commit the changes
	conn.commit()

	conn.close()

# display the contents of the database
def display_data(interval):

    conn=sqlite3.connect(dbname)
    curs=conn.cursor()

    if interval == None:
        curs.execute("SELECT * FROM log;")
    else:
        curs.execute("SELECT * FROM temps WHERE timestamp > datetime('now','-%s hours')" % interval)

    rows=curs.fetchall() 
    return rows  


# display the contents of the database
def createLog():
	# conectando...
	conn = sqlite3.connect(dbname)
	# definindo um cursor
	cursor = conn.cursor()

	# criando a tabela (schema)
	cursor.execute("""
	CREATE TABLE log (
	        id 			   INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	        id_tipo_sensor VARCHAR(20),
	        valor 		   NUMERIC,
	        unidade        VARCHAR(20),
	        variavel 	   VARCHAR(20),
	        data 		   TIMESTAMP
	);
	""")
	# desconectando...
	conn.close()

# display the contents of the database
def createSensor():
	# conectando...
	conn = sqlite3.connect(dbname)
	# definindo um cursor
	cursor = conn.cursor()

	# criando a tabela (schema)
	cursor.execute("""
	CREATE SENSOR (
	        id 			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	        id_tipo_sensor INTEGER
	);
	""")	
	# desconectando...
	conn.close()

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)