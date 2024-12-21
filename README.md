# raspi_air

## Project Description

This project is designed to read data from a SDS011 sensor connected to a Raspberry Pi and log the data to an adafruit dashboard.

## Experimental App

This is an experimental app to read data via `pypms` from an `SDS011` sensor and send it to an Adafruit dashboard. The app leverages advanced sensor reading techniques and cloud integration to provide real-time data visualization and monitoring. By utilizing the `pypms` library, the app ensures accurate and efficient data collection from the `SDS011` sensor. The integration with the Adafruit dashboard allows for seamless data transmission and visualization, enabling users to monitor air quality metrics in real-time.

## Dependencies

- pms
- python-dotenv

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/DerSchimi/raspi_air.git
    cd raspi_air
    ```

2. Install the required dependencies:
    ```sh
    pip install flask pms python-dotenv
    ```
3Create a `.env` file in the project directory and add your Adafruit IO credentials:
    ```plaintext
    ADAFRUIT_IO_USERNAME=your_username
    ADAFRUIT_IO_KEY=your_key
    ```

## Usage

1. To read data from the SDS011 sensor and send it to the Adafruit dashboard every 5 seconds, run:
    ```sh
    python logLive.py
    ```

2. To read data from the SDS011 sensor and log it to a CSV file every 5 minutes, run:
    ```sh
    python logNormal.py
    ```

## Contributing

Contributions are welcome! Please follow these guidelines when contributing to the project:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request with a clear description of your changes.