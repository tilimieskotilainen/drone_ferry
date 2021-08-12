from i2clibraries import i2c_hmc5883l
import time
import math
import json

hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)

PI = 3.14159265
eranto = 9 #magnetic declination in Espoo (called eranto in Finnish)

of = open("compass_offsets.txt") #Open file that contains offsets, saved by the calibration utility
offsets = json.loads(of.read()) #Read the JSON data from the file and store as dictionary called "offsets"
of.close() #Close file

heading = 0 #Initiate variable for heading

def read_compass():

    print("Compass running")
    
    hmc5883l.setContinuousMode()
    
    global heading #declare global variable to be able to change it's value within this function

    #Start loop to read compass again and again
    while True:
        (x, y, z) = hmc5883l.getAxes() #Read values from compass and save as variables x, y and z
        
        x = x - offsets["x_offset"] #Make adjustment for x-offset according to offset value read from file above
        y = y - offsets["y_offset"] #Make adjustment for y-offset according to offset value read from file above
        
        print("X:", x, "/ Y:", y)
        
        #In situations where y is zero we cannot use our trigonometry formulas, as division by zero makes the code crash
        #In these cases heading is always either -90 or 90 depending on whether x is negative or positive
        #Heading before making the magnetic declination adjustment is saved as variable head
        if y == 0:
            if x < 0:
                head = -90
            else:
                head = 90

        #In situations where y is positive, there are two scenarios to give us the type of heading we want (from zero to -180 for left and 0 to 180 for right)
        #The math.atan method returns the angle in radian, so we have to multiply it by 180/PI to convert it into degrees
        #In my case the y-axis values are reversed and I have to treat the angles a bit funny in my code
        elif y > 0:
            head = math.atan(x/y) * 180/PI

        elif y < 0:
            if x > 0:
                head = 180 + math.atan(x/y) * 180/PI
            else:
                head = -180 - math.atan(x/y) * 180/PI
            
        #Heading is calculated by adding the magnetic declination in Espoo to the result from our raw trigonometry
        heading = head + eranto
        
        #Another adjustment in case the heading is over 180, in which case we need to flip it to the range between 0 and -180
        if heading > 180:
            heading = heading - 360
            
        print(heading)

        #Wait 0.1 seconds before reading the compass again
        time.sleep(0.1)
        
#For testing the code, call the read_compass function on load if this script is being executed standalone, ie not from another script.
if __name__ == "__main__":
    read_compass()
