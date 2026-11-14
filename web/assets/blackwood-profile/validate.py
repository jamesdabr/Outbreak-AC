"""T148 fixed Blackwood assembly, DATA_ONLY. Import performs no IO."""
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys

HERE = Path(__file__).absolute().parent
REPO = HERE.parents[2]
TESTS = HERE / 'tests'
INPUTS = (
    ('web/assets/network-profile/manifest.json',
     'c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7', 79),
    ('web/assets/blackwood-candidate/manifest.json',
     'fa3049408e3ed0dbf2d4bc422b45c166b7fc0e0ac5d2fec4c8c5aadd53ae9711', 5),
)
RENAMES = {'LICENSE.txt': 'notices/blackwood-candidate/LICENSE.txt',
           'PROVENANCE.json': 'notices/blackwood-candidate/PROVENANCE.json'}
LIMITATIONS = ['CANDIDATE_NOT_BALANCE_ACCEPTED',
                'NO_RUNTIME_CAPSULE_NAV_OR_GAMEPLAY_PROOF',
                'LEGACY_STARTS_ARE_NOT_CANONICAL_SQUAD_SLOTS',
                'NO_RESOURCE_OR_ACTOR_GRANTS']
REFERENCES = ('tickets/T080.md', 'notes/decisions/D078-Blackwood-data-acceptance.md',
              'MVP/BLACKWOOD_DATA_FOUNDATION.md', 'MVP/BLACKWOOD_ASSET_ASSEMBLY.md')


class Refused(ValueError):
    pass


def need(ok, message):
    if not ok:
        raise Refused(message)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encode(value):
    return (json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True,
                       allow_nan=False) + '\n').encode('ascii')


def parse(raw):
    need(len(raw) <= 2 * 1024 * 1024, 'JSON byte bound')
    def pairs(items):
        result = {}
        for key, value in items:
            need(key not in result, 'duplicate JSON key')
            result[key] = value
        return result
    try:
        return json.loads(raw, object_pairs_hook=pairs,
                          parse_constant=lambda _: (_ for _ in ()).throw(Refused('nonfinite JSON')))
    except (UnicodeError, json.JSONDecodeError, RecursionError) as error:
        raise Refused('invalid JSON') from error


def relative(name):
    need(type(name) is str and 0 < len(name) <= 512, 'relative path type/length')
    need(re.fullmatch(r'[A-Za-z0-9_./-]+', name) is not None, 'relative path characters')
    p = PurePosixPath(name)
    need(not p.is_absolute() and str(p) == name and
         all(x not in ('', '.', '..') for x in name.split('/')), 'relative path escape/alias')
    return name


def ancestry(path):
    path = Path(path)
    need(path.is_absolute(), 'absolute internal path required')
    for p in reversed((path, *path.parents)):
        if os.path.lexists(p):
            need(not stat.S_ISLNK(p.lstat().st_mode), 'symlink ancestry')


def read(path):
    """No-follow ordinary 0644 single-link read, with identity checked around IO."""
    path = Path(path)
    ancestry(path)
    before = path.lstat()
    need(stat.S_ISREG(before.st_mode) and before.st_nlink == 1 and
         stat.S_IMODE(before.st_mode) == 0o644, 'ordinary 0644/nlink1 file required')
    need(before.st_size <= 2 * 1024 * 1024, 'file byte bound')
    fd = os.open(path, os.O_RDONLY | os.O_NOFOLLOW)
    try:
        current = os.fstat(fd)
        need((before.st_dev, before.st_ino) == (current.st_dev, current.st_ino), 'read identity replaced')
        with os.fdopen(fd, 'rb', closefd=False) as stream:
            raw = stream.read(2 * 1024 * 1024 + 1)
        after = os.fstat(fd)
    finally:
        os.close(fd)
    final = path.lstat()
    fields = ('st_dev', 'st_ino', 'st_size', 'st_mode', 'st_nlink', 'st_mtime_ns', 'st_ctime_ns')
    need(all(getattr(before, k) == getattr(after, k) == getattr(final, k) for k in fields),
         'file changed during read')
    need(len(raw) == before.st_size, 'read byte mismatch')
    return raw


