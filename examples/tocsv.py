import csv
import glob
import os
from pathlib import Path
import argparse

from sllib import Reader


def create_csv_with_header(csvfile, fields):
    writer = csv.DictWriter(
        csvfile, fields, dialect='excel',
        extrasaction='ignore', delimiter='\t')
    writer.writeheader()
    return writer


def process_file(filename, outpath, all):
    name = Path(filename).stem
    outfile = os.path.join(outpath, f'{name}.csv.tab')
    with open(outfile, 'w', newline='') as csvfile:
        last = None
        with open(filename, 'rb') as f:
            reader = Reader(f)
            print(filename, reader.header)
            fields = reader.header.fields
            writer = create_csv_with_header(csvfile,  fields)
            for frame in reader:
                point = (frame.longitude, frame.latitude)
                if all or point != last:
                    writer.writerow(frame.to_dict(fields=fields, format=reader.header.format))
                    last = point


def main(path, all):
    print(f'Testing {path} to see what it is')
    if os.path.isfile(path):
        print('You provided a file.')
        process_file(path, os.path.dirname(path), all)
    elif os.path.isdir(path):
        pattern = os.path.join(path, '*.sl*')
        print('You provided a directory.')
        print("Will try to glob " + pattern)
        for filename in glob.iglob(pattern):
            print(filename)
            process_file(filename, path)
    else:
        print(f'Error! You must provide a file or directory. "{path}" is neither.')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="path to file or directory to process.")
    parser.add_argument(
        '-a', '--all',
        help="store all records even if position is unchanged",
        action='store_true')
    args = parser.parse_args()
    print(args)
    main(args.path, args.all)
