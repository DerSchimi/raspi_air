import configparser
import os
import time
import schedule
import json
from temperature_logger import TemperatureLogger
from particle_logger import ParticleLogger

# Load device map from devices.json
with open('devices.json', 'r') as f:
    device_map = json.load(f)

# Instantiate the TemperatureLogger class
temperature_logger = TemperatureLogger()

# Instantiate the ParticleLogger class
particle_logger = ParticleLogger()

def loglog():
    temperature_logger.log_temperatures(device_map)
    particle_logger.read_sensor()

loglog()
schedule.every(5).minutes.do(loglog)

while True:
    schedule.run_pending()
    time.sleep(1)
