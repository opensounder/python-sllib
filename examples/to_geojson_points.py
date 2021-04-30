import sys
import json
from pathlib import Path

from sllib import Reader


def main():
    filename = sys.argv[1]
    name = Path(filename).stem

    features = list()

    with open(filename, 'rb') as f:
        reader = Reader(f)
        print(reader.header)
        last = None
        for frame in reader:
            c = (frame.longitude, frame.latitude)
            point = dict(type='Feature',
                         geometry=dict(type='Point', coordinates=c),
                         properties=dict(water_depth_m=frame.water_depth_m,
                                         speed_kph=frame.gps_speed_kph))
            if c != last:
                features.append(point)
                last = c

    data = dict(type='FeatureCollection', features=features)
    with open(f'{name}.json', 'w') as outfile:
        json.dump(data, outfile, indent=4)


if __name__ == "__main__":
    main()
