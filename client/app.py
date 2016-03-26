from flask import Flask,json, render_template

app = Flask(__name__)


sensor_list = [\
{'id': 1, 'nome': 'sr04','variavel':'distancia','unidade':'cm',\
'portas':[{'Echo':'int'},{'Trigger':'int'}]},\
{'id':2, 'nome': 'sr05'}, {'id':3, 'nome': 'dht11'}]

@app.route('/')
@app.route('/index')
def index(chartID = 'chart_ID', chart_type = 'bar', chart_height = 350):
  chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
  series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
  title = {"text": 'My Title'}
  xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
  yAxis = {"title": {"text": 'yAxis Label'}}
  return render_template('index.html', chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)

@app.route('/api/sensor/tipos')
def getTipos():
  return json.dumps(sensor_list)

if __name__ == "__main__":
  app.run(debug = True, host='0.0.0.0', port=8080, passthrough_errors=True)