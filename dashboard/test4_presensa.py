import RPi.GPIO  
import time,datetime

dateString='%d/%m/%Y %H:%M:%S' 
 
RPi.GPIO.setmode(RPi.GPIO.BCM)  
RPi.GPIO.setup(23, RPi.GPIO.IN)  
sensor=0  
try:  
	while True:  
		sensor=RPi.GPIO.input(23)
		print "\n"
		print "sensor_id XX"
                print "sensor_tipo: PIR"
                print "sensor_porta: ",23
                print "log_variavel: presensa"
             
		if(sensor):  
			print "log_valor: ",True
     		else:  
                        print "log_valor: ",False
                print "log_unidade:","n/a"
                print "log_data:",datetime.datetime.now().strftime(dateString)  
     		time.sleep(1)  
finally:  
	print 'Fim'  
	RPi.GPIO.cleanup()  
