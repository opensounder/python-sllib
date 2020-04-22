import csv
import sys
from pathlib import Path

from sllib import Reader

FIELDS = ['time1', 'gps_speed', 'gps_speed_kph', 'lon_enc', 'lat_enc',
          'longitude', 'latitude', 'water_depth_m']


def main():
    filename = sys.argv[1]
    name = Path(filename).stem

    with open(f'{name}.csv', 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, FIELDS, dialect='excel',
                                extrasaction='ignore', delimiter=';')
        writer.writeheader()
        with open(filename, 'rb') as f:
            reader = Reader(f)
            for frame in reader:
                writer.writerow(frame.to_dict(fields=FIELDS))


if __name__ == "__main__":
    main()
