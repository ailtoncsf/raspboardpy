#!/usr/bin/env python
# coding: utf-8
from decorators import async
#from concretefactory.ultrasonicSensorFactory import UltrasonicSensorFactory
import datetime
#import RPi.GPIO

#Arquivo de banco de dados do SQLite
dbname='sensores.db'

@async
def create_async_sensor(sensor_id, tipo, portas):

  if(tipo == "sr04"):
    #try:
    # srf04 = UltrasonicSensorFactory.createSensor("SRF04")
    # srf04.changeSetup(portas.echo, portas.trigger)
    # srf04.setup()
      while (True):
    #   distancia_cm = srf04.distance_in_cm()
    #   distancia_in = srf04.distance_in_inches()
        distancia_cm = round(random.uniform(5, 10),2)
        gravar_dados_sensor((sensor_id, distancia_cm, "cm", "Distancia", datetime.datetime.now()))
    #finally:
    # print 'Fim'  
    # RPi.GPIO.cleanup()  

# store the temperature in the database
def gravar_dados_sensor(values=()):
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    query = 'INSERT INTO log (id_sensor, valor, unidade, variavel, data) VALUES (%s)' % (
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    conn.commit()
    id = cur.lastrowid
    cur.close()
    conn.close()
    return id