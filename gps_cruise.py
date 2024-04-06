import time
import math
import steering_servo
#import speed_control
import compass_reader
import breadcrumb_calculator
import offset_calculator
import read_gps

#status = "run"

#closest_plus = 3




crumbs_left = 10 #Arbitrary number

dist_bc = 0

#status = "jotain"

#Calculates the bearing and relative bearing from the first coordinate to the second coordinate, considering current heading
def angles(from_coord, to_coord, heading):
    offset_dict = offset_calculator.offset_meter_calculator(from_coord, to_coord)
    offset_y = offset_dict["offsets_met"][0]
    offset_x = offset_dict["offsets_met"][1]
    
    #Rules to bypass calculations for special cases that would cause division error
    if offset_y == 0 and offset_x < 0:
        bearing = -90
    elif offset_y == 0 and offset_x > 0:
        bearing = 90

    #Calculation of bearings in most situations
    else:
        #Calculation of bearing angle
        bearing = math.degrees(math.atan(offset_x / offset_y))
        
        #Adjustments needed for lower two 90-degree quadrants
        if offset_y < 0 and offset_x < 0:
            bearing = -180 + abs(bearing)
        elif offset_y < 0 and offset_x > 0:
            bearing = 180 - abs(bearing)
        
    #Determining the relative bearing
    rel_bearing = bearing - heading
    
    
    #Adjusting if rel_bearing > 180 in either direction to find the direction with samallest angle
    if rel_bearing < -180:
        rel_bearing = 360 + rel_bearing
    if rel_bearing > 180:
        rel_bearing = rel_bearing - 360

    bearings_dict = {"Target bearing":bearing, "Target relative bearing":rel_bearing}
    return(bearings_dict)

def captain(waypoints_list, closest_plus):
    print("Captain started")
#    breadcrumb_coordinates = []
    breadcrumb_coordinates = breadcrumb_calculator.breadcrumb(waypoints_list)
    print("Breadcrumbs:", breadcrumb_coordinates)
    global dist_bc
    location_now = read_gps.current_min #Find out current location for plotting
    while True:
        location_now = read_gps.current_min
        closest_c, target_c, crumbs_left = breadcrumb_calculator.closest_crumb(location_now, breadcrumb_coordinates, closest_plus)
        print("Crumb info:", closest_c, target_c, crumbs_left)
        if crumbs_left > 1:
            dist_bc = offset_calculator.offset_meter_calculator(location_now, closest_c)
            bearings = angles(location_now, target_c, compass_reader.heading)
            rel_bearing = bearings["Target relative bearing"]
            steering_servo.angle = rel_bearing
            #speed_control.propulsion(40)
        else:
            #speed_control.propulsion(0)
            return("GPS Done")
        
        time.sleep(0.5)
    return("GPS Terminated")
