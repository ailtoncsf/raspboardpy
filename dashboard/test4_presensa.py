import RPi.GPIO  
import time  
RPi.GPIO.setmode(RPi.GPIO.BCM)  
RPi.GPIO.setup(23, RPi.GPIO.IN)  
sensor=0  
try:  
	while True:  
		sensor=RPi.GPIO.input(23)  
		if(sensor):  
			print "Movimento"  
     		else:  
			print sensor  
     		time.sleep(1)  
finally:  
	print 'Fim'  
	RPi.GPIO.cleanup()  
