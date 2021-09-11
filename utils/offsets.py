from sllib.frame import Frame
import sys
import struct

"""
This was used to figure out valid offsets for frames
in a sl3 file.

Ultimately led to the discovery of channel 9 and that
flag 0x0008 probably indicates a valid packet.
"""


def main():
    filename = sys.argv[1]
    # name = Path(filename).stem
    count = 0
    last = 0
    offset = 0
    with open(filename, 'rb') as stream:
        do = True
        while do:
            stream.seek(offset)
            buf = stream.read(4)
            if buf == b'' or len(buf) < 4:
                do = False
                continue
            data = struct.unpack('<I', buf)
            # print('offset', offset, 'data', data)
            if data[0] == offset:
                stream.seek(offset)
                fr = Frame.read(stream, 3, 3200)
                now = stream.tell()
                print(
                    'match at', offset, 'now', now, 'size', offset - last, 'asd', now-offset-fr.headersize,
                    fr.to_dict(format=3, fields=['offset', 'index', 'latitude', 'packetsize', 'headersize'])
                )
                last = offset
                count += 1

            offset += 1
            if count > 20:
                break


if __name__ == "__main__":
    main()
