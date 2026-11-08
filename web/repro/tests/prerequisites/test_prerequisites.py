"""FIXTURE_ONLY: invented tiny SDK/cache DATA; no real SDK/process/network effects."""
import copy
import contextlib
import gzip
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import stat
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
REAL=HERE.parents[3]
def module(name,file):
    spec=importlib.util.spec_from_file_location(name,file);m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m);return m
P=module('T095_fixture_producer',REAL/'web/repro/package_prerequisites.py')
S=module('T095_fixture_stager',REAL/'web/repro/stage_prerequisites.py')
CODE={name:(REAL/'web/repro'/name).read_bytes() for name in ('package_prerequisites.py','stage_prerequisites.py')}
META_NAMES=list(P.METADATA)
def put(path,data,mode=0o644):
    path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);path.chmod(mode)
def jput(path,value):put(path,P.canonical(value).encode())
class Fixture:
    def __init__(self,base=None,sdk=None):
        self.base=Path(tempfile.mkdtemp(prefix='FIXTURE_ONLY-',dir=HERE)) if base is None else base
        self.root=self.base/'repo';self.sdk=self.base/'fake-sdk' if sdk is None else sdk
        self.cache=self.root/'web/build/.cache';self.private=self.root/P.PRIVATE
        self.private.mkdir(parents=True);self.cache.mkdir(parents=True)
        for name,data in CODE.items():put(self.root/'web/repro'/name,data)
        put(self.root/'MVP/PREREQUISITE_PACKAGE.md',b'FIXTURE_ONLY approved contract stand-in\n')
        for name,data in [('upstream/emscripten/emscripten-version.txt',b'"7.0.0"\n'),('upstream/emscripten/emscripten-revision.txt',b'777e6e5db7b4990bcaeb1b9998ed642cc84e6629\n'),(P.NODE_REL,b'FIXTURE_ONLY_NODE_NEVER_EXECUTE')]:put(self.sdk/name,data,0o755 if name==P.NODE_REL else 0o644)
        aliases=[]
        for name in ('clang-24','lld','llvm-ar'):
            put(self.sdk/'upstream/bin'/name,('FIXTURE_ONLY_'+name).encode(),0o755)
        for name,target,end in [('clang','clang-24','clang-24'),('clang++','clang','clang-24'),('wasm-ld','lld','lld'),('llvm-ranlib','llvm-ar','llvm-ar')]:
            path=self.sdk/'upstream/bin'/name
            if not path.is_symlink():path.symlink_to(target)
            aliases.append(dict(path=str(path),link_text=target,resolved_path=str(self.sdk/'upstream/bin'/end),resolved_sha256=P.hash_file(self.sdk/'upstream/bin'/end)))
        a0=dict(schema_version=1,root=str(self.sdk/'upstream/bin'),aliases=aliases)
        target=self.sdk/'upstream/emscripten/node_modules/html-minifier-terser/cli.js';put(target,b'FIXTURE_ONLY_JS_DATA')
        link=self.sdk/'upstream/emscripten/node_modules/.bin/html-minifier-terser';link.parent.mkdir(parents=True,exist_ok=True)
        if not link.is_symlink():link.symlink_to('../html-minifier-terser/cli.js')
        supporting=self.sdk/'upstream/emscripten/node_modules/html-minifier-terser/package.json';put(supporting,b'{"FIXTURE_ONLY":true}')
        a1=dict(schema_version=1,root=str(self.sdk/'upstream/emscripten/node_modules'),aliases=[dict(path=str(link),link_text='../html-minifier-terser/cli.js',resolved_path=str(target),resolved_sha256=P.hash_file(target))],inspected_supporting_files={str(supporting):P.hash_file(supporting)})
        specs=[];notices=[];self.archives={}
        for name in P.PORT_NAMES:
            archive='ports/'+name+'.FIXTURE.zip';data=('FIXTURE_ONLY_ARCHIVE_'+name).encode();put(self.cache/archive,data);self.archives[name]=archive
            recipe=self.sdk/'upstream/emscripten/tools/ports'/(name+'.py');put(recipe,('FIXTURE_ONLY_RECIPE_DATA_'+name).encode())
            specs.append(dict(name=name,expected_sha512=P.digest(data,'sha512'),recipe_sha256=P.hash_file(recipe)))
            license_path='ports/'+name+'/source/LICENSE';data=('FIXTURE_ONLY_LICENSE_'+name).encode();put(self.cache/license_path,data)
            output='web/build/notices/'+{'sdl2_image':'sdl2-image'}.get(name,name)+'.txt';put(self.root/output,data)
            notices.append(dict(source='/HISTORICAL_ROOT/web/build/.cache/'+license_path,output=output,sha256=P.digest(data)))
        put(self.root/'web/build/notices/emscripten.txt',b'FIXTURE_ONLY_EMSCRIPTEN_NOTICE')
        notices.append(dict(source=str(self.sdk/'upstream/emscripten/LICENSE'),output='web/build/notices/emscripten.txt',sha256=P.digest(b'FIXTURE_ONLY_EMSCRIPTEN_NOTICE')))
        metadata={P.ALIASES[0]:a0,P.ALIASES[1]:a1,'web/build/sdk-inspection/sources-and-artifacts.json':dict(ports=specs[:5]),
          'web/build/generated/t026/port-integrity.json':[dict(FIXTURE_ONLY=True)],
          'web/build/network-config.json':dict(sdk_root=P.SDK_NAME,sdk_version='7.0.0',compiler_revision='777e6e5db7b4990bcaeb1b9998ed642cc84e6629',libpng_sha512=specs[5]['expected_sha512']),
          'web/build/notices/provenance.json':notices}
        for name,value in metadata.items():jput(self.root/name,value)
        self.metadata={name:P.hash_file(self.root/name) for name in META_NAMES};self.png=specs[5]['recipe_sha256']
        put(self.cache/'sysroot/include/data.h',b'FIXTURE_ONLY_CACHE_DATA\n')
        self.install()
        ready=dict(scope='FIXTURE_ONLY',status='PASS',producer_sha256=P.hash_file(self.root/P.PRODUCER),stager_sha256=P.hash_file(self.root/P.STAGER))
        jput(self.root/'web/repro/tests/prerequisites/FIXTURE_PASS.json',ready)
        jput(self.private/'source-freeze.json',dict(schema_version=1,scope='FROZEN_T095_PRODUCER_STAGER',producer_sha256=P.hash_file(self.root/P.PRODUCER),stager_sha256=P.hash_file(self.root/P.STAGER),contract_sha256=P.hash_file(self.root/'MVP/PREREQUISITE_PACKAGE.md'),fixtures_receipt_sha256=P.hash_file(self.root/'web/repro/tests/prerequisites/FIXTURE_PASS.json')))
    def install(self):
        for m in (P,S):m.ROOT=self.root;m.SDK=self.sdk;m.METADATA=dict(self.metadata);m.NODE_SHA=P.hash_file(self.sdk/P.NODE_REL);m.PNG_RECIPE=self.png
    def create(self):self.install();return P.create()
    def manifest(self):return json.loads((self.root/P.MANIFEST).read_text())
    def save_manifest(self,m):jput(self.root/P.MANIFEST,m);return P.hash_file(self.root/P.MANIFEST)
    def absent_destination(self):
        self.saved=self.root/'saved-original-cache';self.cache.rename(self.saved)
    def stage(self):self.install();return S.stage(self.root/P.BUNDLE,P.hash_file(self.root/P.MANIFEST))
    def mutate_bundle(self,raw):
        data=io.BytesIO()
        with gzip.GzipFile(filename='',fileobj=data,mode='wb',mtime=0,compresslevel=9) as stream:stream.write(raw)
        bundle=self.root/P.BUNDLE;bundle.write_bytes(data.getvalue())
        m=self.manifest();m['cache']['bundle'].update(bytes=bundle.stat().st_size,sha256=P.hash_file(bundle));self.save_manifest(m)
    def reject_stage(self):
        with unittest.TestCase().assertRaises((ValueError,OSError,KeyError,TypeError,IndexError,zlib_error())):self.stage()
        assert not self.cache.exists(),'FIXTURE_ONLY destination reserved before rejection'
