#!/usr/bin/env python3
import configparser
import json
import time
from builtins import input
import logging

import homematicip
import homematicip.auth
from homematicip.home import Home

# Configure logging to a file
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logcredentials.log"),
        logging.StreamHandler()
    ]
)
def main():
    while True:
        access_point = (
            input("Please enter the accesspoint id (SGTIN): ").replace("-", "").upper()
        )
        if len(access_point) != 24:
            logging.info("Invalid access_point id")
            continue
        break

    home = Home()
    home.init(access_point)
    auth = homematicip.auth.Auth(home)

    devicename = input(
        "Please enter the client/devicename (leave blank to use default):"
    )

    while True:
        pin = input("Please enter the PIN (leave Blank if there is none): ")

        if pin != "":
            auth.pin = pin
        response = None
        if devicename != "":
            response = auth.connectionRequest(access_point, devicename)
        else:
            response = auth.connectionRequest(access_point)

        if response.status_code == 200:  # ConnectionRequest was fine
            break

        errorCode = json.loads(response.text)["errorCode"]
        if errorCode == "INVALID_PIN":
            logging.info("PIN IS INVALID!")
        elif errorCode == "ASSIGNMENT_LOCKED":
            logging.info("LOCKED ! Press button on HCU to unlock.")
            time.sleep(5)
        else:
            logging.info("Error: {}\nExiting".format(errorCode))
            return

    logging.info("Connection Request successful!")
    logging.info("Please press the blue button on the access point")
    while not auth.isRequestAcknowledged():
        logging.info("Please press the blue button on the access point")
        time.sleep(2)

    auth_token = auth.requestAuthToken()
    clientId = auth.confirmAuthToken(auth_token)

    logging.info(
        "-----------------------------------------------------------------------------"
    )
    logging.info("Token successfully registered!")
    logging.info(
        "AUTH_TOKEN:\t{}\nACCESS_POINT:\t{}\nClient ID:\t{}\nsaving configuration to ./config.ini".format(
            auth_token, access_point, clientId
        )
    )

    _config = configparser.ConfigParser()
    _config.add_section("AUTH")
    _config.add_section("LOGGING")
    _config["AUTH"] = {"AuthToken": auth_token, "AccessPoint": access_point}
    _config.set("LOGGING", "Level", "30")
    _config.set("LOGGING", "FileName", "None")
    with open("./config.ini", "w") as configfile:
        _config.write(configfile)


if __name__ == "__main__":
    main()
