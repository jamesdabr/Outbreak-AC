#!/usr/bin/env python3
"""Read only original Swamp, using T281 header/entity/RLE semantics; no CFG execution."""
import gzip
import hashlib
import json
from collections import Counter
from pathlib import Path
import struct

ROOT = Path(__file__).resolve().parents[2]
path = ROOT / 'packages/maps/official/ac_swamp.cgz'
with gzip.open(path, 'rb') as stream:
    raw = stream.read(64 * 1024 * 1024)
assert len(raw) < 64 * 1024 * 1024
version, header, factor, numents = struct.unpack_from('<4i', raw, 4)
assert raw[:4] in (b'CUBE', b'ACMP') and version == 10 and 980 <= header <= 980 + (1 << 20)
extra = raw[980:header]
offset = 0


def uint():
    global offset
    value = 0
    for shift in (0, 7, 14, 21):
        assert offset < len(extra)
        byte = extra[offset]
        offset += 1
        value |= (byte if shift == 21 else byte & 127) << shift
        if not byte & 128 or shift == 21:
            return value


records = []
while offset < len(extra):
    length, flags = uint(), uint()
    assert offset + length <= len(extra)
    data = extra[offset:offset + length]
    offset += length
    if flags & 63 in (1, 5):
        records.append(dict(kind=flags & 63, text=data.rstrip(b'\0').decode('latin1')))
entities = []
pos = header
assert 0 <= numents <= 65535 and pos + 16 * numents <= len(raw)
for _ in range(numents):
    e = struct.unpack_from('<hhhhBBBBhbB', raw, pos)
    pos += 16
    entities.append(dict(x=e[0], y=e[1], z=e[2], attr1=e[3], type=e[4],
                         attr2=e[5], attr3=e[6], attr4=e[7], attr5=e[8], attr6=e[9], attr7=e[10]))
used = set()
previous = None
decoded = 0
while decoded < (1 << (factor * 2)):
    assert pos < len(raw)
    cube = raw[pos]
    pos += 1
    count = 1
    if cube == 255:
        assert previous is not None and pos < len(raw)
        count = raw[pos]
        pos += 1
        assert count > 0
        textures = previous
    elif cube == 0:
        assert pos + 2 <= len(raw)
        textures = (raw[pos],)
        pos += 2
    else:
        assert 1 <= cube <= 5 and pos + 8 <= len(raw)
        # floor, ceil, wall, floor tex, ceil tex, vdelta, upper tex, tag.
        textures = tuple(raw[pos + i] for i in (2, 3, 4, 6))
        pos += 8
    used.update(textures)
    decoded += count
    previous = textures
assert decoded == 1 << (factor * 2) and pos == len(raw)
print(json.dumps(dict(path=path.relative_to(ROOT).as_posix(), bytes=path.stat().st_size,
                      sha256=hashlib.sha256(path.read_bytes()).hexdigest(),
                      version=version, revision=struct.unpack_from('<i', raw, 924)[0],
                      flags=struct.unpack_from('<i', raw, 932)[0],
                      waterlevel=struct.unpack_from('<i', raw, 916)[0],
                      title=raw[20:148].split(b'\0', 1)[0].decode('latin1'),
                      sfactor=factor, entity_counts=dict(Counter(e['type'] for e in entities)),
                      model_slots=dict(Counter(e['attr2'] for e in entities if e['type'] == 10)),
                      sound_slots=dict(Counter(e['attr1'] for e in entities if e['type'] == 14)),
                      texture_slots=sorted(used), embedded_records=records,
                      entities=entities), indent=2))
