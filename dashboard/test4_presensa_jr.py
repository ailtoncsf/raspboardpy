from concretefactory.motionSensorFactory import MotionSensorFactory
import time

if __name__ == '__main__':

    pir = MotionSensorFactory.createSensor("PIR")
    pir.changeSetup(23)
    pir.setup()
    while (True):
        if (pir.isMotionDetected() == True):
            print ("Motion Detected:")
        # Wait for 10 milliseconds
        time.sleep(0.01)

