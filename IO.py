import csv

def read_csv(file):
    with open(file, "r") as file:
        reader = csv.reader(file)
        lines = list(reader)
                
        return lines

def write_header1(file):
    with open(file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Hari', 'Tanggal', 'Waktu', 'Closing Time(s)', 'Reopening Time(s)', 'Closed Time(s)', 'Blink Duration(s)', 'Blink Frequency', "Microsleep", "Perclos", "Jarak Rata-Rata(m)", "Jarak Minimal(m)", "Jarak Aman(m)", "Kecepatan Rata-Rata(km/jam)", "Kategori Kecepatan"])

def write_header2(file):
    with open(file, mode='w', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(['Hari', 'Tanggal', 'Waktu', "Time to collision", "Kategori SCE"])

def write_data_to_csv(data, file):
    with open(file, mode='a', newline='') as f:
        writer = csv.writer(f)
        writer.writerow(data)
