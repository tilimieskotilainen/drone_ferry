import RPi.GPIO as GPIO
import time 

#test_steps = -40
step_time = 0.03
angle = 10
status = "waiting"


out1 = 13
out2 = 11
out3 = 15
out4 = 12

cur_step = 0


i = 0
positive = 0
negative = 0
y = 0


#Tätä voi justeerata
max_angle = 50

abs_max_steps = 282
abs_max_angle = 55
max_steps = abs_max_steps / 55 * max_angle


GPIO.setmode(GPIO.BOARD)
GPIO.setup(out1,GPIO.OUT)
GPIO.setup(out2,GPIO.OUT)
GPIO.setup(out3,GPIO.OUT)
GPIO.setup(out4,GPIO.OUT)

#Limit switches
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 21 (pos_limit) to be an input pin and set pull-down
GPIO.setup(23, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 23 (neg limit) to be an input pin and set pull-down
GPIO.setup(22, GPIO.IN, pull_up_down=GPIO.PUD_DOWN) # Set pin 21 (pos_limit) to be an input pin and set pull-down

#print ("First calibrate by giving some +ve and -ve values.....")


## Joku träkkää onko middle limiter päällä vai ei. Kun vapautuu, pitää current steppiin lisätä/poistaa 14 askelta


def steer_direction():
    global i
    global positive
    global negative
    global y
    global cur_step
    mid = False

    #Pitää rakentaa joku tsekki joka ottaa aina viimeisimmäin current positionin ja suhteuttaa pyydetyn kulman siihen.

    while True:

        if status != "run":
            GPIO.cleanup()
            print("Cleaned up due to non-run")
            break

        if -angle > max_angle:
            steer_angle = max_angle
        elif -angle < -max_angle:
            steer_angle = -max_angle
        else:
            steer_angle = -angle

        x = int(steer_angle / max_angle * max_steps - cur_step)

        try:
            GPIO.output(out1,GPIO.LOW)
            GPIO.output(out2,GPIO.LOW)
            GPIO.output(out3,GPIO.LOW)
            GPIO.output(out4,GPIO.LOW)

            if x > 0:
                for y in range(x, 0, -1):

                    cur_step = cur_step + 1

                    if GPIO.input(22) == 0:
                        cur_step = max_steps
                        print("Limit 22")
                        print(cur_step)
                        break
                    elif GPIO.input(21) == 0:
                        cur_step = -max_steps
                        print("Limit 21")
                        print(cur_step)
                    elif GPIO.input(23) == 0:
                        cur_step = 0
                        mid = True
                        print("Middle")
                    elif GPIO.input(23) == 1 and mid == True:
                        cur_step = 14
                        mid = False
                        
                    else:
                        pass

                    print("step:", cur_step)



                    if negative == 1:
                        if i==7:
                            i=0
                        else:
                            i = i + 1
                        y = y + 2
                        negative = 0
                    positive = 1
                    #print((x+1)-y)
                    if i==0:
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i==1:
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i==2:  
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i==3:    
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i==4:  
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i==5:
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.HIGH)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i==6:    
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.HIGH)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i==7:    
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.HIGH)
                        time.sleep(step_time)
                        #time.sleep(1)
                    if i==7:
                        i=0
                        continue
                    i=i+1
            
            
            elif x < 0:
                x = x * -1
                for y in range(x, 0, -1):

                    cur_step = cur_step - 1

                    if GPIO.input(22) == 0:
                        cur_step = max_steps
                        print("Limit 22")
                        
                    elif GPIO.input(21) == 0:
                        cur_step = -max_steps
                        print("Limit 21")
                        break
                    
                    elif GPIO.input(23) == 0:
                        cur_step = 0
                        mid = True
                        print("Middle")

                    elif GPIO.input(23) == 1 and mid == True:
                        cur_step = -14
                        mid = False


                    else:
                        pass

                    print("step:", cur_step)

                    if positive == 1:
                        if i == 0:
                            i = 7
                        else:
                            i = i - 1
                        y = y + 3
                        positive = 0
                    negative = 1
                    #print((x+1)-y) 
                    if i == 0:
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i == 1:
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i == 2:  
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i == 3:    
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.HIGH)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i == 4:  
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.LOW)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i == 5:
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.HIGH)
                        GPIO.output(out4,GPIO.HIGH)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i == 6:    
                        GPIO.output(out1,GPIO.LOW)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.HIGH)
                        time.sleep(step_time)
                        #time.sleep(1)
                    elif i == 7:    
                        GPIO.output(out1,GPIO.HIGH)
                        GPIO.output(out2,GPIO.LOW)
                        GPIO.output(out3,GPIO.LOW)
                        GPIO.output(out4,GPIO.HIGH)
                        time.sleep(step_time)
                        #time.sleep(1)
                    if i == 0:
                        i = 7
                        continue
                    i = i - 1

                        
        except KeyboardInterrupt:
            GPIO.cleanup()
            print("Cleaned up on interrupt")

#        GPIO.cleanup()
#        print("Steering done!")
#        return()

#rest_stepper()
if __name__ == "__main__":
    status = "run"
    steer_direction()
