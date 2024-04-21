import csv
import os
import time

class Recording:

    def __init__(self, cols) -> None:
        # remove newline when deployed
        # os.path.dirname(os.path.abspath(__file__))
        dir_path = os.path.dirname(os.path.abspath(__file__))
        self.csv = open(dir_path + f'/logs/{time.time()}-readings.csv', mode='w', newline='')
        self.csv_writer = csv.writer(self.csv)
        self.cols = cols
        self.setup_csv()
    
    def setup_csv(self):

        header = ['Time']

        for i in range(self.cols):
            header.append(f'Voltage{i+1}')
            header.append(f'Current{i+1}')
        self.csv_writer.writerow(header)

    def write_data(self, data):
        row = [time.time()]
        for v,c in data:
            row.append(v)
            row.append(c)

        # Flushes data out to file immediately
        self.csv_writer.writerow(row)
        self.csv.flush()
        os.fsync(self.csv)

    def close(self):
        self.csv.close()
        print('Closed')
