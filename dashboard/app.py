#!/usr/bin/env python
# coding: utf-8
from flask import Flask, render_template, request, json, jsonify, Response
import sqlite3
import random
import datetime, ast

app = Flask(__name__)

#Arquivo de banco de dados do SQLite
dbname='sensores.db'

sensor_type_list = [\
{'id':1, 'nome': 'sr04','variavel':'Distância','unidade':'cm',\
'portas':[{'nome':'Echo','valor':'23'},{'nome':'Trigger','valor':'24'}]},\
{'id':2, 'nome': 'sr05','variavel':'Distância','unidade':'cm',\
'portas':[{'nome':'Echo','valor':'23'},{'nome':'Trigger','valor':'24'}]},\
{'id':3, 'nome':'dht11','variavel':'Temperatura/Umidade','unidade':'Celsius, N/A',\
'portas':[{'nome':'Data','valor':'23'}]},\
{'id':4, 'nome':  'pir','variavel':'Movimento','unidade':'N/A',\
'portas':[{'nome':'Data','valor':'23'}]}\
]

sensor_list = []

@app.route('/')
@app.route('/index')
def index():

  sensor_list = db_get_sensores()
  return render_template('index.html')

   
@app.route('/api/sensor/tipos')
@app.route('/list_sensors')
def get_list_sensors():
	return json.dumps(sensor_type_list)

@app.route('/api/sensor/listall')
def listAll():
  return json.dumps(sensor_list)

@app.route('/api/sr04')
def addSensorSR04():
  return json.dumps(99999)

@app.route('/api/sr04', methods=('GET', 'POST'))
@app.route('/api/sensor')
@app.route('/sr04', methods=('GET', 'POST'))
def add_sr04(chartID = "sr04", chart_height = 350):
	id_tipo_sensor = request.args.get('id_tipo_sensor')
	echo = request.args.get('echo')
	trigger = request.args.get('trigger')

	#Instanciar a classe de junior passando as informações trigger e echo para o construtor
	#Ex(java) ==> sr04 =  new sr04(echo, trigger)

	#exlcuindo dados de teste
	delete_data()
	
	#gerando 10 registros de testes no banco de dados
	cont = 0
	while (cont < 10):
		distancia = get_distance()
		gravar_dados_sensor((id_tipo_sensor, distancia, 'cm', 'Distancia', datetime.datetime.now()))
		cont = cont + 1

	#apos a gravacao consultar dados e retornar para o cliente
	dados = display_data(id_tipo_sensor) #1
	datetimes = []
	distancias = []

	for dado in dados:
		datetimes.append(dado[4])
		distancias.append(dado[1])

	datetimes = ast.literal_eval(json.dumps(datetimes))


	chartJson = {"chart": {"type": "line", "height": chart_height},\
	"title":{"text": "Sensor HC-SR04", "x": -20},\
	"subtitle":{"text": "Medindo distancia", "x": -20},\
	"xAxis":{"categories": datetimes},\
	"yAxis":{"title": {"text": "Distancia (cm)"}, "plotLines": [{"value": 0, "width": 1, "color": '#808080'}]},\
	"tooltip":{"tooltip":{"valueSuffix": "cm"}},\
	"legend":{"legend" : {"layout": 'vertical', "align": "right", "verticalAlign": "middle", "borderWidth": 0}},\
	"series":[{"name": "HC-SR04", "data": distancias}]}

	return json.dumps(chartJson)


def get_distance():
	return round(random.uniform(5, 10),2)


@app.route('/create')
def create_objects():
	"""
	Este método leva em consideração a não existencia do arquivo de banco de dados
	do SQlite3 no diretório [sensores.db], sendo assim, ele irá criar o banco e as tabelas.
	Obs: Não executar caso o banco já esteja criado, pois será retornada uma msg de erro.
	"""
	try:
		createLog()
		createSensor()
		return 'Tabelas criadas com sucesso.'
	except Exception, e:
		return 'Failed to create Database and tables: '+ str(e)


# display the contents of the database
def display_data(id_tipo_sensor):

	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT id_sensor, valor, unidade, variavel, time(data) FROM log WHERE id_tipo_sensor = (?)",(id_tipo_sensor,))

	rows=curs.fetchall() 
	return rows  

# display all contents of the table SENSOR
def db_get_sensores():

	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT id FROM SENSOR;")

	rows=curs.fetchall() 
	return rows  

def delete_data():
	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("DELETE FROM log;")
	curs.close()
	conn.commit()
	conn.close()
	return True  

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
	        id_sensor 	   VARCHAR(20),
	        valor 		   DECIMAL(10,3),
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
	CREATE TABLE SENSOR (
	        id 			INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
	        tipo_sensor VARCHAR(20)
	);
	""")	
	# desconectando...
	conn.close()


if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)