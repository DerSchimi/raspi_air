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
from Adafruit_IO import Client, Feed


def sendDataToAdafruitIO(pm25, pm10):
  # Your Adafruit IO credentials
  ADAFRUIT_IO_USERNAME = 'DrDanger123'
  ADAFRUIT_IO_KEY = ''

  # Initialize the Adafruit IO Client
  aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

  # Send data to a feed
  feed_name = 'pm10'  # Replace with your feed name
  data_value = pm10          # Replace with the value you want to send

  try:
      aio.send(feed_name, data_value)
      print(f"Data {data_value} sent to feed '{feed_name}' successfully!")
  except Exception as e:
      print(f"Failed to send data: {e}")

  feed_name = 'pm25'  # Replace with your feed name
  data_value = pm25          # Replace with the value you want to send

  try:
      aio.send(feed_name, data_value)
      print(f"Data {data_value} sent to feed '{feed_name}' successfully!")
  except Exception as e:
      print(f"Failed to send data: {e}")


def create_logfile(room_name=None):
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if room_name:
        filename = os.path.join("logfiles", f"log_{current_time}_{room_name}.csv")
    else:
        filename = os.path.join("logfiles", f"log_{current_time}.csv")
    return open(filename, 'w')

def read_sensor():
    reader = SensorReader("SDS011", "/dev/ttyUSB0", interval=10, samples=1)
    start_time = time.time()

    print("\nSDS011 1 sample on CSV format with header")
    with reader:
        print_header = True
        for obs in reader():
          pm25 = obs.pm25
          pm10 = obs.pm10
          sendDataToAdafruitIO(pm25,pm19)
            if print_header:
                print(f"{obs:header}\n")
                print_header = False
            print(f"{obs:csv}\n")
            break

read_sensor()
schedule.every(1).minutes.do(read_sensor)

while True:
    schedule.run_pending()
    time.sleep(1)
