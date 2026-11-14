#!/usr/bin/env python3
"""T281: read-only official CGZ inventory; stdlib, sequential, <=64 MiB/map.

Mirrors world.h header and serverfiles.h RLE, tools.cpp fixmapheadersize /
calcmapdims. Does not execute configs, load game code, or write files.
Output JSON goes only to stdout. No route/navigation/playability claim.
"""
import gzip
import json
from collections import Counter
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
MAPS = ROOT / 'packages/maps/official'
LIMIT = 64 * 1024 * 1024
TYPES = ('SOLID', 'CORNER', 'FHF', 'CHF', 'SPACE', 'SEMISOLID')


def require(value, message):
    if not value:
        raise ValueError(message)


def inspect(path):
    require(path.is_file() and not path.is_symlink(), 'ordinary map required')
    with gzip.open(path, 'rb') as stream:
        raw = stream.read(LIMIT)
    require(len(raw) < LIMIT, 'decompression bound reached; refuse without further reading')
    require(len(raw) >= 916 and raw[:4] in (b'CUBE', b'ACMP'), 'map header')
    version, declared_header, factor, entities = struct.unpack_from('<4i', raw, 4)
    require(1 <= version <= 10 and 6 <= factor <= 11 and 0 <= entities <= 65535, 'header range')
    header = (916 if version < 4 else 1108 if version in (7, 8)
              else 980 if version < 10 or declared_header < 980 else declared_header)
    require(header <= 980 + (1 << 20), 'header extra bound')
    pos = header + entities * (12 if version < 10 else 16)
    require(pos <= len(raw), 'truncated entities')
    side = 1 << factor
    cells = side * side
    kind, floors, ceils = bytearray(), bytearray(), bytearray()
    previous = None

    def take(count):
        nonlocal pos
        require(pos + count <= len(raw), 'truncated geometry')
        result = raw[pos:pos + count]
        pos += count
        return result

    while len(kind) < cells:
        opcode = take(1)[0]
        count = 1
        if opcode == 255:
            require(previous is not None, 'RLE without previous cell')
            count = take(1)[0]
            require(count > 0, 'zero RLE count')
            cell = previous
        elif opcode == 254:
            require(previous is not None and version <= 2, 'legacy light repeat')
            take(2)
            cell = previous
        elif opcode == 0:
            take(2)  # Wall texture, vdelta; floor/ceil unused on SOLID.
            if version <= 2:
                take(2)
            cell = (0, 0, 16)
        else:
            require(opcode != 253, 'unoptimised solid refused by native server')
            require(opcode < len(TYPES), 'invalid cube type')
            floor, ceil = struct.unpack('bb', take(2))
            if floor >= ceil:
                floor = ceil - 1  # Native pre-12_13 compatibility correction.
                floor = (floor + 128) % 256 - 128  # Assignment to signed char.
            take(3)  # Wall/floor/ceiling textures.
            if version <= 2:
                take(2)  # Legacy light.
            take(1)  # vdelta; bounds use unadjusted heights, as calcmapdims.
            if version >= 2:
                take(1)  # Upper-wall texture.
            tag = take(1)[0] if version >= 5 else 0
            cell = (opcode | (tag & 0xC0), floor & 255, ceil & 255)
        require(len(kind) + count <= cells, 'RLE beyond canvas')
        kind.extend(bytes((cell[0],)) * count)
        floors.extend(bytes((cell[1],)) * count)
        ceils.extend(bytes((cell[2],)) * count)
        previous = cell

    counts = Counter()
    floor_counts = Counter()
    nonsolid = clipped = square_unclipped = 0
    x1 = y1 = side
    x2 = y2 = 0
    minfloor, maxceil = 127, -128
    for index, tagged in enumerate(kind):
        cube = tagged & 0x3F
        counts[TYPES[cube]] += 1
        if cube == 0:
            continue
        nonsolid += 1
        x, y = index % side, index // side
        x1, x2, y1, y2 = min(x1, x), max(x2, x), min(y1, y), max(y2, y)
        floor = floors[index] if floors[index] < 128 else floors[index] - 256
        ceil = ceils[index] if ceils[index] < 128 else ceils[index] - 256
        minfloor, maxceil = min(minfloor, floor), max(maxceil, ceil)
        floor_counts[floor] += 1
        if tagged & 0xC0:
            clipped += 1
        elif cube != 1:
            square_unclipped += 1
    require(nonsolid > 0, 'all solid map')
    require(x1 >= 2 and y1 >= 2 and x2 < side - 2 and y2 < side - 2, 'native border violation')
    preview = MAPS / 'preview' / (path.stem + '.jpg')
    return dict(name=path.stem, map_path=path.relative_to(ROOT).as_posix(),
                version=version, sfactor=factor, entities=entities,
                title=raw[20:148].split(b'\0', 1)[0].decode('latin1'),
                canvas_side=side, canvas_area=cells,
                bounds=dict(x1=x1, x2=x2, y1=y1, y2=y2),
                occupied_width=x2-x1+1, occupied_depth=y2-y1+1,
                occupied_bbox_area=(x2-x1+1)*(y2-y1+1),
                nonsolid_cells=nonsolid, tagged_clip_nonsolid_cells=clipped,
                noncorner_unclipped_cells=square_unclipped,
                minfloor=minfloor, maxceil=maxceil,
                distinct_base_floor_heights=len(floor_counts), cube_counts=dict(counts),
                interior_margins=dict(left=x1-2, right=side-3-x2, top=y1-2, bottom=side-3-y2),
                trailing_bytes=len(raw)-pos,
                preview_path=preview.relative_to(ROOT).as_posix() if preview.is_file() else None)


def main():
    paths = sorted(MAPS.glob('*.cgz'))
    require(paths, 'no official maps')
    rows, errors = [], []
    for path in paths:
        try:
            rows.append(inspect(path))
        except (OSError, EOFError, ValueError, struct.error) as error:
            errors.append(dict(name=path.stem, error=str(error)))
    print(json.dumps(dict(method='Native header/RLE and calcmapdims; geometry proxies only',
                          official_maps=len(paths), decoded=len(rows), maps=rows, errors=errors), indent=2))
    return 1 if errors else 0


if __name__ == '__main__':
    raise SystemExit(main())
