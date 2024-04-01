import serial
from pynmea import nmea


#Specs for GPS module
ser = serial.Serial('/dev/serial0') #Aikaisemmin käytetty
#ser = serial.Serial('/dev/ttyS0') #Laitettu 1.4.2024 testinä
ser.baudrate=9600
#ser.baudrate=115200

current_min = (0.0, 0.0)

#Reads gps coordinates and returns current location in minutes and decimals
def read_gps():

    print("GPS Running")

    global current_min

    while True:
        try:
            message = ser.readline().decode()
            if '$GNGGA' in message:
#                gngga = nmea.GPGGA()
#                gngga.parse(message)
                message_list = message.split(",")
                lat = message_list[2]
                lon = message_list[4]
                lat_min = round(float(lat[0:2]) * 60 + float(lat[2:]), 6)
                lon_min = round(float(lon[0:3]) * 60 + float(lon[3:]), 6)
                current_min = (lat_min, lon_min)
                print(current_min)

                return(current_min)
        except:
            print("No GPS-signal")
            pass
        

if __name__ == "__main__":
    read_gps()