"""T148 stdlib DATA_ONLY closure tests; writes only new owned attempt trees."""
import copy
import json
import os
from pathlib import Path
import sys
import unittest
import uuid
import assemble as a
import validate as v


def identities(sources):
    result = {}
    for row in sources['identities']:
        path = v.REPO / row['path']
        raw = v.read(path)
        s = path.lstat()
        result[row['path']] = dict(bytes=len(raw), sha256=v.sha(raw), mode=s.st_mode,
                                  nlink=s.st_nlink, device=s.st_dev, inode=s.st_ino,
                                  mtime_ns=s.st_mtime_ns, ctime_ns=s.st_ctime_ns)
    return result


class Closure(unittest.TestCase):
    def fresh(self, suffix):
        root = self.attempt / (self._testMethodName + '-' + suffix)
        v.fixture_path(root)
        a.build(root, self.sources)
        return root

    def replace(self, path, raw):
        v.fixture_path(path)
        v.need(path.is_file() and not path.is_symlink(), 'test replacement is owned ordinary file')
        path.write_bytes(raw)

    def reject(self, root):
        with self.assertRaises((v.Refused, FileNotFoundError)):
            v.validate_package(root, self.sources)

    def test_exact_data_and_attribution(self):
        result = v.validate_package(v.HERE, self.sources)
        self.assertEqual(result['entries'], 84)
        rows = self.sources['entries']
        self.assertEqual(sum(x['source_manifest'] == v.INPUTS[0][0] for x in rows), 79)
        blackwood = [x for x in rows if x['source_manifest'] == v.INPUTS[1][0]]
        self.assertEqual(len(blackwood), 5)
        self.assertTrue(all(x['notice'] == v.RENAMES['LICENSE.txt'] for x in blackwood))
        self.assertEqual(len(v.dependencies(self.sources['blobs'])), 3)

    def test_deterministic_reproduction(self):
        root = self.fresh('reproduction')
        names = ['manifest.json', 'PROVENANCE.json'] + ['pack-root/' + x['path'] for x in self.sources['entries']]
        for name in names:
            self.assertEqual(v.read(root / name), v.read(v.HERE / name), name)

    def test_no_overwrite_or_output_selector(self):
        root = self.fresh('existing')
        before = v.read(root / 'manifest.json')
        with self.assertRaises(v.Refused):
            a.build(root, self.sources)
        self.assertEqual(v.read(root / 'manifest.json'), before)
        for outside in (v.REPO, v.HERE / 'not-a-test', v.TESTS / 'attempt-x' / '..' / 'escape'):
            with self.subTest(outside=str(outside)), self.assertRaises(v.Refused):
                a.build(outside, self.sources)

    def test_missing_tampered_extra_and_empty_directory(self):
        for case in ('missing', 'tampered', 'extra', 'empty-directory'):
            with self.subTest(case=case):
                root = self.fresh(case)
                p = root / 'pack-root/packages/maps/blackwood_greybox_v1.cgz'
                if case == 'missing':
                    p.unlink()
                elif case == 'tampered':
                    self.replace(p, v.read(p) + b'!')
                elif case == 'extra':
                    a.write_new(root / 'pack-root/extra.txt', b'extra')
                else:
                    (root / 'pack-root/empty').mkdir()
                self.reject(root)

    def test_manifest_schema_path_notice_and_source_negatives(self):
        def mutated(case, model):
            rows = model['entries']
            if case == 'missing-entry': rows.pop()
            elif case == 'extra-entry': rows.append(copy.deepcopy(rows[0]))
            elif case == 'duplicate-entry': rows[1] = copy.deepcopy(rows[0])
            elif case == 'traversal': rows[0]['path'] = '../escape'
            elif case == 'path-alias': rows[0]['path'] = 'packages/./alias'
            elif case == 'notice-collision': rows[-1]['path'] = 'LICENSE.txt'
            elif case == 'wrong-notice':
                next(x for x in rows if x['source_manifest'] == v.INPUTS[1][0])['notice'] = 'LICENSE.txt'
            elif case == 'wrong-license': rows[0]['license'] = 'CC0-1.0'
            elif case == 'wrong-source-hash': rows[0]['source_sha256'] = '0' * 64
            elif case == 'wrong-output-hash': rows[0]['sha256'] = '0' * 64
            elif case == 'wrong-source-path': rows[0]['source_path'] = 'PROVENANCE.json'
            elif case == 'wrong-virtual-path': rows[0]['virtual_path'] = '/other/LICENSE.txt'
            elif case == 'extra-field': model['overlay'] = True
            elif case == 'false-runtime-claim': model['runtime_verified'] = True
            elif case == 'bool-as-integer': model['schema_version'] = True
            elif case == 'wrong-input-pin': model['inputs'][0]['sha256'] = '0' * 64
        cases = ('missing-entry', 'extra-entry', 'duplicate-entry', 'traversal', 'path-alias',
                 'notice-collision', 'wrong-notice', 'wrong-license', 'wrong-source-hash',
                 'wrong-output-hash', 'wrong-source-path', 'wrong-virtual-path', 'extra-field',
                 'false-runtime-claim', 'bool-as-integer', 'wrong-input-pin')
        for case in cases:
            with self.subTest(case=case):
                root = self.fresh(case)
                model = v.manifest_model(self.sources)
                model = copy.deepcopy(model)
                mutated(case, model)
                self.replace(root / 'manifest.json', v.encode(model))
                self.reject(root)

    def test_json_duplicate_keys(self):
        root = self.fresh('duplicate-json')
        self.replace(root / 'manifest.json', b'{"schema_version":1,"schema_version":1}\n')
        self.reject(root)

    def test_symlink_hardlink_permissions_and_parent_alias(self):
        for case in ('symlink', 'hardlink', 'mode', 'parent-alias'):
            with self.subTest(case=case):
                root = self.fresh(case)
                pack = root / 'pack-root'
                p = pack / 'packages/maps/blackwood_greybox_v1.cgz'
                if case == 'symlink':
                    p.unlink()
                    p.symlink_to('dev_outbreak_browser.cgz')
                elif case == 'hardlink':
                    p.unlink()
                    os.link(pack / 'packages/maps/dev_outbreak_browser.cgz', p)
                elif case == 'mode':
                    p.chmod(0o600)
                else:
                    # Alias only within this fixture, never an accepted input.
                    (pack / 'packages').rename(root / 'saved-packages')
                    (pack / 'packages').symlink_to('../saved-packages', target_is_directory=True)
                self.reject(root)

    def test_notice_and_dependency_removal(self):
        for name in ('notices/blackwood-candidate/LICENSE.txt',
                     'packages/audio/outbreak/pistol.wav.LICENSE.txt',
                     'packages/textures/outbreak/ground.png'):
            with self.subTest(name=name):
                root = self.fresh(str(len(name)))
                (root / 'pack-root' / name).unlink()
                self.reject(root)
        blobs = dict(self.sources['blobs'])
        blobs.pop('packages/textures/outbreak/ground.png')
        with self.assertRaisesRegex(v.Refused, 'missing CFG dependency'):
            v.dependencies(blobs)
        blobs = dict(self.sources['blobs'])
        blobs['packages/maps/blackwood_greybox_v1.cfg'] += b'\ntexture 0 "../stock.png"\n'
        with self.assertRaises(v.Refused):
            v.dependencies(blobs)

    def test_provenance_tamper(self):
        root = self.fresh('provenance')
        model = json.loads(v.read(root / 'PROVENANCE.json'))
        model['generator_sources']['assemble.py'] = '0' * 64
        self.replace(root / 'PROVENANCE.json', v.encode(model))
        self.reject(root)

    def test_source_pin_bytes_notice_membership_and_alias(self):
        for case in ('pin', 'bytes', 'notice', 'extra', 'alias'):
            with self.subTest(case=case):
                roots = tuple(self.attempt / ('source-' + case + '-' + str(i)) for i in range(2))
                for root, (name, _, _) in zip(roots, v.INPUTS):
                    v.fixture_path(root)
                    root.mkdir()
                    source = v.REPO / Path(name).parent
                    a.write_new(root / 'manifest.json', v.read(source / 'manifest.json'))
                    for row in json.loads(v.read(source / 'manifest.json'))['entries']:
                        a.write_new(root / 'pack-root' / row['path'], v.read(source / 'pack-root' / row['path']))
                # Verify exact fixture baseline before changing one input.
                self.assertEqual(v.inspect_sources(roots)['entries'], self.sources['entries'])
                blackwood = roots[1]
                if case == 'pin':
                    self.replace(blackwood / 'manifest.json', v.read(blackwood / 'manifest.json') + b' ')
                elif case == 'bytes':
                    self.replace(blackwood / 'pack-root/packages/maps/blackwood_greybox_v1.cgz', b'corrupt')
                elif case == 'notice':
                    (blackwood / 'pack-root/LICENSE.txt').unlink()
                elif case == 'extra':
                    a.write_new(blackwood / 'pack-root/extra.txt', b'extra')
                else:
                    p = blackwood / 'pack-root/PROVENANCE.json'
                    p.unlink()
                    p.symlink_to('LICENSE.txt')
                with self.assertRaises((v.Refused, FileNotFoundError)):
                    v.inspect_sources(roots)