def zlib_error():
    import zlib
    return zlib.error

class PrerequisitesTests(unittest.TestCase):
    def test_roundtrip_modes_raw_preservation(self):
        f=Fixture()
        for mode in (0o644,0o755,0o600,0o664,0o775):put(f.cache/('sysroot/include/mode-%o'%mode),bytes([mode&255]),mode)
        (f.cache/'ports/zlib').chmod(0o775)
        raw=P.source_inventory(f.cache);f.create();self.assertEqual(raw,P.source_inventory(f.cache))
        m=f.manifest();self.assertEqual(sorted(set(r['mode'] for r in m['cache']['members'])),[420,493])
        f.absent_destination();self.assertEqual(f.stage()['status'],'PASS')
        self.assertEqual(S.tree_snapshot(f.cache),m['cache']['members']);self.assertEqual(P.source_inventory(f.saved),raw)
    def test_deterministic_bytes_and_manifest(self):
        base=Path(tempfile.mkdtemp(prefix='FIXTURE_ONLY-determinism-',dir=HERE));sdk=base/'shared-sdk'
        a=Fixture(base/'a',sdk);a.create();b=Fixture(base/'b',sdk);b.create()
        self.assertEqual((a.root/P.BUNDLE).read_bytes(),(b.root/P.BUNDLE).read_bytes())
        self.assertEqual((a.root/P.MANIFEST).read_bytes(),(b.root/P.MANIFEST).read_bytes())
    def test_long_unicode_pax_roundtrip(self):
        f=Fixture();put(f.cache/'sysroot/include'/('x'*130+'é.h'),b'FIXTURE_ONLY_PAX')
        f.create();f.absent_destination();self.assertEqual(f.stage()['status'],'PASS')
    def test_source_rejections(self):
        for mode in (0o000,0o400,0o640,0o700,0o777,0o4755):
            with self.subTest(mode=oct(mode)):
                f=Fixture();put(f.cache/'bad-mode',b'FIXTURE_ONLY',mode)
                path=f.cache/'bad-mode'
                if stat.S_IMODE(path.lstat().st_mode)!=mode:
                    # Some macOS surfaces strip setuid at chmod. Model that
                    # forbidden stat mode without changing OS policy/executing it.
                    original=Path.lstat
                    def fixture_stat(p):
                        s=original(p)
                        if p==path:
                            fields=list(s);fields[0]=(s.st_mode&~0o7777)|mode
                            return os.stat_result(fields)
                        return s
                    with patch.object(Path,'lstat',fixture_stat):
                        with self.assertRaises(ValueError):P.source_inventory(f.cache)
                else:
                    with self.assertRaises(ValueError):P.source_inventory(f.cache)
        for kind in ('symlink','hardlink','fifo','game-object','empty'):
            with self.subTest(kind=kind):
                f=Fixture()
                if kind=='symlink':(f.cache/'bad').symlink_to('sysroot/include/data.h')
                elif kind=='hardlink':os.link(f.cache/'sysroot/include/data.h',f.cache/'bad')
                elif kind=='fifo':os.mkfifo(f.cache/'bad')
                elif kind=='game-object':put(f.cache/'game.cpp.o',b'\0asm\x01\0\0\0')
                else:
                    empty=f.root/'EMPTY';empty.mkdir()
                    with self.assertRaises(ValueError):P.source_inventory(empty)
                    continue
                with self.assertRaises((ValueError,OSError)):
                    raw=P.source_inventory(f.cache);P.dependency_provenance(f.cache,raw)
    def test_port_object_provenance(self):
        f=Fixture();put(f.cache/'ports/ogg/source/thing.c',b'FIXTURE_ONLY_C_SOURCE')
        put(f.cache/'build/ogg/wasm32_libogg/thing.c.o',b'\0asm\x01\0\0\0')
        self.assertEqual(len(P.dependency_provenance(f.cache,P.source_inventory(f.cache))['dependency_objects']),1)
        put(f.cache/'ports/ogg/source/other.m',b'FIXTURE_ONLY_OBJECTIVE_C_SOURCE')
        put(f.cache/'build/ogg/wasm32_libogg/other.m.o',b'\0asm\x01\0\0\0')
        self.assertEqual(len(P.dependency_provenance(f.cache,P.source_inventory(f.cache))['dependency_objects']),2)
        put(f.cache/'build/ogg/wasm32_libogg/game.cpp.o',b'\0asm\x01\0\0\0')
        with self.assertRaises(ValueError):P.dependency_provenance(f.cache,P.source_inventory(f.cache))
    def test_existing_outputs_no_overwrite(self):
        f=Fixture();f.create();before=(f.root/P.BUNDLE).read_bytes();manifest=(f.root/P.MANIFEST).read_bytes()
        with self.assertRaises(ValueError):f.create()
        self.assertEqual(before,(f.root/P.BUNDLE).read_bytes());self.assertEqual(manifest,(f.root/P.MANIFEST).read_bytes())
        source=P.source_inventory(f.cache)
        with self.assertRaises(ValueError):f.stage()
        self.assertEqual(source,P.source_inventory(f.cache))
    def test_manifest_strict_mutations(self):
        changes=[lambda m:m.update(extra=1),lambda m:m.update(schema_version=True),lambda m:m.update(recipe='other'),
          lambda m:m['cache'].update(expanded_bytes=True),lambda m:m['cache']['bundle'].update(bytes=2**30),
          lambda m:m['cache']['members'].append(copy.deepcopy(m['cache']['members'][0])),
          lambda m:m['cache']['members'].reverse(),lambda m:m['cache']['members'][0].update(path='.'),
          lambda m:m['cache']['members'][0].update(path='../escape'),lambda m:m['cache']['members'][0].update(path='/escape'),
          lambda m:m['cache']['members'][0].update(path='a\\b'),lambda m:m['cache']['members'][0].update(path='a\n'),
          lambda m:m['cache']['members'][0].update(kind='symlink'),lambda m:m['cache']['members'][0].update(mode=0o600),
          lambda m:m['cache']['members'][0].update(command='run'),lambda m:m['cache']['members'][0].update(path='PORTS'),
          lambda m:m['cache']['members'].append(dict(m['cache']['members'][0],path=m['cache']['members'][0]['path'].swapcase())),
          lambda m:m['cache']['members'][1].update(bytes=True),lambda m:m['cache']['members'][1].update(bytes=-1),
          lambda m:m['cache']['members'][1].update(bytes=2**30+1),lambda m:m['cache']['members'][1].update(sha256='G'*64),
          lambda m:m['ports'][0].update(archive_sha512='0'*128),lambda m:m['ports'][0].update(recipe='else.py'),
          lambda m:m['producer']['source'].update(sha256='0'*64),lambda m:m['producer']['stager'].update(sha256='0'*64),
          lambda m:m['sdk'].update(version='latest'),lambda m:m['sdk']['node'].update(sha256='0'*64),
          lambda m:m['sdk']['alias_decisions'][0].update(sha256='0'*64),lambda m:m['producer']['provenance'].reverse()]
        for index,change in enumerate(changes):
            with self.subTest(case=index):
                f=Fixture();f.create();f.absent_destination();m=f.manifest();change(m);f.save_manifest(m);f.reject_stage()
    def test_wrong_manifest_digest_and_duplicate_json(self):
        f=Fixture();f.create();f.absent_destination()
        with self.assertRaises(ValueError):S.stage(f.root/P.BUNDLE,'0'*64)
        path=f.root/P.MANIFEST;data=path.read_text();path.write_text(data.replace('"schema_version": 1','"schema_version": 1, "schema_version": 1'))
        f.reject_stage()
    def test_wrong_sdk_recipe_alias_provenance_code(self):
        for kind in ('producer','stager','node','version','revision','recipe','metadata','supporting','alias','parent-link','notice'):
            with self.subTest(kind=kind):
                f=Fixture();f.create();f.absent_destination()
                paths={'producer':f.root/P.PRODUCER,'stager':f.root/P.STAGER,'node':f.sdk/P.NODE_REL,
                  'version':f.sdk/'upstream/emscripten/emscripten-version.txt','revision':f.sdk/'upstream/emscripten/emscripten-revision.txt',
                  'recipe':f.sdk/'upstream/emscripten/tools/ports/sdl2.py','metadata':f.root/P.ALIASES[0],
                  'supporting':f.sdk/'upstream/emscripten/node_modules/html-minifier-terser/package.json','notice':f.root/'web/build/notices/zlib.txt'}
                if kind in paths:paths[kind].write_bytes(b'FIXTURE_ONLY_CHANGED')
                elif kind=='alias':
                    alias=f.sdk/'upstream/bin/clang++';alias.unlink();alias.symlink_to('lld')
                else:
                    parent=f.sdk/'upstream/emscripten/node_modules/.bin';parent.rename(parent.parent/'saved-bin');parent.symlink_to('saved-bin')
                f.reject_stage()
    def test_archive_semantic_corruption(self):
        for kind in ('data','missing','extra','duplicate','symlink','hardlink','special','pax','truncated','trailing-raw','trailing-gzip','crc','isize','mtime'):
            with self.subTest(kind=kind):
                f=Fixture();f.create();f.absent_destination();bundle=f.root/P.BUNDLE;compressed=bundle.read_bytes();raw=gzip.decompress(compressed)
                if kind=='data':raw=raw.replace(b'FIXTURE_ONLY_ARCHIVE_sdl2',b'BROKENXXONLY_ARCHIVE_sdl2',1)
                elif kind=='missing':raw=raw[512:]
                elif kind=='extra':raw=b'\0'*512+raw
                elif kind=='duplicate':raw=raw[:512]+raw
                elif kind in ('symlink','hardlink','special','pax'):
                    info=tarfile.TarInfo('ports');info.type={'symlink':tarfile.SYMTYPE,'hardlink':tarfile.LNKTYPE,'special':tarfile.FIFOTYPE,'pax':tarfile.XHDTYPE}[kind];info.linkname='../escape'
                    raw=info.tobuf(format=tarfile.PAX_FORMAT)+raw[512:]
                elif kind=='truncated':raw=raw[:-512]
                elif kind=='trailing-raw':raw+=bytes(10240)
                if kind not in ('trailing-gzip','crc','isize','mtime'):f.mutate_bundle(raw)
                else:
                    if kind=='trailing-gzip':changed=compressed+gzip.compress(b'EXTRA',mtime=0)
                    elif kind=='crc':changed=compressed[:-8]+b'\0'*4+compressed[-4:]
                    elif kind=='isize':changed=compressed[:-4]+b'\0'*4
                    else:changed=compressed[:4]+b'\1'+compressed[5:]
                    bundle.write_bytes(changed);m=f.manifest();m['cache']['bundle'].update(bytes=len(changed),sha256=P.digest(changed));f.save_manifest(m)
                f.reject_stage()
    def test_limits_and_paths(self):
        for value in ('','.', '..','a/../b','/abs','a//b','./a','a/','a\\b','a\x00','a\x85'):
            with self.subTest(path=repr(value)):
                for m in (P,S):
                    with self.assertRaises(ValueError):m.path_name(value)
        f=Fixture();f.create();f.absent_destination();m=f.manifest()
        with patch.object(S,'MAX_MEMBERS',1):
            with self.assertRaises(ValueError):S.manifest_schema(m)
        with patch.object(S,'MAX_BYTES',1):
            with self.assertRaises(ValueError):S.manifest_schema(m)
        with patch.object(S,'MAX_TAR',1):f.reject_stage()
        with patch.object(S,'MAX_COMPRESSED',1):f.reject_stage()
    def test_late_mutation_and_linked_destination(self):
        f=Fixture();f.create();f.absent_destination();original=S.validate_archive
        def mutate_after(stream,m,writer=None):
            result=original(stream,m,writer)
            if writer is None:(f.root/P.BUNDLE).write_bytes(b'FIXTURE_ONLY_LATE_BUNDLE')
            return result
        with patch.object(S,'validate_archive',mutate_after):f.reject_stage()
        g=Fixture();g.create();g.absent_destination();manifest=g.root/P.MANIFEST
        def mutate_manifest(stream,m,writer=None):
            result=original(stream,m,writer)
            if writer is None:manifest.write_bytes(b'FIXTURE_ONLY_LATE_MANIFEST')
            return result
        with patch.object(S,'validate_archive',mutate_manifest):g.reject_stage()
        h=Fixture();h.create();h.absent_destination();(h.root/'web/build').rename(h.root/'web/saved-build');(h.root/'web/build').symlink_to('saved-build')
        with self.assertRaises(ValueError):h.stage()
    def test_producer_late_source_mutation_preserves_failure(self):
        f=Fixture();original=P.bundle_write
        def mutate(source,bundle,members):
            (source/'sysroot/include/data.h').write_bytes(b'FIXTURE_ONLY_LATE_SOURCE')
            return original(source,bundle,members)
        with patch.object(P,'bundle_write',mutate):
            with self.assertRaises(ValueError):f.create()
        receipt=json.loads((f.private/'create-receipt.json').read_text());self.assertEqual(receipt['status'],'FAIL')
        self.assertFalse((f.root/P.MANIFEST).exists())
    def test_stage_partial_failure_retained_and_refused(self):
        f=Fixture();f.create();f.absent_destination();original=S.validate_archive
        def fail_during_copy(stream,m,writer=None):
            if writer is not None:
                writer(m['cache']['members'][0],None)
                raise ValueError('FIXTURE_ONLY injected post-reservation copy failure')
            return original(stream,m,writer)
        with patch.object(S,'validate_archive',fail_during_copy):
            with self.assertRaises(ValueError):f.stage()
        self.assertTrue(f.cache.is_dir());reports=list(f.private.glob('stage-*.json'));self.assertEqual(len(reports),1)
        receipt=reports[0].read_bytes();self.assertEqual(json.loads(receipt)['status'],'FAIL')
        self.assertTrue(json.loads(receipt)['partial_destination'])
        with self.assertRaises(ValueError):f.stage()
        self.assertEqual(reports[0].read_bytes(),receipt)
    def test_cli_boundary_guards(self):
        f=Fixture()
        for m in (P,S):
            for event in ('subprocess.Popen','socket.connect','os.system'):
                with self.assertRaises(RuntimeError):m.boundary_guard(event,())
            with self.assertRaises(ValueError):m.boundary_guard('open',(f.sdk/'NEW_BAD','w',os.O_WRONLY|os.O_CREAT))
        with self.assertRaises(ValueError):P.boundary_guard('os.chmod',(f.cache/'sanity.txt',0o644))
        P.boundary_guard('open',(f.root/P.MANIFEST,'w',os.O_WRONLY|os.O_CREAT))
        S.boundary_guard('open',(f.cache/'NEW_ALLOWED','w',os.O_WRONLY|os.O_CREAT))
    def test_source_freeze_and_stale_fixture_refusal(self):
        for kind in ('producer_sha256','stager_sha256','contract_sha256','fixture_binding'):
            with self.subTest(kind=kind):
                f=Fixture();freeze_path=f.private/'source-freeze.json';freeze=json.loads(freeze_path.read_text())
                if kind=='fixture_binding':
                    fixture_path=f.root/'web/repro/tests/prerequisites/FIXTURE_PASS.json';fixture=json.loads(fixture_path.read_text());fixture['producer_sha256']='0'*64
                    jput(fixture_path,fixture);freeze['fixtures_receipt_sha256']=P.hash_file(fixture_path)
                else:freeze[kind]='0'*64
                jput(freeze_path,freeze);before=P.source_inventory(f.cache)
                with self.assertRaises(ValueError):f.create()
                self.assertEqual(before,P.source_inventory(f.cache));self.assertFalse((f.root/P.BUNDLE).exists());self.assertFalse((f.root/P.MANIFEST).exists())
    def test_independent_readonly_archive_reviewer_fixture(self):
        f=Fixture();put(f.cache/'sysroot/include'/('p'*130+'é.txt'),b'FIXTURE_ONLY_INDEPENDENT_PAX',0o600);f.create()
        v=module('T095_fixture_independent_review',HERE/'verify_real.py')
        v.ROOT=f.root;v.OUT=f.private;v.SDK=f.sdk;v.NODE_SHA=P.hash_file(f.sdk/P.NODE_REL)
        # The test process already has the stronger FIXTURE_ONLY audit hook.
        # Do not install an additional permanent per-fixture receipt-only hook.
        with patch.object(v,'guard',lambda *args:None),contextlib.redirect_stdout(io.StringIO()):v.main()
        receipt=json.loads((f.private/'independent-real-verification.json').read_text())
        self.assertEqual(receipt['status'],'PASS');self.assertTrue(receipt['raw_source_unchanged']);self.assertGreater(receipt['pax_member_count'],0)

