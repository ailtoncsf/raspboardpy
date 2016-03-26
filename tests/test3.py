from concretesensor.srf04 import SRF04

sensor = SRF04(23,24)
print("distancia em cm:")
print(sensor.distance_in_cm())
