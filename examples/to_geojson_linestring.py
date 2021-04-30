import sys
import json
from pathlib import Path

from sllib import Reader


def main():
    filename = sys.argv[1]
    name = Path(filename).stem

    coords = list()

    with open(filename, 'rb') as f:
        reader = Reader(f)
        print(reader.header)
        last = None
        for frame in reader:
            c = (frame.longitude, frame.latitude)
            if c != last:
                coords.append(c)
                last = c

    line = dict(type='Feature',
                geometry=dict(type='LineString', coordinates=coords),
                properties=dict())
    data = dict(type='FeatureCollection', features=[line])
    with open(f'{name}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    main()
