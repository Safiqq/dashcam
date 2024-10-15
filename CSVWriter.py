import csv

class CSVWriter:
    def __init__(self, fileName):
        self.fileName = fileName

    def write_header(self):
        with open(self.fileName, mode='w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Timestamp', 'Closing Duration', 'Closed Duration', 'Reopening Duration', 'Blink Duration', 'Blink Frequency', 'Microsleep', 'PERCLOS', 'Saccade Frequency', 'Saccade Mean'])

    def write_data(self, data):
        with open(self.fileName, mode='a', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(data)
