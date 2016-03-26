#!/env/bin/env python
# -*- coding: utf-8 -*-
from flask import Flask,json, render_template,request

app = Flask(__name__)


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

defaultJson={ "chart" : { "type": "bar", "height": 350},\
"series":[{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}],\
"title":{"text": 'Temperatura (SR04#99999)'},\
"xAxis":{"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']},\
"yAxis":{"title": {"text": 'yAxis Label'}}}

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
def getTipos():
  return json.dumps(sensor_list)


@app.route('/api/sr04')
def addSensorSR04():
  return json.dumps(99999)

@app.route('/api/sensor')
def getChartSR04():
  sensor_id = request.args.get('sensor_id')
  return json.dumps(defaultJson)

@app.route('/api/sensordata')
def getDataSR04():
  sensor_id = request.args.get('sensor_id')
  return json.dumps(defaultJson)

if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)