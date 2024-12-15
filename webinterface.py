from flask import Flask, render_template, jsonify
import os
import csv
import datetime

app = Flask(__name__)

LOG_DIR = 'logfiles'

# Create logfiles directory if it does not exist
if not os.path.exists(LOG_DIR):
    os.makedirs(LOG_DIR)

@app.route('/')
def index():
    log_files = os.listdir(LOG_DIR)
    # Sort log_files list by date before rendering the template
    log_files = sorted(log_files, key=lambda x: datetime.datetime.strptime(x.split('_')[1] + '_' + x.split('_')[2] + '_' + x.split('_')[3] + '_' + x.split('_')[4] + '_' + x.split('_')[5] + '_' + x.split('_')[6].split('.')[0], '%Y_%m_%d_%H_%M_%S'))
    return render_template('index.html', log_files=log_files)

@app.route('/chart/<filename>')
def chart(filename):
    timestamps = []
    values1 = []
    values2 = []
    with open(os.path.join(LOG_DIR, filename), 'r') as f:
        reader = csv.reader(f)
        for row in reader:
            timestamps.append(datetime.datetime.fromtimestamp(int(row[0])).strftime('%Y-%m-%d %H:%M:%S'))
            values1.append(row[1])
            values2.append(row[2])
    pm25_limit = 5
    pm10_limit = 15
    return render_template('chart.html', timestamps=timestamps, values1=values1, values2=values2, pm25_limit=pm25_limit, pm10_limit=pm10_limit, x_label='Time', y_label='Values')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

if __name__ == '__main__':
    app.run(debug=True)
