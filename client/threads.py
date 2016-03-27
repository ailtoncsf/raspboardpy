#!/usr/bin/env python
# coding: utf-8
from decorators import async, run_thread
#from concretefactory.ultrasonicSensorFactory import UltrasonicSensorFactory
import time, datetime, random, sqlite3
#import RPi.GPIO

#Arquivo de banco de dados do SQLite
dbname='sensores.sqlite'

#@async
@run_thread
def create_async_sensor(sensor_id, tipo, portas):
    try:
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
            time.sleep(5)
        #finally:
        # print 'Fim'  
        # RPi.GPIO.cleanup() 
      if(tipo == "sr05"):
        #try:
        # srf04 = UltrasonicSensorFactory.createSensor("SRF04")
        # srf04.changeSetup(portas.echo, portas.trigger)
        # srf04.setup()
          while (True):
        #   distancia_cm = srf04.distance_in_cm()
        #   distancia_in = srf04.distance_in_inches()
            distancia_cm = round(random.uniform(5, 10),2)
            gravar_dados_sensor((sensor_id, distancia_cm, "cm", "Distancia", datetime.datetime.now()))
            time.sleep(5)
        #finally:
        # print 'Fim'  
        # RPi.GPIO.cleanup()  

      if(tipo == "pir"):
        #try:
        # srf04 = UltrasonicSensorFactory.createSensor("SRF04")
        # srf04.changeSetup(portas.echo, portas.trigger)
        # srf04.setup()
           while (True):
             #   distancia_cm = srf04.distance_in_cm()
             #   distancia_in = srf04.distance_in_inches()
             moviment = randint(0, 1)
             gravar_dados_sensor((sensor_id, moviment, "n/a", "Movimento", datetime.datetime.now()))
             time.sleep(5)
        #finally:
        # print 'Fim'  
        # RPi.GPIO.cleanup() 

      if(tipo == "dht11"):
        #try:
        # srf04 = UltrasonicSensorFactory.createSensor("SRF04")
        # srf04.changeSetup(portas.echo, portas.trigger)
        # srf04.setup()
          while (True):
        #   distancia_cm = srf04.distance_in_cm()
        #   distancia_in = srf04.distance_in_inches()
            temperature = round(random.uniform(5, 10),2)
            gravar_dados_sensor((sensor_id, temperature, "C", "Temperatura", datetime.datetime.now()))
            humidity = round(random.uniform(5, 10),2)
            gravar_dados_sensor((sensor_id, humidity, "h", "Humidade", datetime.datetime.now()))        
            time.sleep(5)
        #finally:
        # print 'Fim'  
        # RPi.GPIO.cleanup()  
    except (KeyboardInterrupt, SystemExit):
        raise
    except: 
        print "Matando thread"

# store the temperature in the database
def gravar_dados_sensor(values=()):
    conn=sqlite3.connect(dbname)
    cur=conn.cursor()
    query = 'INSERT INTO LOG (id_sensor, valor, unidade, variavel, data) VALUES (%s)' % (
        ', '.join(['?'] * len(values))
    )
    cur.execute(query, values)
    conn.commit()
    id = cur.lastrowid
    cur.close()
    conn.close()
    return id