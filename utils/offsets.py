from typing import List
import csv
import os
import struct
import argparse
import logging
from pathlib import Path
from io import IOBase

from sllib.frame import Frame
from sllib import Reader

logger = logging.getLogger(__name__)
# root = logging.getLogger('root')

"""
This was used to figure out valid offsets for frames
in a sl3 file.

Ultimately led to the discovery of channel 9 and that
flag 0x0008 probably indicates a valid packet.
- format 3.1, channel 9 and flag 0x0008 happens on the same time.
- format 3.2, seems as if channel > 5 then header is 128 bytes instead of 168
  no change in flags
"""


def create_csv_with_header(csvfile, fields) -> csv.DictWriter:
    writer = csv.DictWriter(
        csvfile, fields, dialect='excel',
        extrasaction='ignore', delimiter='\t')
    writer.writeheader()
    return writer


def readfile(stream: IOBase, writer: csv.DictWriter, formver: List[int], maxcount: int = 20):
    count = 0
    last = 0
    offset = 8
    last_end = 8
    while True:
        stream.seek(offset)
        buf = stream.read(4)
        if buf == b'' or len(buf) < 4:
            logger.info('no more data.')
            break
        # read data as if offset
        data = struct.unpack('<I', buf)

        if data[0] == offset:  # yes, we have an equal
            stream.seek(offset)  # go back a bit
            fr = Frame.read(stream, formver)
            told = stream.tell()
            dct = fr.to_dict(formver[0])
            dct['start'] = offset
            dct['end'] = told
            dct['offby'] = offset - last_end
            dct['size'] = offset-last
            dct['asdf'] = [fr.channel, f'({fr.flags}) {fr.flags:016b}']
            writer.writerow(dct)
            # print(
            #     'match at', offset, 'now', dct['now'], 'size', offset - last, 'asd', now-offset-fr.headersize,
            #     fr.to_dict(format=3, fields=['offset', 'index', 'latitude', 'packetsize', 'headersize'])
            # )
            last_end = told
            last = offset
            count += 1

        offset += 1
        if count >= maxcount:
            break
    return count


def main(filename, maxcount):
    outpath = os.path.dirname(filename)
    name = Path(filename).stem
    outfile = os.path.join(outpath, f'{name}.offsets.tab')
    with open(filename, 'rb') as stream:
        with open(outfile, 'w', newline='') as csvfile:
            reader = Reader(stream)
            formver = [reader.header.format, reader.header.version]
            print(reader.header)
            fields = ['start', 'end', 'offby', 'size', 'asdf'] + reader.fields
            writer = create_csv_with_header(csvfile, fields)
            count = readfile(stream, writer, formver, maxcount)
            print(f'wrote {count} records to {outfile}')


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('path', help="path to file to test")
    parser.add_argument(
        '-v', '--verbosity',
        default=0, action='count',
        help="increase verbosity")
    parser.add_argument(
        '-n', '--number',
        type=int, default=20,
        help="number of records to read"
    )
    args = parser.parse_args()

    if args.verbosity > 3:
        args.verbosity = 3

    level = logging.ERROR - (args.verbosity * 10)
    # root.setLevel(level)
    logging.basicConfig(level=level)
    main(args.path, args.number)
