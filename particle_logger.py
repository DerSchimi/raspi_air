import os
import logging
import datetime
import time
import configparser
from Adafruit_IO import Client
from dotenv import load_dotenv
from pms.core import SensorReader

class ParticleLogger:
    def __init__(self, config_file="config.ini"):
        self.config_file = config_file
        self.load_config()
        self.configure_logging()
        self.load_environment_variables()
        self.initialize_adafruit_io()

    def load_config(self):
        self.config = configparser.ConfigParser()
        self.config.read(self.config_file)

    def configure_logging(self):
        logging.basicConfig(
            level=logging.INFO,
            format="%(asctime)s [%(levelname)s] %(message)s",
            handlers=[
                logging.FileHandler("particle_logger.log"),
                logging.StreamHandler()
            ]
        )

    def load_environment_variables(self):
        load_dotenv()
        self.adafruit_io_username = os.getenv('ADAFRUIT_IO_USERNAME')
        self.adafruit_io_key = os.getenv('ADAFRUIT_IO_KEY')

    def initialize_adafruit_io(self):
        self.aio = Client(self.adafruit_io_username, self.adafruit_io_key)

    def send_data_to_adafruit_io(self, pm25, pm10):
        feed_name = 'pm10'
        data_value = pm10
        try:
            self.aio.send(feed_name, data_value)
            logging.info(f"Data {data_value} sent to feed '{feed_name}' successfully!")
        except Exception as e:
            logging.info(f"Failed to send data: {e}")

        feed_name = 'pm25'
        data_value = pm25
        try:
            self.aio.send(feed_name, data_value)
            logging.info(f"Data {data_value} sent to feed '{feed_name}' successfully!")
        except Exception as e:
            logging.info(f"Failed to send data: {e}")

    def create_logfile(self, room_name=None):
        current_time = datetime.datetime.now().strftime("%Y_%m_%d_%H_%M_%S")
        if room_name:
            filename = os.path.join("logfiles", f"log_{current_time}_{room_name}.csv")
        else:
            filename = os.path.join("logfiles", f"log_{current_time}.csv")
        return open(filename, 'w')

    def read_sensor(self):
        try:
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
                            self.send_data_to_adafruit_io(pm25, pm10)
                        except Exception as e:
                            logging.info(f"Failed to send data to Adafruit IO: {e}")
                        time.sleep(5)
                        if print_header:
                            logging.info(f"{obs:header}\n")
                            print_header = False
                            logging.info(f"{obs:csv}\n")
                            break
        except Exception as e:
            logging.info(f"Failed to read sensor: {e}")
