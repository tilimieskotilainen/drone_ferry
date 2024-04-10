import json
import time
import steering_servo
import trip_dist_calculator
import breadcrumb_calculator

#Variables for steering control
tof_straight = 105
tof_toler = 5
tof_range = 20
steer_toler = 10

#Variables for route phase selections
#GPS_navi_selected = None
config = None
waypoints_list = None
route_points = None
wp_num = None
trip_dist = 0
closest_plus = 0

#cur_stage = "Waiting for stages..."

def update_vars(gui_input):
    global tof_toler
    global tof_range
    global steer_toler
    global closest_plus #Tämä on käynnistystä varten update_calc -funktiossa ja myöhempiä muutoksia varten update_vars funktiossa


    #tähän koodi joka avaa gui_input -tiedot ja päivittää yllä olevat global variablet


#Function to update the initial calculations when prompted from UI
def update_calc():

    global config
    global waypoints_list
    global wp_num
    global trip_dist
    global route_points
    global closest_plus #Tämä on käynnistystä varten update_calc -funktiossa ja myöhempiä muutoksia varten update_vars funktiossa

    try:
        sc = open("config.txt", "r") #Open file
        config = json.loads(sc.read()) #Read the contents of the opened file and assign it to the variable config
        sc.close()
        print("config read")
        #Number of waypoints in route

        closest_plus = int(config["aim_ahead"])

        of = open(config["route"]) #Open file determined in the config file
        route_points = json.loads(of.read()) #Read the contents of the opened file and assign it to the variable "waypoints_list"
        waypoints_list = route_points["waypoints"]
        of.close()

        trip_dist = round(trip_dist_calculator.trip_dist_calculator(route_points),1)
        wp_num = str(len(waypoints_list))
        print("Trip configured | Trip dist:", trip_dist, "m | Waypoints:", wp_num)


    except:
        print("No saved config found")
        pass


#Käynnistyessä laskee ensimmäisen kerran matkan speksit
update_calc()