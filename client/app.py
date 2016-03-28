#!/env/bin/env python
# -*- coding: utf-8 -*-
import random,datetime,sqlite3,ast
from time import gmtime, strftime
from flask import Flask,json, render_template, request
from threads import create_async_sensor
import threading
from flask_socketio import SocketIO

try:
	app = Flask(__name__)
	socketio = SocketIO(app)

	#Arquivo de banco de dados do SQLite
	dbname='sensores.sqlite'
	condition = threading.Condition();

	threads_list = {}
	sensor_list = []
	sensor_type_list = {\
	'sr04': {'variavel':'Distância','unidade':['cm'],'echo':'23','trigger':'24'},\
	'sr05': {'variavel':'Distância','unidade':['cm'],'echo':'23','trigger':'24'},\
	'dht11':{'variavel':'Temperatura/Umidade','unidade':['%','C'],'data':'23'},\
	'pir':  {'variavel':'Movimento','unidade':['n/a'],'data':'23'}}


	@app.route('/')
	@app.route('/index')
	def index():
		return render_template('index.html')

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

	@app.route('/api/sensor/tipos')
	def getTipos():
		return json.dumps(sensor_type_list)


	@app.route('/api/sensor/start')
	def startSensor():

		tipo = request.args.get('tipo')
		data = request.args.get('data')
		echo = request.args.get('echo')
		trigger = request.args.get('trigger')

		#salvar no banco e retornar o id
		sensor_id = db_insert_sensor((tipo,))

		#inicia uma thread lendo o sensor de Junior
		thread_async = create_async_sensor(condition,sensor_id,tipo, {"data":data, "echo":echo, "trigger":trigger},getChart_CallbackEvent)

		#executar(tipo,portas); -> guardar na variavel global para futura recuperacao. #id, thread
		threads_list[sensor_id] = thread_async

		return json.dumps(sensor_id)

	@app.route('/api/sensor/stop')
	def stopSensor():
		sensor_id = ast.literal_eval(request.args.get('sensor_id'))
		print threads_list
		if (len(threads_list) > 0):
			if ( threads_list[sensor_id] is not None):
				#threads_list[sensor_id]._stop();
				del threads_list[sensor_id]
		db_delete_sensor(sensor_id)
		return listAll()


	@app.route('/api/sensor/listall')
	def listAll():
		sensor_list = db_get_sensores()

		return json.dumps(sensor_list)

	@app.route('/api/sensor/chart')
	def getChartAjax():
		sensor_id = request.args.get('sensor_id')
		return getChart(sensor_id)

		#Utilizado pelo socketio
	def getChart_CallbackEvent(sensor_id):
		socketio.emit('response_api_sensor_chart', getChart(str(sensor_id)))

	def getChart(sensor_id):
		#for item in threads_list:
		#  print 'Thread: ' + item.getName() +   'Ativa: ' + str(item.isAlive()) 
		sensor_type = db_get_sensor_type(sensor_id)
		if (sensor_type is None):
			return json.dumps({})
		else:
			variavel = sensor_type_list[sensor_type]["variavel"]
			unidade = sensor_type_list[sensor_type]["unidade"]

			dados = display_data(sensor_id);
			datetimes = []

			primeiro_valor_medido = []
			segundo_valor_medido = []

			unidade1 = unidade[0]
			
			#print "Unidade 1: " + unidade1

			for dado in dados:
				datetimes.append(dado[0])       
				#print "Unidade do banco " + dado[2]
				if dado[2] == unidade1: 
					#print "primeiro"
					primeiro_valor_medido.append(dado[1])
				else:   
					#print "segundo valor" 
					segundo_valor_medido.append(dado[1]) 

			if(sensor_type == "sr04"):
				chartJson = {"chart": {"type": "line", "height": "400"},\
				"title":{"text": "Sensor " + sensor_id + "(" + sensor_type.upper() + ")", "x": -20},\
				"subtitle":{"text": "Medindo " + variavel, "x": -20},\
				"xAxis":{"categories": ast.literal_eval(json.dumps(datetimes))},\
				"yAxis":{"title": {"text": variavel + " (" + unidade1 + ")"}, "plotLines": [{"value": 0, "width": 1, "color": '#808080'}]},\
				"tooltip":{"tooltip":{"valueSuffix":  unidade1}},\
				"legend":{"legend" : {"layout": 'vertical', "align": "right", "verticalAlign": "middle", "borderWidth": 0}},\
				"series":[{"name": variavel, "data": primeiro_valor_medido}]}

			if(sensor_type == "sr05"):
				chartJson = {"chart": {"type": "line", "height": "400"},\
				"title":{"text": "Sensor " + sensor_id + "(" + sensor_type.upper() + ")", "x": -20},\
				"subtitle":{"text": "Medindo " + variavel, "x": -20},\
				"xAxis":{"categories": ast.literal_eval(json.dumps(datetimes))},\
				"yAxis":{"title": {"text": variavel + " (" + unidade1 + ")"}, "plotLines": [{"value": 0, "width": 1, "color": '#808080'}]},\
				"tooltip":{"tooltip":{"valueSuffix":  unidade1}},\
				"legend":{"legend" : {"layout": 'vertical', "align": "right", "verticalAlign": "middle", "borderWidth": 0}},\
				"series":[{"name": variavel, "data": primeiro_valor_medido}]}

			if(sensor_type == "pir"):
				chartJson = {"chart": {"type": "bar", "height": "400"},\
				"title":{"text": "Sensor " + sensor_id + "(" + sensor_type.upper() + ")", "x": -20},\
				"subtitle":{"text": "Medindo " + variavel, "x": -20},\
				"xAxis":{"categories": ast.literal_eval(json.dumps(datetimes))},\
				"yAxis":{"title": {"text": variavel + " (" + unidade1 + ")"}, "plotLines": [{"value": 0, "width": 1, "color": '#808080'}]},\
				"tooltip":{"tooltip":{"valueSuffix":  unidade1 }},\
				"legend":{"legend" : {"layout": 'vertical', "align": "right", "verticalAlign": "middle", "borderWidth": 0}},\
				"series":[{"name": variavel, "data": primeiro_valor_medido}]}

			if(sensor_type == "dht11"):
				chartJson =  {"chart": {
								"zoomType": 'xy'
						},
						"title": {
								"text": "Sensor " + sensor_id + "(" + sensor_type.upper() + ")"
						},
						"subtitle": {
								"text": "Medindo " + variavel
						},
						"xAxis": [{
								"categories": ast.literal_eval(json.dumps(datetimes)),
								"crosshair": "true"
						}],
						"yAxis": [{ 
								"labels": {
										"format": '{value}°C',
										"style": {
												"color": "#808060"
										}
								},
								"title": {
										"text": 'Temperatura',
										"style": {
												"color": "#808060"
										}
								}
						}, { 
								"title": {
										"text": 'Humidade',
										"style": {
												"color": "#805050"
										}
								},
								"labels": {
										"format": '{value} h',
										"style": {
										"color": "#805050"
										}
								},
								"opposite": "true"
						}],
						"tooltip": {
								"shared": "true"
						},
						"legend": {
								"layout": 'vertical',
								"align": 'left',
								"x": 120,
								"verticalAlign": 'top',
								"y": 100,
								"floating": "true",
								"backgroundColor": '#FFFFFF'
						},
						"series": [{
								"name": 'Humidade',
								"type": 'column',
								"yAxis": 1,
								"data": primeiro_valor_medido,
								"tooltip": {
										"valueSuffix": ' h'
								}

						}, {
								"name": 'Temperatura',
								"type": 'spline',
								"data": segundo_valor_medido,
								"tooltip": {
										"valueSuffix": '°C'
								}
						}]}

			return json.dumps(chartJson)

	# store the temperature in the database
	def db_insert_sensor(values=()):
			condition.acquire()
			conn=sqlite3.connect(dbname)
			cur=conn.cursor()
			query = 'INSERT INTO sensor (tipo_sensor) VALUES (%s)' % (
					', '.join(['?'] * len(values))
			)
			cur.execute(query, values)
			conn.commit()
			id = cur.lastrowid
			cur.close()
			conn.close()
			condition.notify()
			condition.release()
			return id     

	# display the contents of the database
	def display_data(sensor_id):
		condition.acquire()
		conn=sqlite3.connect(dbname)
		curs=conn.cursor()
		curs.execute("SELECT * FROM (SELECT time(data) AS data, valor, unidade FROM LOG WHERE id_sensor = (?) ORDER BY data DESC LIMIT 20) ORDER BY data ASC",(sensor_id,))
		rows=curs.fetchall() 
		condition.notify()
		condition.release()
		return rows  

	# display all contents of the table SENSOR
	def db_get_sensores():
		condition.acquire()
		conn=sqlite3.connect(dbname)
		curs=conn.cursor()
		curs.execute("SELECT id FROM SENSOR")
		rows=curs.fetchall() 
		condition.notify()
		condition.release()

		ar=[r[0] for r in rows]
		return ar  

	# display all contents of the table SENSOR
	def db_get_sensor_type(sensor_id):
		condition.acquire()
		conn=sqlite3.connect(dbname)
		curs=conn.cursor()
		curs.execute("SELECT tipo_sensor FROM SENSOR WHERE id = (?) ",(sensor_id,))
		rows=curs.fetchall() 
		condition.notify()
		condition.release()
		ar=[r[0] for r in rows]
		if (len(ar) > 0):
			return  ar[0]
		else:
			return None

	# display all contents of the table SENSOR
	def db_delete_sensor(sensor_id):
		condition.acquire()
		conn=sqlite3.connect(dbname)
		curs=conn.cursor()
		curs.execute("DELETE FROM SENSOR WHERE id = (?) ",(sensor_id,))
		curs.execute("DELETE FROM LOG WHERE id_sensor = (?) ",(sensor_id,))
		conn.commit()
		curs.close()
		conn.close()
		condition.notify()
		condition.release()
		return True


	def delete_data():
		condition.acquire()
		conn=sqlite3.connect(dbname)
		curs=conn.cursor()
		curs.execute("DELETE FROM LOG;")
		curs.close()
		conn.commit()
		conn.close()
		condition.notify()
		condition.release()
		return True  

	# display the contents of the database
	def createLog():
		condition.acquire()
		# conectando...
		conn = sqlite3.connect(dbname)
		# definindo um cursor
		cursor = conn.cursor()

		# criando a tabela (schema)
		cursor.execute("""
		CREATE TABLE LOG (
						id         INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						id_sensor      VARCHAR(20),
						valor        DECIMAL(10,3),
						unidade        VARCHAR(20),
						variavel     VARCHAR(20),
						data       TIMESTAMP
		);
		""")
		# desconectando...
		conn.close()
		condition.notify()
		condition.release()

	# display the contents of the database
	def createSensor():
		condition.acquire()
		# conectando...
		conn = sqlite3.connect(dbname)
		# definindo um cursor
		cursor = conn.cursor()

		# criando a tabela (schema)
		cursor.execute("""
		CREATE TABLE SENSOR (
						id      INTEGER NOT NULL PRIMARY KEY AUTOINCREMENT,
						tipo_sensor VARCHAR(20)
		);
		""")  
		# desconectando...
		conn.close()
		condition.notify()
		condition.release()

	if __name__ == "__main__":
		socketio.run(app,host='0.0.0.0', port=8080,debug = True)
except IOError as e:
	print e
	if e.errno == errno.EPIPE:
		pass