class T101MissingReportPolicyTests(unittest.TestCase):
    @contextlib.contextmanager
    def actual_policy(self):
        active=[True]
        def forward(event,args):
            if active[0]:S.boundary_guard(event,args)
        sys.addaudithook(forward)
        try:yield
        finally:active[0]=False
    def clean_layout(self):
        f=Fixture();put(f.cache/'sysroot/include/T101-data.h',b'FIXTURE_ONLY_T101_DATA',0o600)
        f.create();external=f.base/'supplied-external.tar.gz';external.write_bytes((f.root/P.BUNDLE).read_bytes())
        raw=P.source_inventory(f.cache);f.absent_destination()
        parent=f.root/'web/repro/prerequisite-bundles';parent.rename(f.root/'saved-fixture-package-proof')
        self.assertFalse(parent.exists());self.assertFalse(f.private.exists());self.assertFalse(f.cache.exists())
        return f,external,raw
    def test_T101_missing_hierarchy_actual_policy_roundtrip_and_refusals(self):
        f,bundle,raw=self.clean_layout();manifest_sha=P.hash_file(f.root/P.MANIFEST)
        with self.actual_policy():receipt=S.stage(bundle,manifest_sha)
        self.assertEqual(receipt['status'],'PASS');self.assertEqual(S.tree_snapshot(f.cache),f.manifest()['cache']['members'])
        self.assertEqual(P.source_inventory(f.saved),raw)
        report=f.private/('stage-'+manifest_sha+'.json');report_bytes=report.read_bytes()
        self.assertTrue(report.is_file());self.assertTrue(f.private.parent.is_dir())
        staged=S.tree_snapshot(f.cache)
        with self.actual_policy():
            with self.assertRaises(ValueError):S.stage(bundle,manifest_sha)
        self.assertEqual(S.tree_snapshot(f.cache),staged);self.assertEqual(report.read_bytes(),report_bytes)
        f.cache.rename(f.root/'saved-staged-cache')
        with self.actual_policy():
            with self.assertRaises(ValueError):S.stage(bundle,manifest_sha)
        self.assertFalse(f.cache.exists());self.assertEqual(report.read_bytes(),report_bytes)
        self.assertEqual(P.source_inventory(f.saved),raw)
    def test_T101_invalid_inputs_create_no_hierarchy_under_actual_policy(self):
        for kind in ('manifest-digest','manifest-schema','bundle'):
            with self.subTest(kind=kind):
                f,bundle,raw=self.clean_layout();expected=P.hash_file(f.root/P.MANIFEST)
                if kind=='manifest-digest':expected='0'*64
                elif kind=='manifest-schema':
                    m=f.manifest();m['unapproved']=True;expected=f.save_manifest(m)
                else:bundle.write_bytes(b'FIXTURE_ONLY_INVALID_BUNDLE')
                with self.actual_policy():
                    with self.assertRaises(ValueError):S.stage(bundle,expected)
                self.assertFalse(f.cache.exists());self.assertFalse(f.private.parent.exists());self.assertEqual(P.source_inventory(f.saved),raw)
    def test_T101_exact_parent_mkdir_only_other_effects_and_links_denied(self):
        f,bundle,raw=self.clean_layout();parent=f.private.parent
        with self.actual_policy():parent.mkdir()
        with self.actual_policy():
            for target in (f.root/'NEW_ANCESTOR',f.root/'web/repro',f.root/'web/repro/prerequisite-bundles-SIBLING',parent/'SIBLING'):
                with self.subTest(target=str(target)):
                    with self.assertRaises(ValueError):target.mkdir(exist_ok=True)
            with self.assertRaises(ValueError):parent.open('wb')
            with self.assertRaises(ValueError):(parent/'BAD_FILE').write_bytes(b'FIXTURE_ONLY')
            with self.assertRaises(ValueError):parent.chmod(0o755)
            with self.assertRaises(ValueError):parent.rmdir()
            with self.assertRaises(ValueError):parent.rename(f.root/'MOVED')
        self.assertTrue(parent.is_dir());self.assertFalse((parent/'BAD_FILE').exists());self.assertFalse(f.cache.exists())
        g,external,original=self.clean_layout();g.private.parent.symlink_to(g.root/'saved-fixture-package-proof')
        with self.actual_policy():
            with self.assertRaises(ValueError):S.stage(external,P.hash_file(g.root/P.MANIFEST))
        self.assertTrue(g.private.parent.is_symlink());self.assertFalse(g.cache.exists());self.assertEqual(P.source_inventory(g.saved),original)

