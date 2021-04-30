import csv
import glob
import os
import sys
from pathlib import Path

from sllib import Reader

FIELDS = ['time1', 'gps_speed', 'gps_speed_kph', 'lon_enc', 'lat_enc',
          'longitude', 'latitude', 'water_depth_m', 'packetsize']


def process_file(filename, outpath):
    name = Path(filename).stem
    outfile = os.path.join(outpath, f'{name}.csv')
    with open(outfile, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, FIELDS, dialect='excel',
                                extrasaction='ignore', delimiter='\t')
        writer.writeheader()
        last = None
        with open(filename, 'rb') as f:
            reader = Reader(f)
            print(reader.header)
            first = True
            for frame in reader:
                if first:
                    print(frame.packetsize)
                    first = False
                point = (frame.longitude, frame.latitude)
                if point != last:
                    writer.writerow(frame.to_dict(fields=FIELDS))
                    last = point


def main():
    filepath = sys.argv[1]
    print(f'Testing {filepath} to see what it is')
    if os.path.isfile(filepath):
        print('You provided a file.')
        process_file(filepath, os.path.dirname(filepath))
    elif os.path.isdir(filepath):
        pattern = os.path.join(filepath, '*.sl*')
        print('Gou provided a directory.')
        print("Will try to glob " + pattern)
        for filename in glob.iglob(pattern):
            print(filename)
            process_file(filename, filepath)
    else:
        print(f'Error! You must provide a file or directory. "{filepath}" is neither.')


if __name__ == "__main__":
    # print('asdfasdf')
    main()