def tree(root):
    """Exact file and implied-directory closure; never follow links/specials."""
    root = Path(root)
    ancestry(root)
    need(stat.S_ISDIR(root.lstat().st_mode), 'ordinary pack directory')
    files, directories = [], []
    def visit(base):
        for p in sorted(base.iterdir()):
            mode = p.lstat().st_mode
            name = p.relative_to(root).as_posix()
            relative(name)
            if stat.S_ISDIR(mode):
                directories.append(name)
                visit(p)
            else:
                need(stat.S_ISREG(mode), 'pack alias/special')
                files.append(name)
    visit(root)
    need(len({x.casefold() for x in files + directories}) == len(files + directories),
         'case alias collision')
    implied = {str(p) for n in files for p in PurePosixPath(n).parents if str(p) != '.'}
    need(set(directories) == implied, 'extra empty directory')
    return sorted(files)


def fixture_path(path):
    """Only tests/attempt-ID descendants are permitted as internal test IO roots."""
    p = Path(path).absolute()
    ancestry(p)
    need(p.is_relative_to(TESTS), 'fixture outside owned tests')
    parts = p.relative_to(TESTS).parts
    need(len(parts) >= 2 and re.fullmatch(r'attempt-[A-Za-z0-9_-]+', parts[0]),
         'fixture must be inside named attempt')
    need(all(x not in ('.', '..') for x in parts), 'fixture traversal')
    return p


def source_roots(roots):
    expected = tuple(REPO / Path(name).parent for name, _, _ in INPUTS)
    if roots is None:
        return expected
    need(type(roots) is tuple and len(roots) == 2, 'two fixture source roots')
    return tuple(fixture_path(p) for p in roots)


def inspect_sources(roots=None):
    """Production inputs are literal; optional roots are confined test copies only."""
    entries, blobs, identities = [], {}, []
    for index, ((manifest_path, digest, count), root) in enumerate(zip(INPUTS, source_roots(roots))):
        raw = read(root / 'manifest.json')
        need(sha(raw) == digest, 'pinned source manifest hash')
        manifest = parse(raw)
        rows = manifest['entries']
        need(type(rows) is list and len(rows) == count, 'source entry count')
        paths = [relative(x['path']) for x in rows]
        need(paths == sorted(paths) and len(set(paths)) == len(paths), 'source order/duplicate')
        need(tree(root / 'pack-root') == paths, 'source pack membership')
        identities.append({'path': manifest_path, 'bytes': len(raw), 'sha256': sha(raw), 'mode': 0o644, 'nlink': 1})
        for row in rows:
            source_path = relative(row['path'])
            notice = relative(row['notice'])
            need(notice in paths and type(row['license']) is str and row['license'], 'source notice/license')
            data = read(root / 'pack-root' / source_path)
            need(type(row['bytes']) is int and len(data) == row['bytes'] and sha(data) == row['sha256'],
                 'source bytes/hash')
            destination = RENAMES.get(source_path, source_path) if index else source_path
            destination = relative(destination)
            need(destination.casefold() not in {x.casefold() for x in blobs}, 'notice/path collision')
            blobs[destination] = data
            entries.append(dict(path=destination, virtual_path='/outbreak/' + destination,
                                bytes=len(data), sha256=sha(data), license=row['license'],
                                notice=RENAMES['LICENSE.txt'] if index else notice,
                                source_manifest=manifest_path, source_path=source_path,
                                source_sha256=row['sha256']))
            identities.append({'path': str(PurePosixPath(manifest_path).parent / 'pack-root' / source_path),
                               'bytes': len(data), 'sha256': sha(data), 'mode': 0o644, 'nlink': 1})
    need(len(entries) == 84, '84 entries')
    entries.sort(key=lambda x: x['path'])
    for row in entries:
        need(row['notice'] in blobs, 'assembled notice missing')
    dependencies(blobs)
    anchors = parse(blobs['packages/outbreak/blackwood_greybox_v1.anchors.json'])
    need(anchors['limitations'] == LIMITATIONS and anchors['coordinate_system'] == 'Q10_FOOT_EAST_NORTH_UP',
         'candidate limitations/coordinates')
    return {'entries': entries, 'blobs': blobs, 'identities': sorted(identities, key=lambda x: x['path'])}