def audit(event,args):
    if event.startswith(('subprocess.','socket.')) or event in ('os.system','os.posix_spawn','os.fork','os.exec'):
        raise RuntimeError('FIXTURE_ONLY process/network boundary forbidden')
    paths=[]
    if event=='open':
        path,mode,flags=args
        if isinstance(path,(str,bytes,os.PathLike)):
            p=Path(os.fsdecode(path)).absolute()
            if p.is_relative_to(Path('/private/tmp/outbreak-web-sdk')):raise RuntimeError('FIXTURE_ONLY real SDK access forbidden')
            if flags&(os.O_WRONLY|os.O_RDWR|os.O_CREAT|os.O_TRUNC|os.O_APPEND):paths=[p]
    elif event in ('os.mkdir','os.chmod','os.remove','os.rmdir','os.mkfifo','os.truncate','os.utime'):paths=[args[0]]
    elif event in ('os.rename','os.link'):paths=list(args[:2])
    elif event=='os.symlink':paths=[args[1]]
    for path in paths:
        require_path=Path(os.fsdecode(path)).absolute()
        if not require_path.is_relative_to(HERE):raise RuntimeError('FIXTURE_ONLY outside write: '+str(require_path))

if __name__=='__main__':
    sys.addaudithook(audit)
    number=1
    while (HERE/('fixture-attempt-%d.json'%number)).exists():number+=1
    capture=io.StringIO();result=unittest.TextTestRunner(stream=capture,verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PrerequisitesTests))
    (HERE/('fixture-attempt-%d.txt'%number)).write_text(capture.getvalue())
    receipt=dict(schema_version=1,scope='FIXTURE_ONLY',status='PASS' if result.wasSuccessful() else 'FAIL',tests=result.testsRun,failures=len(result.failures),errors=len(result.errors),
      producer_sha256=P.digest(CODE['package_prerequisites.py']),stager_sha256=P.digest(CODE['stage_prerequisites.py']),effects='real SDK/process/network forbidden by audit hook; fake data only',fixture_failures_preserved=True)
    jput(HERE/('fixture-attempt-%d.json'%number),receipt)
    if result.wasSuccessful():jput(HERE/'FIXTURE_PASS.json',receipt)
    print(P.canonical(receipt));sys.exit(0 if result.wasSuccessful() else 1)
