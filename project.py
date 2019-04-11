# Libraries
import RPi.GPIO as GPIO
import time
import pygame
import pigpio

#GPIO MODE (BOARD / BCM) 
GPIO.setmode(GPIO.BCM)

#set GPIO Pins
GPIO_TRIGGER = 4
GPIO_ECHO = 17

# Light strip pins
RED_PIN   = 22
GREEN_PIN = 23
BLUE_PIN  = 27

# light strip
pi = pigpio.pi()

red_value = 255
green_value = 100
blue_value = 000

min_red = 173
min_green = 20

red = red_value
green = green_value
blue = blue_value

inhale = False

# Servos

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
 
 # ultrasonic sensor 
def distance():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance
    
# light pulse
def pulse():
    global inhale
    global red
    global blue
    global green
    
    if (inhale):
        if red < 253:
            red += 2
        #if blue < 100:
         #   blue += 3
        if green < 253:
            green += 2
    if (not inhale):
        if red > 2:
            red -= 2
        #if blue > 3:
         #   blue -= 3
        if green > 2:
            green -= 2
    if (green >= 100):
        inhale = False
    if (green <= 20):
        inhale = True
        
    pi.set_PWM_dutycycle(RED_PIN, red)
    pi.set_PWM_dutycycle(GREEN_PIN, green)
    pi.set_PWM_dutycycle(BLUE_PIN, blue)

def rest():
    pi.set_PWM_dutycycle(RED_PIN, min_red-10)
    pi.set_PWM_dutycycle(GREEN_PIN, min_green-10)

 
if __name__ == '__main__':
    try:
        # setup sound file
        pygame.mixer.init()
        pygame.mixer.music.load("/home/pi/Downloads/rain-01.mp3")
        pygame.mixer.music.set_volume(1.0)
        pygame.mixer.music.play(-1) 
        
       
        while True:
            dist = distance()
            
            print ("Measured Distance = %.1f cm" % dist)    
            print("Red", red)
            print("Blue", blue)
            print("Green", green)
                        
            # pulse lights
            pulse()
        
            # change states 
            if (dist < 100):
                # TODO play second mp3 file
                rest()
                time.sleep(5)
                
                inhale = False
                green = min_green
                red = min_red
                #blue = blue_value
                
            #time.sleep(.25)
 
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        pi.set_PWM_dutycycle(RED_PIN, 000)
        pi.set_PWM_dutycycle(GREEN_PIN, 000)
        pi.set_PWM_dutycycle(BLUE_PIN, 000)
        pi.stop()
        GPIO.cleanup()
