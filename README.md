# raspi_air

## Web Interface

This project includes a simple web interface to list all log files from a directory and generate charts from the data in the log files.

### Dependencies

- Flask
- Chart.js

### Installation

1. Clone the repository:
    ```sh
    git clone https://github.com/DerSchimi/raspi_air.git
    cd raspi_air
    ```

2. Install the required dependencies:
    ```sh
    pip install flask
    ```

### Usage

1. Run the web interface:
    ```sh
    python webinterface.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/` to view the list of log files.

3. Click on a log file to generate a chart from the data in the log file.
