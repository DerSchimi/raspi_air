import pyhomematic
import datetime
import time
import os
import schedule
from Adafruit_IO import Client, Feed
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

def sendDataToAdafruitIO(pm25, pm10, temperature):
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

  feed_name = 'temperature'  # Replace with your feed name
  data_value = temperature          # Replace with the value you want to send

  try:
      aio.send(feed_name, data_value)
      print(f"Data {data_value} sent to feed '{feed_name}' successfully!")
  except Exception as e:
      print(f"Failed to send data: {e}")

def read_temperature_from_homematic():
    # Initialize the Homematic client
    homematic = pyhomematic.Client()
    homematic.start()

    # Replace with your Homematic device address and channel
    device_address = 'your_device_address'
    channel = 1

    # Get the temperature from the Homematic device
    temperature = homematic.devices[device_address].channels[channel].TEMPERATURE

    homematic.stop()

    return temperature

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
          temperature = read_temperature_from_homematic()
          sendDataToAdafruitIO(pm25, pm10, temperature)
          if print_header:
            print(f"{obs:header}\n")
            print_header = False
            print(f"{obs:csv}\n")
            break

read_sensor()
schedule.every(5).minutes.do(read_sensor)

while True:
    schedule.run_pending()
    time.sleep(1)
