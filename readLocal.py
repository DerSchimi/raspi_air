"""
Read PMSx003 sensor on /dev/ttyUSB0.

Read 4 samples, one sample every 20 seconds,
and print the observations on different formats.
"""

from pms.core import SensorReader
import datetime
import time
import os

def create_logfile(room_name=None):
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if room_name:
        filename = os.path.join("logfiles", f"log_{current_time}_{room_name}.csv")
    else:
        filename = os.path.join("logfiles", f"log_{current_time}.csv")
    return open(filename, 'w')

reader = SensorReader("SDS011", "/dev/ttyUSB0", interval=60, samples=100)

logfile = create_logfile()
start_time = time.time()

print("\nSDS011 4 samples on CSV format with header")
with reader:
    print_header = True
    for obs in reader():
        if print_header:
            print(f"{obs:header}\n")
            print_header = False
        logfile.write(f"{obs:csv}\n")
        print(f"{obs:csv}\n")
        if time.time() - start_time > 6000:
            break

logfile.close()
print("Logfile saved on", logfile.name)