def dependencies(blobs):
    """Inspect texture declarations only. CubeScript is never evaluated."""
    name = 'packages/maps/blackwood_greybox_v1.cfg'
    need(name in blobs, 'Blackwood CFG missing')
    try:
        text = blobs[name].decode('utf8')
    except UnicodeError as error:
        raise Refused('CFG encoding') from error
    found = []
    for line in text.splitlines():
        line = line.split('//', 1)[0].strip()
        if line.startswith('texture '):
            match = re.fullmatch(r'texture 0 "(outbreak/[A-Za-z0-9_.-]+\.png)"', line)
            need(match is not None, 'unexpected texture declaration')
            path = 'packages/textures/' + relative(match[1])
            need(path in blobs, 'missing CFG dependency')
            found.append(path)
    need(len(found) == 5 and set(found) == {
        'packages/textures/outbreak/ceiling.png', 'packages/textures/outbreak/ground.png',
        'packages/textures/outbreak/wall.png'}, 'exact CFG texture closure')
    return sorted(set(found))


def manifest_model(sources):
    return dict(schema_version=1, profile='BLACKWOOD_ASSET_ASSEMBLY_CANDIDATE_DATA',
                map_name='blackwood_greybox_v1', map_revision=1, mount='/outbreak',
                inputs=[{'path': p, 'sha256': h} for p, h, _ in INPUTS],
                entries=sources['entries'], raw_bytes=sum(x['bytes'] for x in sources['entries']),
                transfer_measurement='NOT_OBSERVED', assembly_performed=True,
                existing_profiles_modified=False, runtime_verified=False,
                gameplay_verified=False, candidate_balance_accepted=False)


def provenance_model(sources):
    return dict(schema_version=1, classification='DATA_ONLY',
                profile='BLACKWOOD_ASSET_ASSEMBLY_CANDIDATE_DATA',
                generator_sources={n: sha(read(HERE / n)) for n in ('assemble.py', 'validate.py')},
                inputs=[{'path': p, 'sha256': h} for p, h, _ in INPUTS],
                notice_renaming={INPUTS[1][0]: RENAMES},
                copied_source_identities=sources['identities'],
                accepted_provenance=[{'path': p, 'sha256': sha(read(REPO / p))} for p in REFERENCES],
                limitations=LIMITATIONS,
                technical_starts='8 integer native FFA starts; not 32 canonical Q10 squad slots',
                scope='ASSEMBLY_ONLY_NO_BOOT_BUILD_OVERLAY_RENDER_NAV_GAMEPLAY_BALANCE_OR_PERFORMANCE')


def package_root(root):
    p = Path(root).absolute()
    if p == HERE:
        ancestry(p)
        return p
    return fixture_path(p)


def validate_package(root=HERE, sources=None):
    root = package_root(root)
    sources = inspect_sources() if sources is None else sources
    expected = manifest_model(sources)
    raw = read(root / 'manifest.json')
    parse(raw)
    need(raw == encode(expected), 'exact manifest schema/source/license/flags mapping')
    need(tree(root / 'pack-root') == [x['path'] for x in expected['entries']], 'output pack membership')
    for row in expected['entries']:
        raw = read(root / 'pack-root' / row['path'])
        need(raw == sources['blobs'][row['path']], 'output differs from source')
        need(sha(raw) == row['sha256'] and len(raw) == row['bytes'], 'output bytes/hash')
    raw = read(root / 'PROVENANCE.json')
    parse(raw)
    need(raw == encode(provenance_model(sources)), 'exact provenance/fingerprints')
    return dict(classification='DATA_ONLY', status='PASS', entries=84,
                raw_bytes=expected['raw_bytes'], cfg_dependencies=dependencies(sources['blobs']),
                runtime_verified=False, gameplay_verified=False, candidate_balance_accepted=False)


def main():
    need(not sys.argv[1:], 'no selectors or flags permitted')
    print(encode(validate_package()).decode(), end='')


if __name__ == '__main__':
    main()
