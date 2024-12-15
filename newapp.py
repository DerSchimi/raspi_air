from multiprocessing import Process
from webinterface import app
from read import create_logfile, reader
import time

def start_webserver():
    app.run(debug=True)

def log_data():
    logfile = create_logfile()
    start_time = time.time()
    with reader:
        print_header = True
        for obs in reader():
            if print_header:
                logfile.write(f"{obs:header}\n")
                print(f"{obs:header}\n")
                print_header = False
            logfile.write(f"{obs:csv}\n")
            print(f"{obs:csv}\n")
            if time.time() - start_time > 60:
                break
    logfile.close()

if __name__ == '__main__':
    webserver_process = Process(target=start_webserver)
    log_data_process = Process(target=log_data)
    webserver_process.start()
    log_data_process.start()
    webserver_process.join()
    log_data_process.join()
