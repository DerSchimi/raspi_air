"""
read PMSx003 sensor on /dev/ttyUSB0.

Read 4 samples, one sample every 20 seconds,
and print the observations on different formats.
"""

import datetime
import time
import os
import schedule
from dotenv import load_dotenv
import logging
from temperature_logger import TemperatureLogger
from particle_logger import ParticleLogger

# Instantiate the TemperatureLogger class
temperature_logger = TemperatureLogger()

# Instantiate the ParticleLogger class
particle_logger = ParticleLogger()

def loglog():
    temperature_logger.read_sensor()
    particle_logger.read_sensor()

loglog()
schedule.every(5).minutes.do(loglog)

while True:
    schedule.run_pending()
    time.sleep(1)
