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
dbname='sensores.sqlite'

threads_list = []

sensor_type_list = {\
'sr04': {'variavel':'Distância','unidade':['cm'],'portas':[{'nome':'Echo','valor':'23'},{'nome':'Trigger','valor':'24'}]},\
'sr05': {'variavel':'Distância','unidade':['cm'],'portas':[{'nome':'Echo','valor':'23'},{'nome':'Trigger','valor':'24'}]},\
'dht11':{'variavel':'Temperatura/Umidade','unidade':['%','C'],'portas':[{'nome':'Data','valor':'23'}]},\
'pir':  {'variavel':'Movimento','unidade':['n/a'],'portas':[{'nome':'Data','valor':'23'}]}}

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
  data = request.args.get('data')
  echo = request.args.get('echo')
  trigger = request.args.get('trigger')

  #salvar no banco e retornar o id
  id_sensor = db_insert_sensor((tipo,))

  #inicia uma thread lendo o sensor de Junior
  thread_async = create_async_sensor(id_sensor,tipo, {"data":data, "echo":echo, "trigger":trigger})

  #executar(tipo,portas); -> guardar na variavel global para futura recuperacao. #id, thread
  threads_list.append(thread_async)

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
  #for item in threads_list:
  #  print 'Thread: ' + item.getName() +   'Ativa: ' + str(item.isAlive()) 

  sensor_id = request.args.get('sensor_id')
  sensor_type = db_get_sensor_type(sensor_id)
  variavel = sensor_type_list[sensor_type]["variavel"]
  unidade = sensor_type_list[sensor_type]["unidade"]

  dados = display_data(sensor_id);
  datetimes = []

  primeiro_valor_medido = []
  segundo_valor_medido = []

  unidade1 = unidade[0]
  
  print "Unidade 1: " + unidade1

  for dado in dados:
    datetimes.append(dado[0])       
    print "Unidade do banco " + dado[2]
    if dado[2] == unidade1: 
      print "primeiro"
      primeiro_valor_medido.append(dado[1])
    else:   
      print "segundo valor" 
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
   "series":[{"name": variavel, "data": valores}]}

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
  curs.execute("SELECT * FROM (SELECT time(data) AS data, valor, unidade FROM LOG WHERE id_sensor = (?) ORDER BY data DESC LIMIT 20) ORDER BY data ASC",(sensor_id,))

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
    return None


def delete_data():
  conn=sqlite3.connect(dbname)
  curs=conn.cursor()
  curs.execute("DELETE FROM LOG;")
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
