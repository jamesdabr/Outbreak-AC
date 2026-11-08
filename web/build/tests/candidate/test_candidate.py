"""FIXTURE_ONLY pure preparation. No real compiler, SDK, subprocess or socket.

Synthetic repositories, media, objects/logs and effect doubles are NOT build
evidence. Only the new gates/phase logic and inherited payload checks run.
"""
import copy
import io
import json
import os
from pathlib import Path
import shutil
import socket
import stat
import sys
import tempfile
import unittest
from contextlib import redirect_stderr
from unittest.mock import patch

sys.dont_write_bytecode=True
HERE=Path(__file__).absolute().parent
BUILD=HERE.parents[1]
sys.path.insert(0,str(BUILD))
import candidate_recipe as c

RUN=HERE / 'preparation-fixtures-5'


def write(path,data):
    path.parent.mkdir(parents=True,exist_ok=True)
    if isinstance(data,bytes):
        path.write_bytes(data)
    else:
        path.write_text(data)


class FixtureRecipe(c.CandidateRecipe):
    fixture_only=True

    def __init__(self,root):
        # Isolated test-only root binding; production constructor always derives
        # its repository from the installed script. No public root/plugin hook.
        super().__init__()
        self.ROOT=root; self.HERE=root / 'web/build'; self.CONFIG=self.HERE / 'network-config.json'
        self.calls=[]; self.effect=None; self.effect_index=None
        self.candidate='FIXTURE_ONLY_candidate'
        self.revision='1'*40
        write(root / '.git/HEAD',self.revision+'\n')
        for name in ('network-config.json','client-config.json','shell.html','network-shell.html'):
            write(self.HERE / name,(BUILD / name).read_bytes())
        for name in ('candidate_recipe.py','build_candidate.py','verify_candidate.py','profile_client.py'):
            write(self.HERE / name,'# FIXTURE_ONLY unexecuted source '+name+'\n')
        self.sources=['source/src/u%02d.cpp'%i for i in range(53)]
        self.sources+=['source/enet/'+name+'.c' for name in ('callbacks','compress','host','list','packet','peer','protocol')]
        self.sources+=['web/transport/enet_websocket.c']
        text='CLIENT_OBJS= \\\n'+' \\\n'.join('u%02d.o'%i for i in range(53))+'\n\nCLIENT_PCH=\n'
        write(root / 'source/src/Makefile',text)
        for name in self.sources+['source/src/shared.h','source/src/late.h','web/transport/enet_websocket.js']:
            write(root / name,'// FIXTURE_ONLY source, never compiled '+name+'\n')
        self.manifest={'entries':[]}; self.payload={}
        for i in range(79):
            name='/outbreak/f%02d'%i; raw=b'FIXTURE_ONLY payload '+str(i).encode()
            self.payload[name]=raw
            self.manifest['entries'].append(dict(virtual_path=name,bytes=len(raw),sha256=c.digest_bytes(raw)))
            write(root / 'web/assets/network-profile/pack-root' / name.split('/')[-1],raw)
        self.PACK_BYTES=sum(map(len,self.payload.values()))
        for i in range(12):
            write(self.HERE / ('notices/n%02d.txt'%i),'FIXTURE_ONLY notice %d'%i)
        write(self.HERE / '.cache/sysroot/include/fixed.h','FIXTURE_ONLY cached header')
        write(self.HERE / '.cache/ports/port.zip',b'FIXTURE_ONLY archive')
        write(self.HERE / 'out/old.html','FIXTURE_ONLY old artifact')
        write(self.HERE / 'candidate-attempts/earlier/old.log','FIXTURE_ONLY immutable earlier attempt')
        write(self.HERE / 'candidates/earlier/old.html','FIXTURE_ONLY immutable earlier candidate')
        write(root / 'source/native.o',b'FIXTURE_ONLY immutable original object')
        write(root / 'web/runtime/tests/closed-history/unused.h','FIXTURE_ONLY unconsumed historical header')
        framework=root / 'web/server/deps-signed/FIXTURE_ONLY.framework'
        write(framework / 'Versions/A/binary',b'FIXTURE_ONLY old framework')
        (framework / 'Versions/Current').symlink_to('A')
        (framework / 'binary').symlink_to('Versions/Current/binary')
        self.opaque=root / 'web/runtime/tests/closed-history/bad-link.h'
        self.opaque.symlink_to('/FIXTURE_ONLY/nonexistent/escape')
        self.tool=root / 'prerequisites/tool'
        write(self.tool,b'FIXTURE_ONLY tool never executed')
        self.port_recipe=root / 'prerequisites/port.py'
        write(self.port_recipe,'# FIXTURE_ONLY port recipe never executed')
        self.alias_doc='notes/decisions/FIXTURE_ONLY_alias.json'
        write(root / self.alias_doc,c.canonical({'fixture_only':True}))
        self.decision='notes/decisions/FIXTURE_ONLY_decision.md'
        write(root / self.decision,'FIXTURE_ONLY NOT MAIN AUTHORITY\n')
        self.source_paths=[root / n for n in self.sources+['source/src/shared.h','source/src/late.h',
            'source/src/Makefile','web/transport/enet_websocket.js']]
        self.source_paths+=[self.HERE / n for n in ('network-config.json','client-config.json','shell.html',
            'network-shell.html','candidate_recipe.py','build_candidate.py','verify_candidate.py','profile_client.py')]
        self.source_paths+=self.files(self.HERE / 'notices')+self.files(root / 'web/assets/network-profile/pack-root')
        members=sorted(set(str(p.relative_to(root)) for p in self.source_paths)|{self.alias_doc,self.decision})
        write(root / 'web/repro/source-manifest.json',c.canonical(dict(schema_version=1,kind='SOURCE_INPUT_MANIFEST',
            source_revision=self.revision,entries=[dict(path=n,**c.file_record(root / n)) for n in members])))
        self.pins_path=root / 'notes/decisions/FIXTURE_ONLY_NOT_AUTHORITY.json'
        self.refresh_pins()

    def network_backend(self):
        return {}  # Effect-double namespace only; production retains hardcoded four hashes.

    def repository_inputs(self,cfg):
        return self.snapshot(self.source_paths)

    def observe(self,strict=True,owned=()):
        cfg=self.config()
        inputs=self.repository_inputs(cfg)
        manifest=self.ROOT / 'web/repro/source-manifest.json'
        inputs.update(self.snapshot([self.tool,self.port_recipe,self.ROOT / self.alias_doc,self.ROOT / self.decision]+
            ([manifest] if manifest.exists() else [])+self.files(self.HERE / '.cache')))
        if manifest.exists():
            for row in self.manifest_document(self.revision)['entries']:
                inputs[str(self.repo(row['path']))]=row['sha256']
        observed=dict(inputs=inputs,preservation=self.preservation(owned),units=self.units(),
            ports=[dict(name='FIXTURE_ONLY',recipe=str(self.port_recipe),sha256=self.sha(self.port_recipe))],
            aliases=[dict(path=str(self.ROOT / 'prerequisites/alias'),resolved_path=str(self.tool),
                          link_text='tool',resolved_sha256=self.sha(self.tool))],
            alias_decisions={self.alias_doc:dict(sha256=self.sha(self.ROOT / self.alias_doc))},
            pack=dict(files=79,raw_bytes=self.PACK_BYTES),tool_errors=[])
        return cfg,self.manifest,observed

    def refresh_pins(self):
        _,_,obs=self.observe()
        doc=dict(schema_version=1,kind='CANDIDATE_NETWORK_BUILD_AUTHORIZATION',authority='MAIN',status='ACCEPTED',
            execution_release='EXPLICIT_CANDIDATE_NETWORK_BUILD_EXECUTION',recipe='network_v1',ticket='FIXTURE_ONLY_NOT_RELEASED',
            candidate_id=self.candidate,decision=self.decision,source_revision=self.revision,
            source_manifest=self.source_manifest(obs,self.revision),
            bindings=dict(repository=str(self.ROOT),sdk='/private/tmp/outbreak-web-sdk',ports_cache=str(self.HERE / '.cache')),
            observation=obs)
        # Conspicuous filename, ticket, source bytes and outer test scope mark
        # these synthetic documents; the real CLI's installed-root gates reject them.
        write(self.pins_path,c.canonical(doc))
        self.pins_sha=self.sha(self.pins_path)
        return doc

    def mutate_pins(self,action):
        doc=c.load_json(self.pins_path); action(doc)
        write(self.pins_path,c.canonical(doc)); self.pins_sha=self.sha(self.pins_path)

    def run_bounded(self,argv,env,log):
        index=len(self.calls); self.calls.append(argv)
        if self.effect_index==index and self.effect=='spawn-error':
            raise OSError('FIXTURE_ONLY simulated spawn failure')
        if self.effect_index==index and self.effect in ('failure','timeout','overflow'):
            write(log,b'FIXTURE_ONLY simulated command fault')
            return dict(argv=argv,environment=env,exit_code=1,log=str(log),log_sha256=self.sha(log),
                log_bytes=log.stat().st_size,elapsed_ms=1,failure={'failure':'NONZERO','timeout':'COMMAND_TIMEOUT',
                'overflow':'LOG_OVERFLOW'}[self.effect],owned_process_reaped=True)
        def dep(path,source):
            names=[self.ROOT / source,self.ROOT / 'source/src/shared.h',
                   Path(env['EM_CACHE']) / 'sysroot/include/fixed.h']
            esc=lambda p:str(p).replace('\\','\\\\').replace(' ','\\ ').replace('#','\\#')
            write(path,'FIXTURE_ONLY_TARGET: '+' '.join(esc(p) for p in names)+'\n')
        if '-M' in argv:
            source=str(Path(argv[-1]).relative_to(self.ROOT))
            dep(Path(argv[argv.index('-MF')+1]),source)
            if self.effect_index==index and self.effect=='stale-object':
                write(Path(argv[argv.index('-MT')+1]),self.MAGIC+b'FIXTURE_ONLY stale object')
        elif '-c' in argv:
            source=str(Path(argv[argv.index('-c')+1]).relative_to(self.ROOT))
            write(Path(argv[argv.index('-o')+1]),self.MAGIC+b'FIXTURE_ONLY uncompiled '+source.encode())
            dep(Path(argv[argv.index('-MF')+1]),source)
            if self.effect_index==index and self.effect=='dependency-membership':
                path=Path(argv[argv.index('-MF')+1]); path.write_text(path.read_text().rstrip()+' '+str(self.ROOT / 'source/src/late.h')+'\n')
            if self.effect_index==index and self.effect=='undeclared-header':
                undeclared=self.ROOT / 'prerequisites/undeclared.h'; write(undeclared,'FIXTURE_ONLY genuinely included unpinned header')
                path=Path(argv[argv.index('-MF')+1]); path.write_text(path.read_text().rstrip()+' '+str(undeclared)+'\n')
        elif '-o' in argv:
            root=Path(argv[argv.index('-o')+1]).parent
            write(root / 'index.html','<!-- FIXTURE_ONLY --><canvas id="canvas"></canvas><script src="index.js"></script>')
            write(root / 'index.wasm',self.MAGIC+b'FIXTURE_ONLY NOT VALIDATED WASM')
            data=bytearray(); slices=[]
            for name,raw in self.payload.items():
                start=len(data); data.extend(raw)
                slices.append('{filename:"%s",start:%d,end:%d}'%(name,start,len(data)))
            write(root / 'index.data',bytes(data))
            write(root / 'index.js','// FIXTURE_ONLY never executed\nvar files=['+','.join(slices)+'];')
        if self.effect_index==index and self.effect=='late-source':
            write(self.ROOT / 'source/src/shared.h','FIXTURE_ONLY changed after command')
        if self.effect_index==index and self.effect=='late-cache':
            write(Path(env['EM_CACHE']) / 'sysroot/include/fixed.h','FIXTURE_ONLY changed cache dependency')
        write(log,b'FIXTURE_ONLY effect double; no subprocess/compiler/runtime executed\n')
        return dict(argv=argv,environment=env,exit_code=0,log=str(log),log_sha256=self.sha(log),
                    log_bytes=log.stat().st_size,elapsed_ms=1,failure=None,owned_process_reaped=True)


class CandidateTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix='FIXTURE_ONLY-',dir=RUN / 'fixtures')
        self.addCleanup(self.tmp.cleanup)
        self.b=FixtureRecipe(Path(self.tmp.name))
        # Global audit hook below forbids real effects without monkeypatching any
        # historical module or its shared subprocess namespace.

    def execute(self):
        return self.b.execute_candidate(self.b.candidate,self.b.pins_path,self.b.pins_sha)

    def verify(self,receipt=None):
        return self.b.verify_candidate(self.b.candidate,self.b.pins_path,self.b.pins_sha,receipt)

    def deny_auth(self,action):
        self.b.mutate_pins(action)
        with self.assertRaises((ValueError,OSError,TypeError,KeyError)):
            self.execute()
        self.assertEqual(len(self.b.calls),0)
        a,p=self.b.paths(self.b.candidate); self.assertFalse(a.exists()); self.assertFalse(p.exists())

    def test_fixture_full_pipeline_and_readonly_independent_verification(self):
        result=self.execute()
        self.assertTrue(result['fixture_only']); self.assertEqual(len(result['compiles']),61)
        self.assertEqual(len(self.b.calls),125)
        before=c.protected_tree(self.b.ROOT)
        outcome=self.verify(); self.assertEqual(outcome['status'],'FIXTURE_ONLY')
        self.assertEqual(before,c.protected_tree(self.b.ROOT))

    def test_fixture_receipt_exclusive_confined_and_repeat_readonly(self):
        self.execute(); _,publication=self.b.paths(self.b.candidate)
        path=publication / 'verification/receipt.json'
        self.verify(path); self.verify()
        self.assertEqual(c.load_json(path)['status'],'FIXTURE_ONLY')
        with self.assertRaises(FileExistsError): self.verify(path)
        with self.assertRaises(ValueError): self.verify(publication / 'elsewhere.json')

    def test_real_verifier_refuses_fixture_only_before_receipt(self):
        self.execute(); self.b.fixture_only=False
        with self.assertRaisesRegex(ValueError,'FIXTURE_ONLY'): self.verify()

    def test_auth_wrong_missing_extra_identities(self):
        mutations=[lambda d:d.pop('authority'),lambda d:d.update(extra='not allowed'),
            lambda d:d.update(schema_version=True),lambda d:d.update(schema_version=1.0),
            lambda d:d.update(kind='FIXTURE_ONLY'),lambda d:d.update(authority='worker'),
            lambda d:d.update(status='SUBMITTED'),lambda d:d.update(execution_release='BUILD'),
            lambda d:d.update(recipe='arbitrary'),lambda d:d.update(candidate_id='other'),
            lambda d:d.update(ticket=''),lambda d:d.update(ticket='x'*65),
            lambda d:d.update(ticket='nonascii\u00e9'),lambda d:d.update(source_revision='2'*40)]
        original=self.b.pins_path.read_text()
        for action in mutations:
            with self.subTest(action=repr(action)):
                write(self.b.pins_path,original); self.b.pins_sha=self.b.sha(self.b.pins_path)
                self.deny_auth(action)

    def test_auth_wrong_root_manifest_digest_decision(self):
        original=self.b.pins_path.read_text()
        actions=[lambda d:d['bindings'].update(repository='/other'),
                 lambda d:d['bindings'].update(sdk='/tmp/other'),
                 lambda d:d['bindings'].update(ports_cache='/other'),
                 lambda d:d['bindings'].update(extra='x'),
                 lambda d:d['source_manifest'].update(path='other.json'),
                 lambda d:d['source_manifest'].update(sha256='0'*64),
                 lambda d:d.update(decision='notes/decisions/../other.md'),
                 lambda d:d.update(decision='notes/decisions/missing.md')]
        for action in actions:
            with self.subTest(action=repr(action)):
                write(self.b.pins_path,original); self.b.pins_sha=self.b.sha(self.b.pins_path); self.deny_auth(action)

    def test_auth_exact_all_observation_members(self):
        original=self.b.pins_path.read_text()
        for key in sorted(c.OBSERVATION):
            for value in (None,{},[],{'FIXTURE_ONLY_EXTRA':'bad'}):
                if c.exact(json.loads(original)['observation'][key],value):
                    continue
                with self.subTest(key=key,value=value):
                    write(self.b.pins_path,original); self.b.pins_sha=self.b.sha(self.b.pins_path)
                    self.deny_auth(lambda d,k=key,v=value:d['observation'].__setitem__(k,v))

    def test_observation_float_bool_counts_cannot_equal_integer(self):
        self.deny_auth(lambda d:d['observation']['pack'].update(files=79.0))

    def test_auth_duplicate_json_keys_and_bad_digest(self):
        raw=self.b.pins_path.read_text(); write(self.b.pins_path,raw.replace('"authority": "MAIN"','"authority":"MAIN","authority":"MAIN"'))
        self.b.pins_sha=self.b.sha(self.b.pins_path)
        with self.assertRaisesRegex(ValueError,'duplicate'): self.execute()
        self.assertFalse(self.b.calls)
        write(self.b.pins_path,raw); self.b.pins_sha='0'*64
        with self.assertRaisesRegex(ValueError,'digest'): self.execute()

    def test_auth_pins_relative_external_link_and_noncanonical_paths(self):
        for path in ('relative.json',str(self.b.ROOT / 'other.json'),str(self.b.ROOT)+'/notes//decisions/a.json',
                     str(self.b.ROOT / 'notes/decisions/../a.json')):
            with self.subTest(path=path),self.assertRaises((ValueError,OSError)):
                self.b.execute_candidate(self.b.candidate,path,self.b.pins_sha)
        link=self.b.pins_path.parent / 'link.json'; link.symlink_to(self.b.pins_path.name)
        with self.assertRaisesRegex(ValueError,'symlink'):
            self.b.execute_candidate(self.b.candidate,link,self.b.pins_sha)

    def test_cli_modes_unknown_flags_ids_and_missing_pins(self):
        for argv in ([],['--plan-only','--execute','--candidate-id','x'],
                     ['--plan-only','--candidate-id','x','--command','anything']):
            with redirect_stderr(io.StringIO()),self.assertRaises(SystemExit): c.build_parser().parse_args(argv)
        for name in ('','../x','/x','x/y','a'*49,'x.y','nonascii\u00e9'):
            with self.assertRaises(ValueError): self.b.paths(name)
        for name in ('a','A-z_09','a'*48): self.b.paths(name)
        _,_,obs=self.b.observe()
        with self.assertRaises(ValueError): self.b.authorization(self.b.candidate,None,None,obs)

    def test_source_manifest_wrong_schema_types_sort_duplicate_modes_hash(self):
        path=self.b.ROOT / 'web/repro/source-manifest.json'; original=path.read_text()
        mutations=[lambda d:d.update(extra=True),lambda d:d.update(schema_version=True),
            lambda d:d.update(source_revision='2'*40),lambda d:d['entries'].reverse(),
            lambda d:d['entries'].append(d['entries'][0]),lambda d:d['entries'].pop(),
            lambda d:d['entries'][0].update(mode=421),lambda d:d['entries'][0].update(bytes=True),
            lambda d:d['entries'][0].update(sha256='0'*64),lambda d:d['entries'][0].update(path='../escape')]
        for action in mutations:
            with self.subTest(action=repr(action)):
                write(path,original); doc=c.load_json(path); action(doc); write(path,c.canonical(doc))
                with self.assertRaises((ValueError,OSError)):
                    _,_,obs=self.b.observe(); self.b.source_manifest(obs,self.b.revision)

    def test_shared_manifest_declared_other_target_members_and_recursive(self):
        path=self.b.ROOT / 'web/repro/source-manifest.json'; doc=c.load_json(path)
        members=['source/outbreak/fixed.h','web/server/candidate/build.py',
                 'notes/decisions/FIXTURE_ONLY_native.md','notes/decisions/FIXTURE_ONLY_portable.md',
                 'tests/FIXTURE_ONLY/invalid.json']
        for name in members:
            extra=self.b.ROOT / name; write(extra,'FIXTURE_ONLY declared shared package member, never executable selector')
            doc['entries'].append(dict(path=name,**c.file_record(extra)))
        doc['entries'].sort(key=lambda r:r['path']); write(path,c.canonical(doc))
        self.b.refresh_pins(); _,_,obs=self.b.observe()
        self.b.source_manifest(obs,self.b.revision)
        self.assertTrue(all(str(self.b.ROOT / name) in obs['inputs'] for name in members))
        self.execute(); self.verify()
        extra=self.b.ROOT / members[0]; extra.write_text('FIXTURE_ONLY changed other-target source')
        with self.assertRaisesRegex(ValueError,'changed'): self.verify()
        extra.write_text('FIXTURE_ONLY declared shared package member, never executable selector')
        doc['entries']=[dict(path='web/repro/source-manifest.json',bytes=1,sha256='0'*64,mode=420)]
        write(path,c.canonical(doc))
        with self.assertRaisesRegex(ValueError,'recursive'): self.b.observe()

    def test_source_symlink_and_mode_change_refused(self):
        path=self.b.ROOT / 'source/src/shared.h'; path.unlink(); path.symlink_to('late.h')
        with self.assertRaisesRegex(ValueError,'symlink'): self.execute()

    def test_source_manifest_permission_mode_not_only_bytes(self):
        path=self.b.ROOT / 'source/src/shared.h'; path.chmod(0o755)
        with self.assertRaisesRegex(ValueError,'mode changed'): self.execute()
        self.assertEqual(len(self.b.calls),0)

    def test_existing_attempt_or_publication_before_effect(self):
        a,p=self.b.paths(self.b.candidate)
        p.mkdir(); write(p / 'do-not-overwrite.txt','FIXTURE_ONLY preserved')
        with self.assertRaisesRegex(ValueError,'reserved'): self.execute()
        self.assertFalse(a.exists()); self.assertEqual(self.b.calls,[])

    def test_reservation_race_retains_first_failed_owned_attempt(self):
        original=self.b.reserve
        def race(a,p):
            original(a,p); raise ValueError('FIXTURE_ONLY after exclusive reservation')
        self.b.reserve=race
        with self.assertRaisesRegex(ValueError,'reservation'): self.execute()
        a,p=self.b.paths(self.b.candidate)
        self.assertTrue(a.exists() and p.exists()); self.assertEqual(c.load_json(a / 'failure.json')['status'],'FAIL')
        with self.assertRaises(ValueError): self.execute()

    def test_second_reservation_race_never_writes_unowned_publication(self):
        a,p=self.b.paths(self.b.candidate)
        original=Path.mkdir
        def raced(path,*args,**kwargs):
            if path==p and not p.exists():
                original(p); (p / 'other-owner.txt').write_text('FIXTURE_ONLY race winner')
            return original(path,*args,**kwargs)
        with patch.object(Path,'mkdir',raced),self.assertRaises(FileExistsError): self.execute()
        self.assertEqual((p / 'other-owner.txt').read_text(),'FIXTURE_ONLY race winner')
        self.assertEqual(set(c.inventory(p)['files']),{'other-owner.txt'})
        self.assertTrue((a / 'failure.json').exists())

    def test_late_publication_failure_retained_not_success(self):
        original=self.b.verify_bundle
        _,p=self.b.paths(self.b.candidate)
        def failed(root,*args):
            tree=original(root,*args)
            if root==p: raise ValueError('FIXTURE_ONLY late publication failure')
            return tree
        self.b.verify_bundle=failed
        with self.assertRaisesRegex(ValueError,'late publication'): self.execute()
        a,_=self.b.paths(self.b.candidate)
        self.assertTrue((p / 'index.html').exists())
        self.assertTrue((a / 'failure.json').exists()); self.assertFalse((a / 'freeze.json').exists())
        with self.assertRaises((ValueError,OSError)): self.verify()

    def test_effect_failures_timeouts_overflow_never_publish_success(self):
        for effect in ('failure','timeout','overflow'):
            with self.subTest(effect=effect):
                b=FixtureRecipe(self.b.ROOT / ('FIXTURE_ONLY_'+effect))
                b.effect=effect; b.effect_index=0
                with self.assertRaisesRegex(ValueError,'command failure'): b.execute_candidate(b.candidate,b.pins_path,b.pins_sha)
                a,p=b.paths(b.candidate)
                result=c.load_json(a / 'failure.json'); self.assertEqual(result['status'],'FAIL')
                self.assertFalse((a / 'freeze.json').exists()); self.assertFalse((p / 'index.html').exists())

    def test_spawn_failure_retains_attempted_command_and_no_false_cleanup(self):
        self.b.effect='spawn-error'; self.b.effect_index=0
        with self.assertRaises(OSError): self.execute()
        a,_=self.b.paths(self.b.candidate)
        row=c.load_json(a / 'failure.json')['compiles'][0]['pre_scan']
        self.assertTrue(row['argv']); self.assertIsNone(row['exit_code'])
        self.assertEqual(row['failure'],'NOT_COMPLETED'); self.assertFalse(row['owned_process_reaped'])

    def test_late_source_cache_dependency_and_stale_object_fail(self):
        for effect,index in (('late-source',0),('late-cache',1),('dependency-membership',1),('stale-object',0)):
            with self.subTest(effect=effect):
                b=FixtureRecipe(self.b.ROOT / ('FIXTURE_ONLY_'+effect)); b.effect=effect; b.effect_index=index
                with self.assertRaises(ValueError): b.execute_candidate(b.candidate,b.pins_path,b.pins_sha)
                a,p=b.paths(b.candidate)
                self.assertEqual(c.load_json(a / 'failure.json')['status'],'FAIL'); self.assertFalse((p / 'index.html').exists())

    def test_D088_unconsumed_history_excluded_included_undeclared_header_fails(self):
        _,_,observed=self.b.observe()
        unused=str(self.b.ROOT / 'web/runtime/tests/closed-history/unused.h')
        self.assertNotIn(unused,observed['inputs'])
        manifest=c.load_json(self.b.ROOT / 'web/repro/source-manifest.json')
        self.assertNotIn('web/runtime/tests/closed-history/unused.h',{r['path'] for r in manifest['entries']})
        self.assertIn(unused,observed['preservation']['files'])
        self.b.effect='undeclared-header'; self.b.effect_index=1
        with self.assertRaisesRegex(ValueError,'undeclared compiler dependency'): self.execute()

    def test_dependency_parser_escaped_spaces_dollars_and_late_headers(self):
        path=self.b.ROOT / 'FIXTURE_ONLY.d'
        path.write_text('target\\ with\\ spaces.o: /some/a\\ b.h \\\n /some/c$$d.h\n')
        self.assertEqual(c.parse_dependencies(path,self.b.ROOT),[Path('/some/a b.h'),Path('/some/c$d.h')])
        for text in ('missing colon','target:','target: /a /a','target: ../escape'):
            write(path,text)
            with self.assertRaises(ValueError): c.parse_dependencies(path,self.b.ROOT)

    def test_compiler_commands_fixed_61_unit_socket_and_flags(self):
        cfg=self.b.config(); a,_=self.b.paths(self.b.candidate)
        result=self.b.candidate_commands(cfg,self.b.units(),a)
        self.assertEqual(len(result['compiles']),61)
        self.assertNotIn('source/enet/unix.c',[r['source'] for r in result['compiles']])
        self.assertEqual(sum(r['source']=='web/transport/enet_websocket.c' for r in result['compiles']),1)
        self.assertTrue(all('-MD' in r['command'] and '-M' in r['pre_command'] for r in result['compiles']))
        bad=copy.deepcopy(cfg); bad['link'].append('-sERROR_ON_UNDEFINED_SYMBOLS=0')
        with self.assertRaises(ValueError): self.b.candidate_commands(bad,self.b.units(),a)

    def test_fixed_config_unknown_fields_and_library_pin_rejected(self):
        paths=[self.b.HERE / 'client-config.json',self.b.CONFIG]
        originals=[p.read_text() for p in paths]
        for path in paths:
            doc=c.load_json(path); doc['unexpected']='FIXTURE_ONLY'; write(path,c.canonical(doc))
        with self.assertRaisesRegex(ValueError,'exact fields'): self.b.config()
        for path,text in zip(paths,originals): write(path,text)
        for path in paths:
            doc=c.load_json(path); doc['libpng_sha512']='0'*128; write(path,c.canonical(doc))
        with self.assertRaisesRegex(ValueError,'libpng'): self.b.config()

    def test_semantic_json_strict_opaque_tool_and_source_fixture_bytes_not_parsed(self):
        cfg=self.b.config()
        paths=self.b.configuration_json_paths(cfg,{self.b.alias_doc:{}})
        for path in paths:
            if not path.exists(): write(path,'{"fixture_only":true}')
        opaque=self.b.ROOT / 'FIXTURE_ONLY_sdk/test/malformed.json'; write(opaque,'not valid JSON, opaque tool bytes')
        self.assertNotIn(opaque,paths)
        for path in paths: c.load_json(path)
        write(self.b.CONFIG,'{"same":1,"same":1}')
        with self.assertRaisesRegex(ValueError,'duplicate'):
            for path in paths: c.load_json(path)

    def test_verifier_corruption_objects_commands_logs_payload_notices_metadata(self):
        self.execute(); a,p=self.b.paths(self.b.candidate)
        files=[a / 'objects/00.o',a / 'logs/00-compile.log',a / 'bundle/index.data',
               p / 'index.js',p / 'index.html',p / 'notices/n00.txt',p / 'build-metadata.json']
        for path in files:
            original=path.read_bytes(); path.write_bytes(original+b'FIXTURE_ONLY corruption')
            with self.subTest(path=path),self.assertRaises(ValueError): self.verify()
            path.write_bytes(original)
        path=a / 'result.json'; original=path.read_text()
        mutations=[lambda d:d.update(extra=True),lambda d:d.update(status='FAIL'),
            lambda d:d.update(object_reuse=True),lambda d:d['claims'].update(runtime=True),
            lambda d:d['claims'].update(runtime=0),lambda d:d.update(environment={}),
            lambda d:d['compiles'][0]['compile'].update(exit_code=1),
            lambda d:d['compiles'][0]['compile'].update(argv=['arbitrary']),
            lambda d:d['compiles'][0]['compile'].update(failure='COMMAND_TIMEOUT'),
            lambda d:d['compiles'][0]['compile'].update(owned_process_reaped=False),
            lambda d:d['compiles'][0].update(object=d['compiles'][1]['object']),
            lambda d:d['compiles'].pop()]
        for action in mutations:
            write(path,original); doc=c.load_json(path); action(doc); write(path,c.canonical(doc))
            with self.subTest(action=repr(action)),self.assertRaises((ValueError,KeyError)): self.verify()
        write(path,original)

    def test_phase_original_and_new_files_empty_dirs_exact(self):
        self.execute(); a,p=self.b.paths(self.b.candidate)
        for path in (self.b.HERE / 'out/unknown',self.b.HERE / 'candidates/earlier/extra',
                     a / 'objects/extra.o',a / 'unexpected.txt',p / 'extra.txt',
                     a / 'cache/extra.a',a / 'tmp/late.txt'):
            write(path,b'FIXTURE_ONLY extra')
            with self.subTest(path=path),self.assertRaises(ValueError): self.verify()
            path.unlink()
        for path in (self.b.HERE / 'out/empty-extra',a / 'logs/empty-extra',p / 'empty-extra',a / 'cache/empty-extra'):
            path.mkdir()
            with self.subTest(path=path),self.assertRaises(ValueError): self.verify()
            path.rmdir()
        self.verify()

    def test_D091_opaque_protected_links_do_not_grant_consumed_or_output_aliases(self):
        _,_,obs=self.b.observe()
        keys={'files','directories','links','absent_roots'}
        self.assertEqual(set(obs['preservation']),keys)
        record=obs['preservation']['links'][str(self.b.opaque)]
        self.assertEqual(record,dict(target=os.readlink(self.b.opaque),mode=stat.S_IMODE(self.b.opaque.lstat().st_mode)))
        self.assertNotIn(str(self.b.opaque),obs['inputs'])
        self.assertFalse(any('/Versions/Current/' in p for p in obs['preservation']['files']))
        self.execute(); self.verify()
        old=os.readlink(self.b.opaque); self.b.opaque.unlink(); self.b.opaque.symlink_to('/FIXTURE_ONLY/changed')
        with self.assertRaisesRegex(ValueError,'link membership'): self.verify()
        self.b.opaque.unlink(); self.b.opaque.symlink_to(old)
        extra=self.b.opaque.with_name('new-link'); extra.symlink_to('missing')
        with self.assertRaisesRegex(ValueError,'link membership'): self.verify()
        extra.unlink()
        a,p=self.b.paths(self.b.candidate)
        output=p / 'index.js'; output.unlink(); output.symlink_to('../../out/old.html')
        with self.assertRaisesRegex(ValueError,'symlink'): self.verify()

    def test_D091_shared_manifest_links_not_ordinary_source_and_link_modes_exact(self):
        path=self.b.ROOT / 'web/repro/source-manifest.json'; doc=c.load_json(path)
        name=str(self.b.opaque.relative_to(self.b.ROOT))
        doc['entries'].append(dict(path=name,bytes=0,sha256='0'*64,mode=420)); doc['entries'].sort(key=lambda r:r['path'])
        write(path,c.canonical(doc))
        with self.assertRaisesRegex(ValueError,'symlink'): self.b.observe()
        before=self.b.preservation(); changed=copy.deepcopy(before)
        changed['links'][str(self.b.opaque)]['mode']^=1
        with self.assertRaisesRegex(ValueError,'link membership'): self.b.protection_equal(before,changed,())

    def test_late_original_dependency_tool_port_alias_changes(self):
        self.execute()
        for path in (self.b.ROOT / 'source/src/shared.h',self.b.tool,self.b.port_recipe,
                     self.b.HERE / '.cache/ports/port.zip',self.b.ROOT / self.b.alias_doc):
            old=path.read_bytes(); path.write_bytes(old+b'FIXTURE_ONLY changed')
            with self.subTest(path=path),self.assertRaises((ValueError,json.JSONDecodeError)): self.verify()
            path.write_bytes(old)

    def test_terminal_freeze_missing_extra_unsupported_claims(self):
        self.execute(); a,p=self.b.paths(self.b.candidate)
        path=a / 'freeze.json'; old=path.read_text()
        for mutation in (lambda d:d.update(status='ACCEPTED'),lambda d:d.update(extra=1),
                         lambda d:d['attempt']['files'].pop('objects/00.o'),lambda d:d.update(elapsed_ms=3600001)):
            doc=c.load_json(path); mutation(doc); write(path,c.canonical(doc))
            with self.assertRaises(ValueError): self.verify()
            write(path,old)

    def test_published_payload_overlap_and_unindexed_suffix_rejected(self):
        self.execute(); _,p=self.b.paths(self.b.candidate)
        js=p / 'index.js'; original=js.read_text()
        altered=original.replace('start:0,','start:1,',1); write(js,altered)
        with self.assertRaisesRegex(ValueError,'overlap'): self.b.validate_payload(p,self.b.manifest)
        write(js,original); data=p / 'index.data'; data.write_bytes(data.read_bytes()+b'x')
        with self.assertRaises(ValueError): self.b.validate_payload(p,self.b.manifest)

    def test_alias_confined_chain_escape_unknown_cycle(self):
        root=self.b.ROOT / 'FIXTURE_ONLY_aliases'; root.mkdir(); write(root / 'tool',b'FIXTURE_ONLY target')
        a=root / 'a'; b=root / 'b'; a.symlink_to('b'); b.symlink_to('tool')
        records=[dict(path=str(p),link_text=os.readlink(p),resolved_path=str(root / 'tool'),resolved_sha256=self.b.sha(root / 'tool')) for p in (a,b)]
        self.b.validate_aliases(root,records)
        with self.assertRaises(ValueError): self.b.validate_aliases(root,records[:1])
        b.unlink(); b.symlink_to('a'); records[1]['link_text']='a'
        with self.assertRaises(ValueError): self.b.validate_aliases(root,records)
        b.unlink(); b.symlink_to('../escape'); records[1]['link_text']='../escape'
        with self.assertRaises(ValueError): self.b.validate_aliases(root,records)

    def test_inherited_six_port_archive_recipe_membership_gates(self):
        sdk=self.b.ROOT / 'FIXTURE_ONLY_sdk'; specs=[]; archives=[]; recipes=[]
        cfg=self.b.config(); cfg=dict(cfg,sdk_root=str(sdk))
        for name in ('sdl2','sdl2_image','zlib','vorbis','ogg','libpng'):
            recipe=sdk / ('upstream/emscripten/tools/ports/'+name+'.py')
            archive=self.b.HERE / ('.cache/ports/'+name+'.zip')
            write(recipe,'# FIXTURE_ONLY '+name); write(archive,('FIXTURE_ONLY '+name).encode())
            archives.append(archive); recipes.append(recipe)
            spec=dict(name=name,expected_sha512=self.b.sha(archive,'sha512'),recipe_sha256=self.b.sha(recipe))
            if name=='libpng':
                cfg['libpng_sha512']=spec['expected_sha512']; self.b.PNG_RECIPE=spec['recipe_sha256']
            else: specs.append(spec)
        inspection=self.b.HERE / 'sdk-inspection/sources-and-artifacts.json'
        write(inspection,c.canonical(dict(fixture_only=True,ports=specs)))
        self.assertEqual(len(c.Recipe.ports(self.b,cfg)),6)
        archive=archives[0]; raw=archive.read_bytes(); archive.write_bytes(raw+b'corrupt')
        with self.assertRaises(ValueError): c.Recipe.ports(self.b,cfg)
        archive.write_bytes(raw); extra=archive.with_name('sdl2.extra.zip'); write(extra,raw)
        with self.assertRaises(ValueError): c.Recipe.ports(self.b,cfg)
        extra.unlink(); recipes[0].write_text('# FIXTURE_ONLY changed recipe')
        with self.assertRaises(ValueError): c.Recipe.ports(self.b,cfg)

    def test_json_special_files_and_nonfinite_rejected_before_read(self):
        path=self.b.ROOT / 'FIXTURE_ONLY.json'; write(path,'{"x":NaN}')
        with self.assertRaises(ValueError): c.load_json(path)
        path.unlink(); os.mkfifo(path)
        with self.assertRaisesRegex(ValueError,'ordinary'): c.load_json(path)

    def test_plan_has_no_effect_or_candidate_reservation(self):
        result=self.b.plan(self.b.candidate)
        self.assertEqual(result['status'],'NOT_EXECUTED'); self.assertFalse(result['execution_ready'])
        a,p=self.b.paths(self.b.candidate)
        self.assertFalse(a.exists() or p.exists()); self.assertFalse(self.b.calls)

    def test_plan_pending_MAIN_manifest_is_not_execution_authority(self):
        (self.b.ROOT / 'web/repro/source-manifest.json').unlink()
        plan=self.b.plan(self.b.candidate)
        self.assertIsNone(plan['source_manifest']); self.assertEqual(plan['source_manifest_error'],'PENDING_MAIN_SOURCE_MANIFEST')
        self.assertFalse(plan['execution_ready']); self.assertTrue(plan['proposed_source_entries'])
        with self.assertRaises((ValueError,OSError)): self.execute()
        self.assertEqual(len(self.b.calls),0)


