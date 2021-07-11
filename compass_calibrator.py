from i2clibraries import i2c_hmc5883l
import time
import math
import json
#import pixel_display
import steering_servo
import speed_control
 
hmc5883l = i2c_hmc5883l.i2c_hmc5883l(1)
x_list = []
y_list = []

n = 0

steering_servo.steer_direction(30)
speed_control.propulsion(50)


while n < 100:
    hmc5883l.setContinuousMode()
    hmc5883l.setDeclination(9, 0)
    (x, y, z) = hmc5883l.getAxes()
    x_list.append(x)
    y_list.append(y)
    time.sleep(0.5)
    n = n + 1
    print(n, x, y)

speed_control.propulsion(0)
steering_servo.steer_direction(0)

x_min = min(x_list)
x_max = max(x_list)
y_min = min(y_list)
y_max = max(y_list)

x_range = x_max - x_min
y_range = y_max - y_min

x_offset = x_max - x_range/2
y_offset = y_max - y_range/2

offsets_dict = {"x_offset":x_offset, "y_offset":y_offset}

of = open("compass_offsets.txt", "w+") #Open file determined at the top of the program
offsets_json = json.dumps(offsets_dict)
of.write(offsets_json)
of.close()

print("Saved offsets to file:", offsets_dict)


