#!/env/bin/env python
# -*- coding: utf-8 -*-
import random,datetime,sqlite3,ast
from time import gmtime, strftime
from flask import Flask,json, render_template, request
from threads import create_async_sensor
#from concretefactory.ultrasonicSensorFactory import UltrasonicSensorFactory
#import RPi.GPIO

app = Flask(__name__)

#Arquivo de banco de dados do SQLite
dbname='sensores.db'

sensor_type_list = {\
'sr04': {'variavel':'Distância','unidade':'cm','portas':[{'nome':'Echo','valor':'23'},{'nome':'Trigger','valor':'24'}]},\
'sr05': {'variavel':'Distância','unidade':'cm','portas':[{'nome':'Echo','valor':'23'},{'nome':'Trigger','valor':'24'}]},\
'dht11':{'variavel':'Temperatura/Umidade','unidade':'Celsius, N/A','portas':[{'nome':'Data','valor':'23'}]},\
'pir':  {'variavel':'Movimento','unidade':'N/A','portas':[{'nome':'Data','valor':'23'}]}}

sensor_list = []

#Dados gerados pelos testes de Ailton
defaultJson={"chart": {"height": 350, "type": "line"}, 
"legend": {"legend": {"align": "right", "borderWidth": 0, "layout": "vertical", "verticalAlign": "middle"}}, 
"series": [{"data": [6.75, 6.17, 7.89, 9.92, 9.74, 8.57, 9.28, 8.71, 6.12, 8.47], "name": "HC-SR04"}], 
"subtitle": {"text": "Medindo distancia", "x": -20}, "title": {"text": "Sensor HC-SR04", "x": -20}, 
"tooltip": {"tooltip": {"valueSuffix": "cm"}}, 
"xAxis": {"categories": ["18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53"]}, 
"yAxis": {"plotLines": [{"color": "#808080", "value": 0, "width": 1}], "title": {"text": "Distancia (cm)"}}}
    
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
  portas = request.args.get('portas')
    #salvar no banco e retornar o id
  id_sensor = db_insert_sensor((tipo,))
    #inicia uma thread lendo o sensor de Junior
  create_async_sensor(id_sensor,tipo, {"echo": 23, "trigger":24})

    #executar(tipo,portas); -> guardar na variavel global para futura recuperacao. #id, thread
  return json.dumps(id_sensor)

@app.route('/api/sensor/stop')
def stopSensor():
  sensor_id = request.args.get('sensor_id')
  #procurarETerminar(sensor_id)
  return json.dumps("STOPPED")


@app.route('/api/sensor/listall')
def listAll():
  sensor_list = db_get_sensores()


  return json.dumps(sensor_list)

@app.route('/api/sensor/chart')
def getChart():
  sensor_id = request.args.get('sensor_id')
  sensor_type = db_get_sensor_type(sensor_id)
  variavel = ast.literal_eval(sensor_type_list[ast.literal_eval(sensor_type)]["variavel"])
  unidade = sensor_type_list[sensor_type]["unidade"]

  dados = display_data(sensor_id);
  datetimes = []
  valores = []

  for dado in dados:
    datetimes.append(dado[0])
    valores.append(dado[1])

  chartJson = {"chart": {"type": "line", "height": "400"},\
  "title":{"text": "Sensor " + sensor_id + "(" + sensor_type + ")", "x": -20},\
  "subtitle":{"text": "Medindo distancia", "x": -20},\
  "xAxis":{"categories": ast.literal_eval(json.dumps(datetimes))},\
  "yAxis":{"title": {"text": variavel + " (" + unidade+ ")"}, "plotLines": [{"value": 0, "width": 1, "color": '#808080'}]},\
  "tooltip":{"tooltip":{"valueSuffix":  unidade}},\
  "legend":{"legend" : {"layout": 'vertical', "align": "right", "verticalAlign": "middle", "borderWidth": 0}},\
  "series":[{"name": variavel, "data": valores}]}

  return json.dumps(chartJson)

# store the temperature in the database
def db_insert_sensor(values=()):
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
    return id     

# display the contents of the database
def display_data(sensor_id):

  conn=sqlite3.connect(dbname)
  curs=conn.cursor()
  curs.execute("SELECT time(data) as data,valor FROM log WHERE id_sensor = (?) LIMIT 10",(sensor_id,))

  rows=curs.fetchall() 
  return rows  

# display all contents of the table SENSOR
def db_get_sensores():
  conn=sqlite3.connect(dbname)
  curs=conn.cursor()
  curs.execute("SELECT id FROM SENSOR")

  rows=curs.fetchall() 

  ar=[r[0] for r in rows]
  return ar  

# display all contents of the table SENSOR
def db_get_sensor_type(sensor_id):
  conn=sqlite3.connect(dbname)
  curs=conn.cursor()
  curs.execute("SELECT tipo_sensor FROM SENSOR WHERE id = (?) ",(sensor_id,))

  rows=curs.fetchall() 
  ar=[r[0] for r in rows]
  if (len(ar) > 0):
    return  ar[0]
  else:
    return "" 


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

# display the contents of the database
def createSensor():
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

if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)