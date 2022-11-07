import RPi.GPIO as GPIO
import time
 
GPIO.setmode(GPIO.BCM)

LED = 12
GPIO_TRIGGER = 8
GPIO_ECHO = 10

MAX_DISTANCE = 25

GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(LED, GPIO.OUT) 
 
led = GPIO.PWM(LED,100)
led.start(0)

def distance():
    GPIO.output(GPIO_TRIGGER, True)
 
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    TimeElapsed = StopTime - StartTime
    distance = (TimeElapsed * 34000) / 2
 
    return distance

try:
	while True:
		dist = distance()
		print ("Measured Distance = %.1f cm" % dist)
		if dist <= MAX_DISTANCE:
			led.ChangeDutyCycle(100 - (dist/MAX_DISTANCE * 100))
			time.sleep(0.1)
		else:
			led.ChangeDutyCycle(0)
 
except KeyboardInterrupt:
    print("Measurement stopped by User")
    
led.stop()
GPIO.cleanup()

