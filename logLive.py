"""
read PMSx003 sensor on /dev/ttyUSB0.

Read 4 samples, one sample every 20 seconds,
and print the observations on different formats.
"""

from pms.core import SensorReader
import datetime
import time
import os
import schedule
from Adafruit_IO import Client, Feed
from dotenv import load_dotenv
import logging

# Configure logging to a file
# Configure logging to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logLive.log"),
        logging.StreamHandler()
    ]
)

# Load environment variables from .env file
load_dotenv()

def sendDataToAdafruitIO(pm25, pm10):
  # Get Adafruit IO credentials from environment variables
  ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME')
  ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY')

  # Initialize the Adafruit IO Client
  aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

  # Send data to a feed
  feed_name = 'pm10'  # Replace with your feed name
  data_value = pm10          # Replace with the value you want to send

  try:
      aio.send(feed_name, data_value)
      logging.info(f"Data {data_value} sent to feed '{feed_name}' successfully!")
  except Exception as e:
      logging.info(f"Failed to send data: {e}")

  feed_name = 'pm25'  # Replace with your feed name
  data_value = pm25          # Replace with the value you want to send

  try:
      aio.send(feed_name, data_value)
      logging.info(f"Data {data_value} sent to feed '{feed_name}' successfully!")
  except Exception as e:
      logging.info(f"Failed to send data: {e}")


def create_logfile(room_name=None):
    current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
    if room_name:
        filename = os.path.join("logfiles", f"log_{current_time}_{room_name}.csv")
    else:
        filename = os.path.join("logfiles", f"log_{current_time}.csv")
    return open(filename, 'w')

def read_sensor():
    try:
        reader = SensorReader("SDS011", "/dev/ttyUSB0", interval=60, samples=1)
    except Exception as e:
        logging.info(f"Failed to initialize sensor reader: {e}")
        return

    start_time = time.time()

    logging.info("\nSDS011 Live Logger ")
    with reader:
        print_header = True
        while time.time() - start_time < 120:
         for obs in reader():
           pm25 = obs.pm25
           pm10 = obs.pm10
           try:
               sendDataToAdafruitIO(pm25,pm10)
           except Exception as e:
               logging.info(f"Failed to send data to Adafruit IO: {e}")
           time.sleep(5)
           if print_header:
             logging.info(f"{obs:header}\n")
             print_header = False
             logging.info(f"{obs:csv}\n")
             break

try:
    read_sensor()
except Exception as e:
    logging.info(f"Failed to read sensor: {e}")
