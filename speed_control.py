import RPi.GPIO as GPIO
import time
  
GPIO.setmode(GPIO.BOARD)
GPIO.setup(33, GPIO.OUT)
GPIO.setup(35, GPIO.OUT)
GPIO.output(33, GPIO.LOW)
GPIO.output(35, GPIO.LOW)
pwm_fwd = GPIO.PWM(33, 1000) # Set Frequency to 1 KHz
pwm_rev = GPIO.PWM(35, 1000)
pwm_fwd.start(0) # Set the starting Duty Cycle
pwm_rev.start(0)


def propulsion(speed):
    
    if speed > 0:
        pwm_rev.ChangeDutyCycle(0)
        pwm_fwd.ChangeDutyCycle(speed)
    elif speed < 0:
        pwm_fwd.ChangeDutyCycle(0)
        pwm_rev.ChangeDutyCycle(-speed)
    else:
        pwm_fwd.ChangeDutyCycle(0)
        pwm_rev.ChangeDutyCycle(0)

#    time.sleep(3)
    
#    pwm_fwd.ChangeDutyCycle(0)
#    pwm_rev.ChangeDutyCycle(0)

def stop():
    pwm_fwd.ChangeDutyCycle(0)
    pwm_rev.ChangeDutyCycle(0)
    GPIO.cleanup()
    print("Stopped")
     
if  __name__ == '__main__':
    propulsion(10)