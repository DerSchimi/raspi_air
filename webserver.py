from flask import Flask, send_file
import matplotlib.pyplot as plt
import csv
import io

app = Flask(__name__)

def read_logfile(filename):
    times = []
    pm25_values = []
    pm10_values = []
    with open(filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)
        for row in reader:
            times.append(row['time'])
            pm25_values.append(float(row['pm25']))
            pm10_values.append(float(row['pm10']))
    return times, pm25_values, pm10_values

def generate_chart(times, pm25_values, pm10_values):
    plt.figure(figsize=(10, 5))
    plt.plot(times, pm25_values, label='PM2.5')
    plt.plot(times, pm10_values, label='PM10')
    plt.xlabel('Time')
    plt.ylabel('Concentration')
    plt.title('Air Quality Over Time')
    plt.legend()
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    return buf

@app.route('/')
def chart():
    times, pm25_values, pm10_values = read_logfile('logfile.csv')
    chart_buf = generate_chart(times, pm25_values, pm10_values)
    return send_file(chart_buf, mimetype='image/png')

if __name__ == '__main__':
    app.run(debug=True)
