# raspi_air

## Instructions to run the web server

1. Ensure you have Python installed on your system.
2. Install the required dependencies by running:
   ```
   pip install -r requirements.txt
   ```
3. Run the `read.py` script to generate the logfile:
   ```
   python read.py
   ```
4. Start the web server by running:
   ```
   python webserver.py
   ```

## Instructions to view the chart

1. Open a web browser.
2. Navigate to `http://127.0.0.1:5000/`.
3. You should see a chart displaying the air quality data.
