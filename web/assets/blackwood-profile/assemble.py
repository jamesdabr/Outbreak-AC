"""T148 fixed-input DATA_ONLY byte-preserving assembly. Import performs no IO."""
import os
from pathlib import Path
import sys
import validate as v


def write_new(path, raw):
    path = Path(path).absolute()
    if path.is_relative_to(v.HERE) and path.relative_to(v.HERE).parts[0] in (
            'pack-root', 'manifest.json', 'PROVENANCE.json'):
        v.relative(path.relative_to(v.HERE).as_posix())
    else:
        v.fixture_path(path)
    v.ancestry(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    v.ancestry(path.parent)
    fd = os.open(path, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW, 0o644)
    try:
        os.fchmod(fd, 0o644)
        with os.fdopen(fd, 'wb', closefd=False) as stream:
            stream.write(raw)
            stream.flush()
    finally:
        os.close(fd)


def build(root=v.HERE, sources=None):
    root = v.package_root(root)
    sources = v.inspect_sources() if sources is None else sources
    # All existing final slots refuse before the first output write.
    for name in ('pack-root', 'manifest.json', 'PROVENANCE.json'):
        v.need(not os.path.lexists(root / name), 'existing assembly output: ' + name)
    manifest = v.encode(v.manifest_model(sources))
    provenance = v.encode(v.provenance_model(sources))
    root.mkdir(parents=True, exist_ok=True)
    (root / 'pack-root').mkdir()
    for name, raw in sorted(sources['blobs'].items()):
        write_new(root / 'pack-root' / v.relative(name), raw)
    write_new(root / 'manifest.json', manifest)
    write_new(root / 'PROVENANCE.json', provenance)
    return v.validate_package(root, sources)


def main():
    v.need(not sys.argv[1:], 'no selectors or flags permitted')
    print(v.encode(build()).decode(), end='')


if __name__ == '__main__':
    main()
