import RPi.GPIO as GPIO          
from time import sleep
import board
import busio
import adafruit_vl53l0x
import time

rel_bearing = 0 

tof_straight = 105
tof_toler = 5

tof_left = 85
tof_right = 125


i2c = busio.I2C(board.SCL, board.SDA)
vl53 = adafruit_vl53l0x.VL53L0X(i2c)

in1 = 18 #OK23
in2 = 27 #OK23
en = 17 #OK23
temp1=1

GPIO.setmode(GPIO.BCM)
GPIO.setup(in1,GPIO.OUT)
GPIO.setup(in2,GPIO.OUT)
GPIO.setup(en,GPIO.OUT)
GPIO.output(in1,GPIO.LOW)
GPIO.output(in2,GPIO.LOW)
p=GPIO.PWM(en,1000)
p.start(25)
print("\n")
print("The default speed & direction of motor is LOW & Forward.....")
print("r-run s-stop f-forward b-backward l-low m-medium h-high e-exit")
print("\n")    

x = "s"

while True:

#    x=raw_input()

    tof = vl53.range
    print("TOF:", tof)

#jäi kesken kirjoittaa ehdot kääntämiselle

    if rel_bearing < 0:
        if tof > tof_left:
            x = "b"
        elif tof <= tof_left - tof_toler:
           x = "f"
        else:
           x = "s"

    if rel_bearing > 0:
        if tof < tof_right:
          x = "f"
        elif tof >= tof_right + tof_toler:
          x = "b"
        else:
          x = "s"

    if rel_bearing == 0:
        if tof > tof_straight:
          x = "b"
        elif tof < tof_straight:
          x = "f"
        elif tof == tof_straight:
          x = "s"

    if x=='r':
        print("run")
        if(temp1==1):
         GPIO.output(in1,GPIO.HIGH)
         GPIO.output(in2,GPIO.LOW)
         print("forward")
         x='z'
        else:
         GPIO.output(in1,GPIO.LOW)
         GPIO.output(in2,GPIO.HIGH)
         print("backward")
         x='z'


    elif x=='s':
        print("stop")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.LOW)
#        x='z'

    elif x=='f':
        print("forward")
        GPIO.output(in1,GPIO.HIGH)
        GPIO.output(in2,GPIO.LOW)
        temp1=1
#        x='z'

    elif x=='b':
        print("backward")
        GPIO.output(in1,GPIO.LOW)
        GPIO.output(in2,GPIO.HIGH)
        temp1=0
#        x='z'
     
    
    elif x=='e':
        GPIO.cleanup()
        break
    
    else:
        print("Problem with running steering motor")

    time.sleep(0.5)