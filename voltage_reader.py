import time
import threading
from record import Recording

class Readings: 
    
    def __init__(self, plots) -> None:
        self.sema = threading.Semaphore()
        self.counter = 1

        # [timestamp, voltage]
        self.readings = [
            [[0],[0]] for _ in range(plots)
        ]
        self.csv_record = Recording()
    
    def update_readings(self, filtered_data: list):
        print(filtered_data)
        self.sema.acquire()
        try: 
        # updating readings
            for i in range(len(filtered_data)):
                reading = self.readings 
                reading[i][0].append(self.counter)
                reading[i][1].append(filtered_data[i])
                if (len(reading[i][0]) > 10):
                    reading[i][0] = reading[i][0][-10:]
                    reading[i][1] = reading[i][1][-10:]
            self.counter += 1

            # recording readings
            filtered_data.insert(0, time.time())
            self.csv_record.write_data(filtered_data)
        
        except:
            print('Could not update readings')
        
        self.sema.release()

    def use_readings(self, action, lines_data, axs):
        self.sema.acquire()
        action(self.readings, lines_data, axs)
        self.sema.release()
    
    def __str__(self):
        return str(self.readings)

class VoltageReader:

    stop_reading = threading.Event()

    def __init__(self, arduino, plots) -> None:
        self.counter = 0
        self.readings = Readings(plots)
        self.arduino = arduino
        self.plots = plots

    def line_filter(self, v):
        if v != '':
            return True
        return False

    # could set the serial to have no timeout
    def read_voltages(self):
        arduino = self.arduino

        # wait for startup
        time.sleep(2)

        while not self.stop_reading.is_set(): 
            lines = []
            read_line = arduino.readline().decode().strip()

            while (not not read_line):
                lines.append(read_line)
                time.sleep(0.01)
                try:
                    read_line = arduino.readline().decode().strip()
                except:
                    print('Could not read line')
                if not read_line:
                    lines.append(read_line)
            
            if (len(lines) > 0):
                filtered_lines = [float(v) for v in filter(self.line_filter, lines)]
                self.readings.update_readings(filtered_lines)