def main():
    v.need(not sys.argv[1:], 'no test selectors or flags')
    # No old scripts, process, network, compiler, browser or game imports/calls.
    sources = v.inspect_sources()
    before = identities(sources)
    attempt = v.TESTS / ('attempt-' + uuid.uuid4().hex)
    attempt.mkdir(parents=True, exist_ok=False)
    # Generate exactly once; subsequent test calls validate the existing final output.
    if not os.path.lexists(v.HERE / 'pack-root'):
        a.build()
    else:
        v.validate_package()
    Closure.sources, Closure.attempt = sources, attempt
    with (attempt / 'unittest.log').open('x') as stream:
        result = unittest.TextTestRunner(stream=stream, verbosity=2).run(
            unittest.defaultTestLoader.loadTestsFromTestCase(Closure))
    after_sources = v.inspect_sources()
    after = identities(after_sources)
    v.need(before == after, 'accepted inputs changed')
    report = dict(classification='DATA_ONLY', status='PASS' if result.wasSuccessful() else 'FAIL',
                  tests_run=result.testsRun, failures=len(result.failures), errors=len(result.errors),
                  source_files_checked=len(before), accepted_inputs_unchanged=before == after,
                  inputs_before=before, inputs_after=after,
                  source_fingerprints={n: v.sha(v.read(v.HERE / n)) for n in
                                       ('assemble.py', 'validate.py', 'test_assembly.py')},
                  deterministic_reproduction='test_deterministic_reproduction',
                  validation=v.validate_package(), runtime_verified=False, gameplay_verified=False)
    a.write_new(attempt / 'evidence.json', v.encode(report))
    print(v.encode({k: value for k, value in report.items() if k not in ('inputs_before', 'inputs_after')} |
                   {'evidence': attempt.relative_to(v.REPO).as_posix() + '/evidence.json'}).decode(), end='')
    raise SystemExit(0 if result.wasSuccessful() else 1)


if __name__ == '__main__':
    main()
