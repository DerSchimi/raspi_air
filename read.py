"""
Read PMSx003 sensor on /dev/ttyUSB0.

Read 4 samples, one sample every 20 seconds,
and print the observations on different formats.
"""

from pms.core import SensorReader
import datetime
import time
import os
import schedule

def create_logfile(room_name=None):
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if room_name:
        filename = os.path.join("logfiles", f"log_{current_time}_{room_name}.csv")
    else:
        filename = os.path.join("logfiles", f"log_{current_time}.csv")
    return open(filename, 'w')

def read_sensor():
    reader = SensorReader("SDS011", "/dev/ttyUSB0", interval=10, samples=1)
    #logfile = create_logfile()
    start_time = time.time()

    print("\nSDS011 1 sample on CSV format with header")
    with reader:
        print_header = True
        for obs in reader():
            if print_header:
                print(f"{obs:header}\n")
                print_header = False
            #logfile.write(f"{obs:csv}\n")
            print(f"{obs:csv}\n")
                break
    print("done")
    #logfile.close()
    #print("Logfile saved on", logfile.name)

read_sensor()
schedule.every(5).minutes.do(read_sensor)

while True:
    schedule.run_pending()
    time.sleep(1)
