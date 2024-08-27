import csv

def write(file, rows, encoding='utf-8'):
    with open(file, "w", encoding=encoding, newline="") as fp:
        csv_writer = csv.writer(fp)
        csv_writer.writerows(rows)
