import sys
import time
import RPi.GPIO as GPIO
import threading

GPIO.setmode(GPIO.BOARD) #Changed by EK
GPIO_pins = (15, 12, 13, 11)
gpiopins = GPIO_pins

GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 21 (pos_limit) to be an input pin and set pull-down
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 23 (neg limit) to be an input pin and set pull-down
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 21 (pos_limit) to be an input pin and set pull-down

left_lim = GPIO.input(22)
mid_lim = GPIO.input(23)
right_lim = GPIO.input(21)

cur_step = 0
wait = 0.005
initdelay = 0.05
steptype = "full"


def steer_direction(target):
    
    global cur_step
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
    try:
        for pin in GPIO_pins:
            GPIO.setup(pin, GPIO.OUT)
            GPIO.output(pin, False)
        time.sleep(initdelay)

        # select step based on user input
        # Each step_sequence is a list containing GPIO pins that should be set to High
        if steptype == "half":  # half stepping.
            step_sequence = list(range(0, 8))
            step_sequence[0] = [gpiopins[0]]
            step_sequence[1] = [gpiopins[0], gpiopins[1]]
            step_sequence[2] = [gpiopins[1]]
            step_sequence[3] = [gpiopins[1], gpiopins[2]]
            step_sequence[4] = [gpiopins[2]]
            step_sequence[5] = [gpiopins[2], gpiopins[3]]
            step_sequence[6] = [gpiopins[3]]
            step_sequence[7] = [gpiopins[3], gpiopins[0]]
        elif steptype == "full":  # full stepping.
            step_sequence = list(range(0, 4))
            step_sequence[0] = [gpiopins[0], gpiopins[1]]
            step_sequence[1] = [gpiopins[1], gpiopins[2]]
            step_sequence[2] = [gpiopins[2], gpiopins[3]]
            step_sequence[3] = [gpiopins[0], gpiopins[3]]
        elif steptype == "wave":  # wave driving
            step_sequence = list(range(0, 4))
            step_sequence[0] = [gpiopins[0]]
            step_sequence[1] = [gpiopins[1]]
            step_sequence[2] = [gpiopins[2]]
            step_sequence[3] = [gpiopins[3]]
        else:
            print("Error: unknown step type ; half, full or wave")
            quit()
            
        step_sequence_rev = step_sequence.copy()
        step_sequence_rev.reverse()


        


        # Iterate through the pins turning them on and off.
        while True:
            
            if GPIO.input(22) == 0:
                cur_step = -4880
                print("Right limit")
            if GPIO.input(21) == 0:
                print("Left limit")
                cur_step = 4900

            if GPIO.input(23) == 0:
                print("Middle")
                cur_step = 0
            
            if target[0] - cur_step < -10 and GPIO.input(22) == 1:

                for pin_list in step_sequence_rev:
                    for pin in gpiopins:
                        if pin in pin_list:
                            GPIO.output(pin, True)
                        else:
                            GPIO.output(pin, False)
                    time.sleep(wait)
                    cur_step = cur_step - 1
                    
            elif target[0] - cur_step > 10 and GPIO.input(21) == 1:

                for pin_list in step_sequence:
                    for pin in gpiopins:
                        if pin in pin_list:
                            GPIO.output(pin, True)
                        else:
                            GPIO.output(pin, False)
                    time.sleep(wait)
                    cur_step = cur_step +1
            

            print(cur_step)
            

    finally:
        # switch off pins at end
        for pin in gpiopins:
            GPIO.output(pin, False)

if __name__ == "__main__":
    test = [0]
    steering_thread = threading.Thread(target=steer_direction, args=(test,), daemon=True)
    steering_thread.start() # Start compass thread
    while True:
        print("Enter target angle")
        test[0] = int(input())
    