if __name__ == '__main__':
    # Fresh task-owned output only; no external /tmp or prior evidence deletion.
    RUN.mkdir(exist_ok=False)
    (RUN / 'fixtures').mkdir()
    (RUN / 'source-snapshot').mkdir()
    for source in [BUILD / n for n in ('candidate_recipe.py','build_candidate.py','verify_candidate.py')]+[Path(__file__).absolute()]:
        shutil.copyfile(source,RUN / 'source-snapshot' / source.name)
    attempted_effects=[]
    def audit(event,args):
        if event in ('subprocess.Popen','os.system','os.fork','os.posix_spawn','os.exec') or event.startswith('socket.'):
            attempted_effects.append(event)
            raise AssertionError('FIXTURE_ONLY forbidden real effect: '+event)
    sys.addaudithook(audit)
    output=io.StringIO()
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(CandidateTests)
    result=unittest.TextTestRunner(stream=output,verbosity=2).run(suite)
    (RUN / 'tests.log').write_text(output.getvalue())
    report=dict(fixture_only=True,kind='FIXTURE_ONLY_PREPARATION_RESULT',tests=result.testsRun,
        failures=len(result.failures),errors=len(result.errors),passed=result.wasSuccessful() and not attempted_effects,
        actual_compiler=False,actual_subprocess=False,actual_network=False,actual_plan=False,
        attempted_real_effects=attempted_effects,
        source_hashes={str(p):c.file_record(p)['sha256'] for p in
            [BUILD / n for n in ('candidate_recipe.py','build_candidate.py','verify_candidate.py')]+[Path(__file__).absolute()]})
    c.write_new(RUN / 'result.json',report)
    print(c.canonical(report))
    if not result.wasSuccessful():
        print(output.getvalue())
    sys.exit(0 if report['passed'] else 1)
