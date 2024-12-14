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

3. Create the `logfiles` directory:
    ```sh
    mkdir logfiles
    ```

4. Create the `index.html` file in the `templates` directory:
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Log Files</title>
    </head>
    <body>
        <h1>Log Files</h1>
        <ul>
            {% for log_file in log_files %}
                <li><a href="/chart/{{ log_file }}">{{ log_file }}</a></li>
            {% endfor %}
        </ul>
    </body>
    </html>
    ```

5. Create the `chart.html` file in the `templates` directory:
    ```html
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>Chart</title>
        <script src="https://cdn.jsdelivr.net/npm/chart.js"></script>
    </head>
    <body>
        <h1>Chart</h1>
        <canvas id="myChart" width="400" height="200"></canvas>
        <script>
            var ctx = document.getElementById('myChart').getContext('2d');
            var myChart = new Chart(ctx, {
                type: 'line',
                data: {
                    labels: {{ timestamps|tojson }},
                    datasets: [{
                        label: 'Value 1',
                        data: {{ values1|tojson }},
                        borderColor: 'rgba(75, 192, 192, 1)',
                        borderWidth: 1
                    }, {
                        label: 'Value 2',
                        data: {{ values2|tojson }},
                        borderColor: 'rgba(153, 102, 255, 1)',
                        borderWidth: 1
                    }]
                },
                options: {
                    scales: {
                        y: {
                            beginAtZero: true
                        }
                    }
                }
            });
        </script>
    </body>
    </html>
    ```

### Usage

1. Run the web interface:
    ```sh
    python webinterface.py
    ```

2. Open your web browser and go to `http://127.0.0.1:5000/` to view the list of log files.

3. Click on a log file to generate a chart from the data in the log file.
