from os import path
import csv

from sllib import create_reader

FIELDS = ['time1', 'gps_speed', 'gps_speed_kph', 'lon_enc', 'lat_enc',
          'longitude', 'latitude', 'water_depth_m']


def main():
    filename = path.join('tests', 'sample-data-lowrance', 'Elite_4_Chirp',
                         'small.sl2')

    with open('test.csv', 'w') as csvfile:
        with create_reader(filename) as reader:
            writer = csv.DictWriter(csvfile, FIELDS, dialect='excel', extrasaction='ignore')
            writer.writeheader()
            for frame in reader:
                writer.writerow(frame.to_dict())


if __name__ == "__main__":
    main()
