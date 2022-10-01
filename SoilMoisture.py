
#Author: Zubaidah Almashhadani

import urllib.request
import json
import time
import matplotlib.pyplot as plt
import csv
import datetime
from gpiozero import CPUTemperature


READ_API_KEY='8Z1VMQ91F1HBD3KV' 
CHANNEL_ID= '1365090'
wet_thresh= 80.00
dry_thresh= 70.00

#this can be removed after the first code run! 
header = ['Date', 'Time', 'State', 'Soil_Moisture', 'Temperature']
with open('soil.csv', mode='a') as f:
        writer = csv.writer(f)
        writer.writerow(header)
#until here is removed after the first code run! 
try:
    while True:
        print("----------------------------------------------------")
        TS = urllib.request.urlopen("http://api.thingspeak.com/channels/%s/feeds/last.json?api_key=%s" \
                       % (CHANNEL_ID,READ_API_KEY))
        response = TS.read()
        data = json.loads(response.decode('utf-8'))
        a = data['created_at']
        b = data['field1']
        c = data['field2']
        z = float(b)
        print (a + "    "+ "Soil_Moisture = "+ b + "    " + "Temprature = " + c + "    ")
        if z >= wet_thresh:
            state= 'Wet/Soaking'
            print("The Soil is Wet (No Irrigation Required)")
        elif z <= dry_thresh:
            state= 'Dry'
            print("The Soil is Dry (Irrigation is Required)")
        elif ((z < wet_thresh) and (z > dry_thresh)):
            state = 'Good Condition'
            print("The Soil is in a good arrigation conditions")
        else:
            print("Cannot connect to Thingspeak")
        time.sleep(10)
        #Save The Data top .CSV File
        def date_now():
            today = datetime.datetime.now().strftime("%Y-%m-%d")
            today = str(today)
            return(today)
        def time_now():
            now = datetime.datetime.now().strftime("%H:%M:%S")
            now = str(now)
            return(now)  # the a is for append, if w for write is used then it overwrites the file
        def write_to_csv():
            with open('soil.csv', mode='a') as f:
                sensor_write = csv.writer(f, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
                write_to_log = sensor_write.writerow([date_now(), time_now(), state ,b, c])
                return(write_to_log)
        write_to_csv()
  
        TS.close()

except KeyboardInterrupt:
    print('Press CTRL+C to Terminate The Loop')
    pass

def cpu_temperature():
    cpu = CPUTemperature()
    cpu_temp = cpu.temperature
    cpu_temp = str(cpu_temp)
    print('CPU Temperature is : ', cpu_temp)
    return(cpu_temp)
cpu_temperature()
print("[INFO] cleaning up ...")


