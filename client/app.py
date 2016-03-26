#!/env/bin/env python
# -*- coding: utf-8 -*-
import random,datetime
from time import gmtime, strftime
from flask import Flask,json, render_template,request

app = Flask(__name__)


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

sensor_list = [99996,99997,99998,99999]

defaultJson={ "chart" : {  "type": "line", "height": 350},\
"plotOptions": {"series": { "animation": "false"}},\
"series":[{"name": 'Label1', "data": [1,2,3,8]}, {"name": 'Label2', "data": [4, 5, 6,9]}],\
"title":{"text": 'Temperatura (SR04#99999)'},\
"xAxis":{"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']},\
"yAxis":{"title": {"text": 'yAxis Label'}}}

#Dados gerados pelos testes de Ailton
defaultJson={"chart": {"height": 350, "type": "line"}, "legend": {"legend": {"align": "right", "borderWidth": 0, "layout": "vertical", "verticalAlign": "middle"}}, "series": [{"data": [6.75, 6.17, 7.89, 9.92, 9.74, 8.57, 9.28, 8.71, 6.12, 8.47], "name": "HC-SR04"}], "subtitle": {"text": "Medindo distancia", "x": -20}, "title": {"text": "Sensor HC-SR04", "x": -20}, "tooltip": {"tooltip": {"valueSuffix": "cm"}}, "xAxis": {"categories": ["18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53", "18:18:53"]}, "yAxis": {"plotLines": [{"color": "#808080", "value": 0, "width": 1}], "title": {"text": "Distancia (cm)"}}}

@app.route('/')
@app.route('/index')
def index():
  return render_template('index.html')

@app.route('/api/sensor/tipos')
def getTipos():
  return json.dumps(sensor_type_list)


@app.route('/api/sensor/start')
def startSensor():
  tipo = request.args.get('tipo')
  portas = request.args.get('portas')
  return json.dumps(99999)

@app.route('/api/sensor/stop')
def stopSensor():
  sensor_id = request.args.get('sensor_id')
  return json.dumps("STOPPED")


@app.route('/api/sensor/listall')
def listAll():
  return json.dumps(sensor_list)

@app.route('/api/sensor/chart')
def getChart():
  sensor_id = request.args.get('sensor_id')
  defaultJson["series"][0]["data"].append(random.randint(0,99));
  defaultJson["series"][1]["data"].append(random.randint(0,99));
  defaultJson["xAxis"]["categories"].append(strftime("%H:%M:%S",gmtime()))
  if(len(defaultJson["series"][0]["data"]) > 10):
      defaultJson["series"][0]["data"].pop(0)
  if(len(defaultJson["series"][1]["data"]) > 10):
      defaultJson["series"][1]["data"].pop(0)
  if(len(defaultJson["xAxis"]["categories"]) > 10):
      defaultJson["xAxis"]["categories"].pop(0)
  return json.dumps(defaultJson)



if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)