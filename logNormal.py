import configparser
import os
import time
import logging
import schedule
import json
from homematicip.home import Home
from Adafruit_IO import Client, Feed
from dotenv import load_dotenv
from pms.core import SensorReader

# Configure logging to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logNormal.log"),
        logging.StreamHandler()
    ]
)
# Load environment variables from .env file
load_dotenv()

# Config-Datei einlesen
config_file = "config.ini"
config = configparser.ConfigParser()
config.read(config_file)

# Authentifizierungsdaten aus der Config
auth_token = config["AUTH"]["authtoken"]
access_point = config["AUTH"]["accesspoint"]

# Verbindung zum Homematic IP System herstellen
home = Home()
home.set_auth_token(auth_token)
home.init(access_point)

# Daten synchronisieren
try:
    home.get_current_state()
except Exception as e:
    logging.info(f"Failed to get current state: {e}")

# Load device map from devices.json
with open('devices.json', 'r') as f:
    device_map = json.load(f)

# Get Adafruit IO credentials from environment variables
ADAFRUIT_IO_USERNAME = os.getenv('ADAFRUIT_IO_USERNAME')
ADAFRUIT_IO_KEY = os.getenv('ADAFRUIT_IO_KEY')

# Initialize the Adafruit IO Client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

def send_temperature_to_adafruit(feed_id, temperature):
    try:
        aio.send(feed_id, temperature)
        logging.info(f"Data {temperature} sent to feed '{feed_id}' successfully!")
    except Exception as e:
        logging.info(f"Failed to send data: {e}")

def log_temperatures():
    try:
        home.get_current_state()
    except Exception as e:
        logging.info(f"Failed to get current state: {e}")
    logging.info("Logging temperature data of devices:")
    for device in home.devices:
        if device.id in device_map and hasattr(device, 'actualTemperature'):
            adafruit_feed_id = device_map[device.id]
            temperature = device.actualTemperature
            logging.info(f"Gerät: {device.label} / {device.id} - Temperatur: {temperature}°C - Adafruit Feed ID: {adafruit_feed_id}")
            try:
                send_temperature_to_adafruit(adafruit_feed_id, temperature)
            except Exception as e:
                logging.info(f"Failed to send temperature to Adafruit IO: {e}")

def sendDataToAdafruitIO(pm25, pm10):
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
    reader = SensorReader("SDS011", "/dev/ttyUSB0", interval=10, samples=1)
    start_time = time.time()

    logging.info("\nSDS011 1 sample on CSV format with header")
    with reader:
        print_header = True
        try:
            for obs in reader():
                pm25 = obs.pm25
                pm10 = obs.pm10
                sendDataToAdafruitIO(pm25, pm10)
                if print_header:
                    logging.info(f"{obs:header}\n")
                    print_header = False
                    logging.info(f"{obs:csv}\n")
                    break
        except Exception as e:
            logging.info(f"Failed to read sensor: {e}")

# Schedule the logging every 1 minute

def loglog():
    logging.info("Log log")
    log_temperatures()
    read_sensor()

loglog()
schedule.every(5).minutes.do(loglog)


while True:
    schedule.run_pending()
    time.sleep(1)
