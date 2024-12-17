# raspi_air

## Project Description

This project is designed to read data from a SDS011 sensor connected to a Raspberry Pi and log the data into CSV files. The project also includes a web interface to list all log files from a directory and generate charts from the data in the log files.

## Experimental App

This is an experimental app to read data via `pypms` from an `SDS011` sensor and send it to an Adafruit dashboard. The app leverages advanced sensor reading techniques and cloud integration to provide real-time data visualization and monitoring. By utilizing the `pypms` library, the app ensures accurate and efficient data collection from the `SDS011` sensor. The integration with the Adafruit dashboard allows for seamless data transmission and visualization, enabling users to monitor air quality metrics in real-time.

## Dependencies

- Flask
- Chart.js
- pms

## Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/DerSchimi/raspi_air.git
    cd raspi_air
    ```

2. Install the required dependencies:
    ```sh
    pip install flask pms
    ```

3. Create the `logfiles` directory:
    ```sh
    mkdir logfiles
    ```

## Usage

1. Run the web interface:
    ```sh
    python webinterface.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/` to view the list of log files.

3. Click on a log file to generate a chart from the data in the log file.

4. The log files will be created in the `logfiles` directory with a name pattern like `log_2023_04_15_14_30_00.csv`.

5. To read data from the SDS011 sensor and log it to a CSV file, run:
    ```sh
    python readLocal.py
    ```

6. To read data from the SDS011 sensor and send it to the Adafruit dashboard, run:
    ```sh
    python logAndSendToAdafruitDashboard.py
    ```

## Contributing

Contributions are welcome! Please follow these guidelines when contributing to the project:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request with a clear description of your changes.