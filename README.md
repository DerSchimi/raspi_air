# raspi_air

## Project Description

This project is designed to read data from a PMSx003 sensor connected to a Raspberry Pi and log the data into CSV files. The project also includes a web interface to list all log files from a directory and generate charts from the data in the log files.

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

## Contributing

Contributions are welcome! Please follow these guidelines when contributing to the project:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes.
4. Submit a pull request with a clear description of your changes.
