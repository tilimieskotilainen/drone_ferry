#This is the backbone of the code, initiating the various stages of the journey based on trigger events

status = ["init"]

import json
import threading
import read_gps
import compass_reader
#import asyncio
#import websockets
import time
import steering_servo
#import shoot_and_calculate
import trip_dist_calculator
import breadcrumb_calculator
import gps_cruise
#import Approach
#import webbrowser


#Variables for route phase selections
GPS_navi_selected = None

config = None
waypoints_list = None
route_points = None
wp_num = None
trip_dist = 0
closest_plus = 0

cur_stage = "Waiting for stages..."

read_gps_thread = threading.Thread(target=read_gps.read_gps, args=(), daemon=True) #Define GPS thread
read_gps_thread.start() # Start GPS thread
read_compass_thread = threading.Thread(target=compass_reader.read_compass, args=(), daemon=True) #Define compass thread
read_compass_thread.start() # Start compass thread
steering_thread = threading.Thread(target=steering_servo.steer_direction, args=(status[0]), daemon=True) #Define compass thread
steering_thread.start() # Start compass thread


#Function to update the initial calculations when prompted from UI
def update_calc():

    global config
    global waypoints_list
    global wp_num
    global trip_dist
    global closest_plus
    global route_points

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
        print("Trip dist:", trip_dist)
        wp_num = str(len(waypoints_list))
        print("waypoints read")


    except:
        print("No saved config found")
        pass


#Käynnistyessä laskee ensimmäisen kerran matkan speksit
update_calc()

#Funktio joka lähtee pyörimään, kun UI:ssa valitaan statukseksi "run"
def run(stages):
    print("GPS Cruise starting")
    gps_cruise.captain(waypoints_list, closest_plus)
    print("GPS Cruise ended")
    
#Käynnistää run-funktion ilman parametrejä
run()
