#!/usr/bin/env python3
"""Extract official source archives as non-executable data in the T022 root."""
import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath
import tarfile

BASE = Path('/private/tmp/outbreak-web-sdk-inspection')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('archive', type=Path)
    parser.add_argument('destination', type=Path)
    args = parser.parse_args()
    archive = args.archive.resolve()
    destination = args.destination
    if not archive.is_relative_to(BASE) or not destination.resolve().is_relative_to(BASE):
        raise ValueError('Only ticket-owned inspection paths are permitted')
    if destination.exists() or destination.is_symlink():
        raise ValueError('Destination must be new')
    for parent in destination.parents:
        if parent.is_symlink():
            raise ValueError('Symlinked destination ancestry')
    with tarfile.open(archive, 'r:gz') as source:
        members = source.getmembers()
        total = 0
        names = set()
        for member in members:
            name = PurePosixPath(member.name)
            if name.is_absolute() or '..' in name.parts or '\\' in member.name:
                raise ValueError(f'Unsafe path: {member.name}')
            if not member.isdir() and not member.isfile():
                raise ValueError(f'Links/special entries refused: {member.name}')
            if str(name) in names:
                raise ValueError(f'Duplicate entry: {name}')
            names.add(str(name))
            total += member.size
        if total > 500 * 1024 * 1024:
            raise ValueError('Source archive exceeds inspection size bound')
        destination.mkdir(parents=True)
        files = []
        for member in members:
            path = destination / member.name
            if member.isdir():
                path.mkdir(parents=True, exist_ok=True)
                continue
            path.parent.mkdir(parents=True, exist_ok=True)
            data = source.extractfile(member).read()
            with path.open('xb') as output:
                output.write(data)
            path.chmod(0o600)
            files.append({'path': str(path.relative_to(BASE)), 'sha256': hashlib.sha256(data).hexdigest(), 'bytes': len(data)})
    print(json.dumps({'archive': str(archive), 'archive_sha256': hashlib.sha256(archive.read_bytes()).hexdigest(), 'uncompressed_bytes': total, 'files': files}, indent=2))


if __name__ == '__main__':
    main()
