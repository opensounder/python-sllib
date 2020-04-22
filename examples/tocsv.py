import csv
import sys
from pathlib import Path

from sllib import create_reader

FIELDS = ['time1', 'gps_speed', 'gps_speed_kph', 'lon_enc', 'lat_enc',
          'longitude', 'latitude', 'water_depth_m']


def main():
    filename = sys.argv[1]
    name = Path(filename).stem

    with open(f'{name}.csv', 'w', newline='') as csvfile:
        with create_reader(filename) as reader:
            writer = csv.DictWriter(csvfile, FIELDS, dialect='excel',
                                    extrasaction='ignore', delimiter=';')
            writer.writeheader()
            for frame in reader:
                writer.writerow(frame.to_dict(fields=FIELDS))


if __name__ == "__main__":
    main()
