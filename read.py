"""
Read PMSx003 sensor on /dev/ttyUSB0.

Read 4 samples, one sample every 20 seconds,
and print the observations on different formats.
"""

from pms.core import SensorReader
import datetime
import time

def format_time(timestamp):
    return datetime.datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')

def create_logfile():
    current_time = datetime.datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"log_{current_time}.csv"
    logfile = open(filename, 'w')
    logfile.write("time, pm25, pm10\n")
    return logfile

reader = SensorReader("SDS011", "/dev/ttyUSB0", interval=20, samples=4)

logfile = create_logfile()
start_time = time.time()

print("\nSDS011 4 samples on CSV format with header")
with reader:
    for obs in reader():
        formatted_time = format_time(time.time())
        logfile.write(f"{formatted_time}, {obs.pm25}, {obs.pm10}\n")
        if time.time() - start_time > 300:
            break

logfile.close()
