import glob
import os
import sys
from pathlib import Path

from sllib import Reader

FIELDS = ['time1', 'gps_speed', 'gps_speed_kph', 'lon_enc', 'lat_enc',
          'longitude', 'latitude', 'water_depth_m', 'packetsize']

fmt = "|{:>11}|{:>10}|{:>14}|{:>9}|{:>9}|{:>11}|{:>11}|{:>14}|{:>10}|\n"


def fnum(value):
    if isinstance(value, float):
        return f'{value:f}'
    return value


# def format_data(row):
#     return {k: fnum(v) for (k, v) in row.items()}


def process_file(filename, outpath):
    name = Path(filename).stem
    outfile = os.path.join(outpath, f'{name}.txt')
    with open(outfile, 'w', newline='\n') as fil:
        header = fmt.format(*FIELDS)
        fil.write(header)
        fil.write(fmt.replace('>', '->').format(*map(lambda k: '-', FIELDS)))

        last = None
        with open(filename, 'rb') as f:
            reader = Reader(f)
            print(reader.header)

            for frame in reader:
                point = (frame.longitude, frame.latitude)
                values = frame.to_dict(fields=FIELDS)
                if point != last:
                    fil.write(fmt.format(*map(lambda k: fnum(values[k]), FIELDS)))
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
