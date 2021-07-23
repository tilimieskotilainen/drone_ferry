import RpiMotorLib_EKmod
import RPi.GPIO as GPIO


#Limit switches
GPIO.setmode(GPIO.BOARD)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 21 (pos_limit) to be an input pin and set pull-down
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 23 (neg limit) to be an input pin and set pull-down
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 21 (pos_limit) to be an input pin and set pull-down



"""motor_run,  moves stepper motor based on 7 inputs

 (1) GPIOPins, type=list of ints 4 long, help="list of
 4 GPIO pins to connect to motor controller
 These are the four GPIO pins we will
 use to drive the stepper motor, in the order
 they are plugged into the controller board. So,
 GPIO 18 is plugged into Pin 1 on the stepper motor.
 (2) wait, type=float, default=0.001, help=Time to wait
 (in seconds) between steps.
 (3) steps, type=int, default=512, help=Number of steps sequence's
 to execute. Default is one revolution , 512 (for a 28BYJ-48)
 (4) counterclockwise, type=bool default=False
 help="Turn stepper counterclockwise"
 (5) verbose, type=bool  type=bool default=False
 help="Write pin actions",
 (6) steptype, type=string , default=half help= type of drive to
 step motor 3 options full step half step or wave drive
 where full = fullstep , half = half step , wave = wave drive.
 (7) initdelay, type=float, default=1mS, help= Intial delay after
 GPIO pins initialized but before motor is moved.

"""

#define GPIO pins
#GPIO_pins = (13, 11, 15, 12)
GPIO_pins = (15, 12, 13, 11)

def steer(angle):
    
    RpiMotorLib_EKmod.motor_run(GPIO_pins, 0.005, angle, False, "full", 0.05)
    GPIO.cleanup()
    


steer(200)