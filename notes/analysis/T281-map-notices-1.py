#!/usr/bin/env python3
"""Read-only T281 embedded HX_MAPINFO/HX_CONFIG comment inspection; no config execution."""
import gzip
import json
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
LIMIT = 64 * 1024 * 1024


class Reader:
    def __init__(self, data):
        self.data, self.pos = data, 0

    def take(self, count):
        if self.pos + count > len(self.data):
            raise ValueError('truncated header record')
        result = self.data[self.pos:self.pos + count]
        self.pos += count
        return result

    def uint(self):
        result = 0
        for shift in (0, 7, 14, 21):
            byte = self.take(1)[0]
            result |= (byte if shift == 21 else byte & 127) << shift
            if not byte & 128 or shift == 21:
                return result

    def string(self):
        out = bytearray()
        for _ in range(255):
            byte = self.take(1)[0]
            value = (struct.unpack('<h', self.take(2))[0] if byte == 128 else
                     struct.unpack('<i', self.take(4))[0] if byte == 129 else byte)
            if value == 0:
                return out.decode('latin1')
            out.append(value & 255)
        raise ValueError('mapinfo string exceeds native bound')


def main():
    rows = []
    for path in sorted((ROOT / 'packages/maps/official').glob('*.cgz')):
        with gzip.open(path, 'rb') as stream:
            raw = stream.read(LIMIT)
        if len(raw) >= LIMIT:
            raise ValueError('decompression limit')
        version, header = struct.unpack_from('<ii', raw, 4)
        if version != 10 or not 980 <= header <= 980 + (1 << 20):
            raise ValueError('expected inspected official version10 header')
        p = Reader(raw[980:header])
        infos, comments = [], []
        while p.pos < len(p.data):
            length, flags = p.uint(), p.uint()
            data = p.take(length)
            kind = flags & 63
            if kind == 1:  # protocol.h HX_MAPINFO; worldio.cpp getstring pair.
                q = Reader(data)
                infos.append(dict(license=q.string(), comment=q.string()))
            elif kind == 5:  # HX_CONFIG: retain comments as text, never execute.
                comments.extend(line for line in data.rstrip(b'\0').decode('latin1').splitlines()
                                if line.lstrip().startswith('//'))
        rows.append(dict(name=path.stem, mapinfo=infos, embedded_config_comments=comments))
    print(json.dumps(rows, indent=2))


if __name__ == '__main__':
    main()
