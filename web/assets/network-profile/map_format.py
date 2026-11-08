"""T064 bounded v10 map envelope/geometry inspection; never a native loader."""
import binascii
import hashlib
import importlib.util
import math
from pathlib import Path
import struct
import zlib

HERE = Path(__file__).resolve().parent
REPO = HERE.parents[2]
ENTITY = struct.Struct('<hhhhBBBBhbB')
GZIP_HEADER = bytes.fromhex('1f8b08000000000002ff')
MAX_RAW = 1024 * 1024


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(raw):
    return hashlib.sha256(raw).hexdigest()


def regular(path):
    path = Path(path).absolute()
    require('..' not in path.parts and not any(p.is_symlink() for p in (path, *path.parents)), 'unsafe/symlink path')
    return path


def confined(root, name):
    p = Path(name)
    require(bool(p.parts) and not p.is_absolute() and str(p) == name and '..' not in p.parts
            and '\\' not in name and ':' not in name, 'unsafe member path')
    return regular(regular(root) / p)


def members(root):
    root = regular(root)
    result = set()
    for p in root.rglob('*'):
        regular(p)
        if p.is_file():
            result.add(p.relative_to(root).as_posix())
    return result


def inflate(data):
    require(18 <= len(data) <= MAX_RAW, 'compressed map bounds')
    require(data[:10] == GZIP_HEADER, 'canonical gzip header/mtime/flags')
    try:
        stream = zlib.decompressobj(31)
        raw = stream.decompress(data, MAX_RAW + 1)
        require(stream.eof and not stream.unused_data and not stream.unconsumed_tail
                and len(raw) <= MAX_RAW, 'gzip bounds/truncation/trailing stream')
    except zlib.error as error:
        raise ValueError('gzip CRC/deflate: ' + str(error)) from error
    crc, size = struct.unpack('<II', data[-8:])
    require(crc == binascii.crc32(raw) & 0xffffffff and size == len(raw), 'gzip footer CRC/ISIZE')
    return raw


def deflate(raw):
    require(len(raw) <= MAX_RAW, 'decompressed map bounds')
    compressor = zlib.compressobj(9, zlib.DEFLATED, -15)
    body = compressor.compress(raw) + compressor.flush()
    return GZIP_HEADER + body + struct.pack('<II', binascii.crc32(raw) & 0xffffffff, len(raw))


def parse(data):
    raw = inflate(data)
    require(len(raw) >= 980, 'truncated map header')
    magic, version, header_size, factor, count = struct.unpack_from('<4s4i', raw)
    require((magic, version, factor) == (b'ACMP', 10, 6), 'map header identity')
    require(980 <= header_size <= 5076 and 0 < count <= 32 and header_size + ENTITY.size * count < len(raw), 'map structure bounds')
    require(ENTITY.size == 16, 'persistent_entity layout')
    records = [raw[header_size + n * 16:header_size + (n + 1) * 16] for n in range(count)]
    return dict(raw=raw, header=raw[:header_size], header_size=header_size, count=count,
                revision=struct.unpack_from('<i', raw, 924)[0], records=records,
                entities=[ENTITY.unpack(r) for r in records], geometry=raw[header_size + count * 16:])


def original_parser():
    path = regular(REPO / 'web/assets/original/validate_pack.py')
    require(digest(path.read_bytes()) == '176c5bce9892eecddfcbc5492f6567cfa502b6715e5cda5a1818f2637f65f2be', 'inspected map parser changed')
    spec = importlib.util.spec_from_file_location('t064_original_parser', path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def anchors_report(cells, starts):
    parser = original_parser()
    anchors = []
    for x, y, z, yaw in starts:
        require(parser.clear(cells, x, y, 1.1), 'radius1.1 blocked anchor')
        touched = []
        for cy in range(math.floor(y - 1.1), math.floor(y + 1.1) + 1):
            for cx in range(math.floor(x - 1.1), math.floor(x + 1.1) + 1):
                nx, ny = max(cx, min(x, cx + 1)), max(cy, min(y, cy + 1))
                if (nx - x)**2 + (ny - y)**2 < 1.1**2:
                    cell = cells[cy * 64 + cx]
                    require((cell['type'], cell['floor'], cell['ceil']) == (4, 0, 12), 'anchor exterior floor/ceiling')
                    touched.append([cx, cy])
        require(z - 4.5 >= 0 and z + 0.7 < 12, 'anchor vertical clearance')
        anchors.append(dict(x=x, y=y, z=z, yaw_encoded=yaw, yaw_degrees=yaw / 10,
                            type=2, attr2=100, other_attributes=[0, 0, 0, 0, 0],
                            floor=0, ceiling=12, radius=1.1, clearance='PASS', intersected_cells=touched))
    distances = [math.hypot(a[0] - b[0], a[1] - b[1]) for i, a in enumerate(starts) for b in starts[i + 1:]]
    require(len(starts) == 8 and min(distances) >= 16, 'anchor count/separation')
    return dict(anchors=anchors, minimum_horizontal_separation=min(distances), geometry_cells=4096,
                runtime_native_decode='NOT RUN', dedicated_mode_selection='NOT RUN', gameplay='NOT RUN',
                final_squad_deployment=False)
