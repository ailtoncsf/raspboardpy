#!/usr/bin/env python
# coding: utf-8
from flask import Flask, render_template, request, json, jsonify, Response
import sqlite3
import random
import datetime, ast

app = Flask(__name__)

#Arquivo de banco de dados do SQLite
dbname='sensores.db'

sensor_list = [\
{'id':1, 'nome': 'sr04','variavel':'Distância','unidade':'cm',\
'portas':[{'nome':'Echo','valor':'23'},{'nome':'Trigger','valor':'24'}]},\
{'id':2, 'nome': 'sr05','variavel':'Distância','unidade':'cm',\
'portas':[{'nome':'Echo','valor':'23'},{'nome':'Trigger','valor':'24'}]},\
{'id':3, 'nome':'dht11','variavel':'Temperatura/Umidade','unidade':'Celsius, N/A',\
'portas':[{'nome':'Data','valor':'23'}]},\
{'id':4, 'nome':  'pir','variavel':'Movimento','unidade':'N/A',\
'portas':[{'nome':'Data','valor':'23'}]}\
]


@app.route('/')
@app.route('/index')
def index(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
  chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
  series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
  title = {"text": 'Temperatura (SR04#9879879)'}
  xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
  yAxis = {"title": {"text": 'yAxis Label'}}
  return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

   
@app.route('/api/sensor/tipos')
@app.route('/list_sensors')
def get_list_sensors():
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

@app.route('/api/dht11', methods=('GET', 'POST'))
def add_dht11(chartID = "dht11", chart_height = 350):
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
		gravar_dados_sensor((id_tipo_sensor, distancia, 'C°/h', 'Temperatura/Umidade', datetime.datetime.now()))
		cont = cont + 1

	#apos a gravacao consultar dados e retornar para o cliente
	dados = display_data(id_tipo_sensor) #3
	datetimes = []
	distancias = []

	for dado in dados:
		datetimes.append(dado[4])
		distancias.append(dado[1])

	datetimes = ast.literal_eval(json.dumps(datetimes))


	chartJson =   chart: {zoomType: 'xy'}, title: {text: 'Average Monthly Temperature and Rainfall in Tokyo'},\
    subtitle: {text: 'Source: WorldClimate.com'},
    xAxis: [{categories: ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun','Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'], crosshair: true}],\
        yAxis: [{ // Primary yAxis
            labels: {
                format: '{value}°C',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            },
            title: {
                text: 'Temperature',
                style: {
                    color: Highcharts.getOptions().colors[1]
                }
            }
        }, { // Secondary yAxis
            title: {
                text: 'Rainfall',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            labels: {
                format: '{value} mm',
                style: {
                    color: Highcharts.getOptions().colors[0]
                }
            },
            opposite: true
        }],
        tooltip: {
            shared: true
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            x: 120,
            verticalAlign: 'top',
            y: 100,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF'
        },
        series: [{
            name: 'Rainfall',
            type: 'column',
            yAxis: 1,
            data: [49.9, 71.5, 106.4, 129.2, 144.0, 176.0, 135.6, 148.5, 216.4, 194.1, 95.6, 54.4],
            tooltip: {
                valueSuffix: ' mm'
            }

        }, {
            name: 'Temperature',
            type: 'spline',
            data: [7.0, 6.9, 9.5, 14.5, 18.2, 21.5, 25.2, 26.5, 23.3, 18.3, 13.9, 9.6],
            tooltip: {
                valueSuffix: '°C'
            }
        }]

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


# store the temperature in the database
def gravar_dados_sensor(values=()):
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    query = 'INSERT INTO log (id_tipo_sensor, valor, unidade, variavel, data) VALUES (%s)' % (
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    conn.commit()
    id = cur.lastrowid
    cur.close()
    conn.close()
    return id

# display the contents of the database
def display_data(id_tipo_sensor):

	conn=sqlite3.connect(dbname)
	curs=conn.cursor()
	curs.execute("SELECT id_tipo_sensor, valor, unidade, variavel, time(data) FROM log WHERE id_tipo_sensor = (?)",(id_tipo_sensor,))

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
	        id_tipo_sensor VARCHAR(20),
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
	        id_tipo_sensor INTEGER
	);
	""")	
	# desconectando...
	conn.close()

if __name__ == "__main__":
    app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)