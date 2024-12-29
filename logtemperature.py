import schedule
import time
import json
from temperature_logger import TemperatureLogger

# Load device map from devices.json
with open('devices.json', 'r') as f:
    device_map = json.load(f)

# Instantiate the TemperatureLogger class
temperature_logger = TemperatureLogger()

def log_temperatures():
    temperature_logger.log_temperatures(device_map)

# Schedule the logging every 1 minute
log_temperatures()
schedule.every(1).minutes.do(log_temperatures)

while True:
    schedule.run_pending()
    time.sleep(1)
