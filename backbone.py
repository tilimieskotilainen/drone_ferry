#This is the backbone of the code, initiating the various stages of the journey based on trigger events

status = ["init"]

import json
import threading
import read_gps
import compass_reader
import asyncio
import websockets
import time
import steering_servo
import shoot_and_calculate
import trip_dist_calculator
import breadcrumb_calculator
import gps_cruise
import Approach


#Variables for route phase selections
retreat_selected = None
turn_selected = None
GPS_navi_selected = None
Approach = None

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
cam_nav = threading.Thread(target=shoot_and_calculate.calculate_diff, daemon=True)
cam_nav.start()


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
    print("Run started")
    
    global cur_stage
    
    if stages["retreat"] == True and status[0] == "run":
        print("Retreat started")
        cur_stage = "Retreat"
        shoot_and_calculate.detect = True
        shoot_and_calculate.detect = False
        print("Retreat ended")
        pass
    
    if stages["turn"] == True and status[0] == "run":
        print("Turn started")
        cur_stage = "Turn"
        print("Turn ended")
        pass

    if stages["gps_cruise"] == True and status[0] == "run":
        print("GPS Cruise started")
        cur_stage = "GPS Cruise"
        gps_cruise.captain(waypoints_list, closest_plus, status, status[0])
        print("GPS Cruise ended")
    
    if stages["approach"] == True and status[0] == "run":
        print("Approach started")
        cur_stage = "Approach"
        shoot_and_calculate.detect = True
        Approach.Approach(waypoints_list)
        shoot_and_calculate.detect = False
        print("Approach ended")

    cur_stage = "Finished all stages"
    print("Run program completed")

async def test(websocket, path):

    global cur_stage
    global status
    while True:
        try:
            send_dict = {"config":config, "status":status[0], "cur_stage":cur_stage, "wp":route_points, "wp_num":wp_num, "heading":round(compass_reader.heading, 0), "gps":read_gps.current_min, "dist":trip_dist, "closest_bc":breadcrumb_calculator.closest_index}
            send_json = json.dumps(send_dict)
            await websocket.send(send_json)
            print("Send dict:", send_dict)


            #Catch and convert data from client
            recv_json = await websocket.recv()
            recv_dict = json.loads(recv_json)

            #Perform update of configuration data if an update is indicated by client

            print("Received:", recv_dict)

            if recv_dict["control"] == "update":
                recv_dict.pop("control") #Remove unnecessary indicator item from the dictionary
                save_config_json = json.dumps(recv_dict) #Create JSON from received config data

                scs = open("config.txt", "w+") #Open config file in write-mode
                scs.write(save_config_json) #Write the JSON data to file
                scs.close() #Close file

            elif recv_dict["control"] == "waiting":
                status[0] = "waiting"

            elif recv_dict["control"] == "run":
#                print("run started")
#                gps_cruise.status = "run" #Used to have all running threads to check on every loop before continuing
#                print("gps cruise status updated")
#                Approach.status = "run" #Tätä ei tarvita koska Approach ei ole jatkuvasti päällä oleva thread.


                if status[0] != "run":
                    run_thread = threading.Thread(target=run, daemon=True, args=(recv_dict["stages"],))
                    run_thread.start()
                    status[0] = "run"
                    print("main status updated")
                

            elif recv_dict["control"] == "terminate":
                status[0] = "waiting"
#                gps_cruise.status = "terminate"
                cur_stage = "Waiting for stage..."

    #        status = "waiting"

        except:
            print("Try failed")
            break

        time.sleep(0.5)

start_server = websockets.serve(test, "127.0.0.1", 5678)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
