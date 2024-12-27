import configparser
import os
import time
import logging
import schedule
from homematicip.home import Home
from Adafruit_IO import Client
from dotenv import load_dotenv

# Configure logging to a file
# Configure logging to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("log_temperatures.log"),
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

# Map with device IDs and corresponding Adafruit data feed IDs
device_map = {
    "3014F711A0000313C98CC0B3": "tempwohnzimmer",
    "3014F711A0000A9BE991DED0": "tempgaestewc",
    "3014F711A0000313C98CC097": "tempkinderzimmer",
    "3014F711A0000A9A499947EC": "tempbadezimmer"
}

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

# Schedule the logging every 1 minute
log_temperatures()
schedule.every(1).minutes.do(log_temperatures)

while True:
    schedule.run_pending()
    time.sleep(1)
