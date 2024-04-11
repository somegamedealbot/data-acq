import csv

class Recording:

    def __init__(self, rows) -> None:
       self.csv = open('test.csv', mode='x')
       self.csv_writer = csv.writer(self.csv)
       self.rows = rows + 1
       self.setup_csv()
    
    def setup_csv(self):
        header = ['Time' if i == 0 else f'Plot {i}' for i in range(self.rows)]
        
        self.csv_writer.writerow(header)

    def write_data(self, data):
        self.csv_writer(data)
