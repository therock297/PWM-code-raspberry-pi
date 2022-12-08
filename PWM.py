#Importing few libraries that are necassary for this task
import RPi.GPIO as GPIO  #It provide basic interactions with the GPIO pins and enables us to use the cleanup method
import time  #To represent time in code
 
## Using "GPIO" pin numbering
#In this case we use BCM- the GPIO number- rather than the pin number itself
GPIO.setmode(GPIO.BCM) #Basically it tells the library which pin nunbering system you are going to use

LED = 12 #Setting the led to pin no 23 of raspberry pi
GPIO_TRIGGER = 8 #Setting the trigger pin of ultrasonic sensor to gpio pin no. 23 of raspberry pi as to emit the waves
GPIO_ECHO = 10 #Setting the echo pin of ultrasonic sensor to gpio pin no. 10 of raspberry pi as to recieve the emitted waves after reflection

MAX_DISTANCE = 25 #Setting the maximum range of sensor

#Giving GPIO direction
GPIO.setup(GPIO_TRIGGER, GPIO.OUT) #GPIO.OUT as trigger pin would be emiiting waves                
GPIO.setup(GPIO_ECHO, GPIO.IN)  #GPIO.IN as echo pin would be recieving input 
GPIO.setup(LED, GPIO.OUT) #The pin will state in logic level high or low( output voltage 3.3V or 0V)
 
led = GPIO.PWM(LED,100)  #Here setting pulse width modulation  of led to 100  where it would glow to maximum if an object is placed very close to sensor
led.start(0) #Initially LED would be off, assuming no object is placed behind the sensor, so pwm of led at starting set to zero

#Created a distance function which would calculate the distance between the object and the sensor
def distance():
    GPIO.output(GPIO_TRIGGER, True) #As the trigger would emit waves, it is set to true
 
    time.sleep(0.00001) #After 1 second,
    GPIO.output(GPIO_TRIGGER, False)  #It is turned to false, means it would not emit anything

    #Explained below in 34th to 38th line
    StartTime = time.time()
    StopTime = time.time()
 
    while GPIO.input(GPIO_ECHO) == 0: #When echo is zero,
        StartTime = time.time()  #Time of the start of pulse will be saved here
 
    while GPIO.input(GPIO_ECHO) == 1: #When echo is one,
        StopTime = time.time() # Arriving time to the echo will be saved

    #Calculating the distance
    TimeElapsed = StopTime - StartTime
    #Speed of sound in air is 3400cm/s, so it is divided by 2 as the sound would be emitted, collided and recieved by an echo pin. 
    distance = (TimeElapsed * 34000) / 2 
    return distance

try:
	while True:    #Using while loop,
        #Calling the distance function that is implemented above
		dist = distance()
        #Printing the ditance as in one decimal place 
		print ("Measured Distance = %.1f cm" % dist)
		if dist <= MAX_DISTANCE:  #Giving a condition, if distance is less than the maximum distance, then the led will glow
			led.ChangeDutyCycle(100 - (dist/MAX_DISTANCE * 100))
			time.sleep(0.1)
		else:  #Else the led will turn off
			led.ChangeDutyCycle(0)
 
#Giving an exception if any key is pressed,
except KeyboardInterrupt:
    print("Measurement stopped by User") #then it would print the statement

#Led would stop working
led.stop()
GPIO.cleanup() #Lastly it sets up the GPIO pins back to its intital setting

