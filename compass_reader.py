from i2clibraries import i2c_hmc5883l
import time
import math
import json

hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)

PI = 3.14159265
eranto = 9

of = open("compass_offsets.txt") #Open file that contains offsets
offsets = json.loads(of.read())
of.close()

heading = 0

def read_compass():

    print("Compass running")
    
    hmc5883l.setContinuousMode()
    
    global heading

    while True:
        (x, y, z) = hmc5883l.getAxes()
        
        x = x - offsets["x_offset"]
        y = y - offsets["y_offset"]
        
        
        if y == 0:
            if x < 0:
                head = -90
            else:
                head = 90

        elif y > 0:
            if x > 0:
                head = 180 - math.atan(x/y) * 180/PI
            else:
                head = -180 - math.atan(x/y) * 180/PI
        elif y < 0:
            head = - math.atan(x/y) * 180/PI

        heading = -head + eranto #For some reason heading is reversed after calculations and hence head is here with a negative sign
        
        if heading > 180:
            heading = heading - 360
            
#        print(heading)
        
#        if once == True:
#            return(heading)

        time.sleep(0.1)
        
if __name__ == "__main__":
    read_compass()