"""FIXTURE_ONLY: temporary fake files/Mach-O/commands. All real effects forbidden."""
import ast,copy,json,os,shlex,struct,tempfile,time,unittest
from pathlib import Path
from unittest.mock import patch
import stage,build,verify

def retained_otool(path):
 data=stage.loads((Path(__file__).parent/'preparation-T098-20261108-1/retained-otool.json').read_bytes())
 row=next(r for r in data['rows'] if r['inspected_path'].endswith('/hidapi')==path.endswith('/hidapi'))
 return row['stdout'].replace(row['inspected_path'],path)

def fake_macho(kind,paths=()):
 blocks=[]
 for path in paths:
  data=path.encode()+b'\0';size=(12+len(data)+7)//8*8;blocks.append(struct.pack('<III',0x8000001c,size,12)+data+b'\0'*(size-12-len(data)))
 if kind!=1:blocks.append(struct.pack('<IIII',0x1d,16,32+sum(map(len,blocks))+16,16))
 return struct.pack('<8I',0xfeedfacf,0x100000c,0,kind,len(blocks),sum(map(len,blocks)),0,0)+b''.join(blocks)+(b'FIXTURE_ONLY_SIG' if kind!=1 else b'FIXTURE_ONLY_OBJECT')

class Fixture:
 def __init__(self,root):
  root=root.resolve();self.root=str(root);self.external={};self.sdk_root=root/'EXTERNAL/SDK';self.ident='FIXTURE_ONLY';self.pin=root/'notes/decisions/FIXTURE_ONLY.json';self.view=None
  def put(name,data=b'FIXTURE_ONLY\n',mode=420):
   p=root/name;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data);p.chmod(mode);return p
  self.put=put;put('.git/HEAD',b'1'*40+b'\n');put('notes/decisions/FIXTURE_ONLY.md');put('notes/decisions/OTHER.md');put('source/game/portable.h');put('web/runtime/tests/historical/unconsumed.h')
  put('source/src/Makefile',('SERVER_OBJS= \\\n'+''.join('\t'+Path(x).stem+'-standalone.o'+(' \\\n' if i<7 else '\n') for i,x in enumerate(stage.CPP))+'MASTER_OBJS=x\n').encode())
  put('source/enet/Makefile.am',('libenet_la_SOURCES = '+' '.join(Path(x).name for x in stage.C)+' win32.c\n').encode())
  for name in stage.CPP+stage.C+['source/src/sound.h']:put(name)
  for name in stage.SCRIPT_NAMES:put('web/server/candidate/'+name)
  frame=Path(stage.FRAMEWORK);put(str(frame/'COPYING.txt'));put(str(frame/'Versions/A/Headers/SDL.h'));put(str(frame/'Versions/A/SDL2'),fake_macho(6),493);put(str(frame/'Versions/A/Frameworks/hidapi.framework/Versions/A/hidapi'),fake_macho(6),493)
  (root/frame/'Headers').symlink_to('Versions/Current/Headers');(root/frame/'Versions/Current').symlink_to('A')
  # Opaque old history may intentionally be malformed; never a consumed alias.
  old=root/'web/server/deps-signed';old.mkdir(parents=True);(old/'opaque').symlink_to('/FIXTURE_ONLY/nonexistent/outside')
  for name in [*stage.TOOLS.values(),stage.CLT+'/usr/bin/clang',stage.CLT+'/usr/bin/ld',stage.CLT+'/usr/lib/clang/17/include/stddef.h',stage.PYTHON+'/bin/python3']:
   self.ext(name)
  for name in ['SDKSettings.json','usr/include/zlib.h','usr/include/pthread/pthread.h','usr/include/pthread/sched.h','usr/lib/libz.tbd','usr/lib/libpthread.tbd','usr/lib/libc++.tbd']:self.ext(stage.SDK+'/'+name,b'{"Version":"15.5"}' if name=='SDKSettings.json' else b'FIXTURE_ONLY_SDK')
  for name,text,mode,_ in stage.SDK_HEADER_ALIASES:
   alias=self.sdk_root/name[len(stage.SDK)+1:];alias.symlink_to(text);os.lchmod(alias,mode);self.external[name]=alias
  self.view=FixtureView(self)
  entries=[]
  package=stage.CPP+stage.C+['source/src/sound.h','source/src/Makefile','source/enet/Makefile.am','notes/decisions/FIXTURE_ONLY.md','notes/decisions/OTHER.md','source/game/portable.h']+['web/server/candidate/'+n for n in stage.SCRIPT_NAMES]
  package+=['source/xcode/Frameworks/SDL2.framework/'+n for n,row in self.view.framework().items() if row['kind']=='file']
  for name in sorted(package):p=root/name;entries.append({'path':name,'bytes':p.stat().st_size,'sha256':stage.sha(p.read_bytes()),'mode':self.view.mode(str(p))})
  manifest={'schema_version':1,'kind':'SOURCE_INPUT_MANIFEST','source_revision':'1'*40,'entries':entries};put('web/repro/source-manifest.json',stage.canonical_json(manifest).encode())
  inputs={self.root+'/'+e['path']:e['sha256'] for e in entries};inputs[self.root+'/web/repro/source-manifest.json']=self.view.hash(self.root+'/web/repro/source-manifest.json');inputs.update({n:self.view.hash(n) for n in self.external if self.view.ordinary(n) and self.view.canonical(n)==n})
  sdkfiles={n[len(stage.SDK)+1:]:self.view.hash(n) for n in self.external if n.startswith(stage.SDK+'/') and self.view.ordinary(n) and self.view.canonical(n)==n}
  self.auth={'schema_version':1,'kind':'CANDIDATE_NATIVE_BUILD_AUTHORIZATION','authority':'MAIN','status':'ACCEPTED','execution_release':'EXPLICIT_CANDIDATE_NATIVE_BUILD_EXECUTION','recipe':'native_standalone_v1','ticket':'FIXTURE_ONLY_NOT_REAL_AUTHORITY','candidate_id':self.ident,'decision':'notes/decisions/FIXTURE_ONLY.md','source_revision':'1'*40,'source_manifest':{'path':'web/repro/source-manifest.json','sha256':self.view.hash(self.root+'/web/repro/source-manifest.json')},'bindings':{'repository':self.root,'system_sdk':stage.SDK,'source_framework':self.root+'/'+stage.FRAMEWORK},'observation':{'inputs':inputs,'preservation':self.view.preservation(),'source_framework':self.view.framework(),'units':{'cpp':stage.CPP,'c':stage.C},'tools':{k:{'path':p,'sha256':self.view.hash(p)} for k,p in stage.TOOLS.items()},'system_sdk':{'root':stage.SDK,'files':sdkfiles},'flags':{m:stage.flags(self.root,self.ident,m) for m in ('release','debug')},'errors':[]}}
  self.write()
 def ext(self,name,data=b'FIXTURE_ONLY_TOOL'):
  path=self.sdk_root/name[len(stage.SDK)+1:] if name.startswith(stage.SDK+'/') else Path(self.root)/'EXTERNAL'/stage.sha(name.encode());path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(data);self.external[name]=path
 def write(self):self.pin.write_text(stage.canonical_json(self.auth));self.digest=stage.sha(self.pin.read_bytes())
 def output(self):return Path(stage.attempt(self.root,self.ident))

class FixtureView(stage.View):
 def __init__(self,f):self.fixture=f;self.root=f.root
 def mapped(self,name):return self.fixture.sdk_root/name[len(stage.SDK)+1:] if name.startswith(stage.SDK+'/') else self.fixture.external.get(name,Path(name))
 def ordinary(self,name):p=self.mapped(name);return p.is_file() and not p.is_symlink()
 def canonical(self,name):
  if name.startswith(stage.SDK+'/'):
   physical=self.mapped(name).resolve(strict=True);return stage.SDK+'/'+str(physical.relative_to(self.fixture.sdk_root)) if physical.is_relative_to(self.fixture.sdk_root) else str(physical)
  return name if name in self.fixture.external else str(Path(name).resolve(strict=True))
 def ordinary_ancestors(self,name):return super().ordinary_ancestors(self.mapped(name))
 def link_identity(self,name):return super().link_identity(self.mapped(name))
 def hash(self,name):return stage.sha(self.mapped(name).read_bytes())
 def size(self,name):return self.mapped(name).stat().st_size
 def mode(self,name):return self.mapped(name).stat().st_mode&0o7777
 def text(self,name):return self.mapped(name).read_text()
 def json(self,name):return stage.loads(self.mapped(name).read_bytes())
 def preservation(self):return stage.preservation_record(self.root,getattr(self,'active',None),browser_sdk=None,omit_container=getattr(self,'omit_container',False))
 def authoring_files(self):p=stage.PYTHON+'/bin/python3';return {p:self.hash(p)}

class FakeRunner:
 failure=None;include_undeclared=False;wrong_signature=False;wrong_dylib=False;retained_fat=False
 def __init__(self,root,base,persist=True):self.root=Path(root);self.base=Path(base);self.persist=persist;self.records=[];self.started=time.monotonic();self.env={'PATH':'/usr/bin:/bin:/usr/sbin:/sbin','TMPDIR':str(self.base/'tmp'),'CLANG_MODULE_CACHE_PATH':str(self.base/'tmp/modules')}
 def run(self,kind,argv):
  i=len(self.records);out='';err='';bad=kind=='compile' and self.failure is not None
  if '--version' in argv:out='Apple clang version 17.0.0 FIXTURE_ONLY\nTarget: arm64-apple-darwin25\nInstalledDir: '+stage.CLT+'/usr/bin\n'
  elif kind=='adhoc_sign_copy':
   p=Path(argv[-1])/('Versions/A/hidapi' if argv[-1].endswith('hidapi.framework') else 'Versions/A/SDL2');b=p.read_bytes();p.write_bytes(b[:-1]+b'X')
  elif kind in ('discover_dependencies','compile') and not bad:
   source=argv[-1] if kind=='discover_dependencies' else argv[argv.index('-c')+1];obj=argv[argv.index('-MT')+1] if kind=='discover_dependencies' else argv[argv.index('-o')+1];dep=argv[argv.index('-MF')+1]
   names=[source,str(self.root/'source/src/sound.h'),str(self.base/'deps-signed/SDL2.framework/Headers/SDL.h'),stage.SDK+'/usr/include/zlib.h',stage.SDK_PTHREAD_ALIAS[0],stage.SDK_SCHED_ALIAS[0],stage.CLT+'/usr/lib/clang/17/include/stddef.h']
   if self.include_undeclared:names.append(str(self.root/'web/runtime/tests/historical/unconsumed.h'))
   Path(dep).write_text(obj+': '+' '.join(shlex.quote(n) for n in names)+'\n')
   if kind=='compile':Path(obj).write_bytes(fake_macho(1))
  elif kind=='link':
   rpaths=[str(self.base/'deps-signed'),str(self.base/'deps-signed/SDL2.framework/Versions/A/Frameworks')];Path(argv[-1]).write_bytes(fake_macho(2,rpaths));Path(argv[-1]).chmod(493);out='\n'.join([x for x in argv if x.endswith('.o')]+[str(self.base/'deps-signed/SDL2.framework/Versions/A/SDL2'),stage.SDK+'/usr/lib/libz.tbd',stage.SDK+'/usr/lib/libpthread.tbd'])+'\n'
  elif argv[0]==stage.TOOLS['file']:
   typ=struct.unpack_from('<I',Path(argv[-1]).read_bytes(),12)[0];out='Mach-O 64-bit '+('object' if typ==1 else 'executable' if typ==2 else 'dynamically linked shared library')+' arm64\n'
  elif argv[0]==stage.TOOLS['otool']:
   p=argv[-1];out=p+':\n'
   if argv[1]=='-L':
    if self.wrong_dylib:out+='\t/FIXTURE_ONLY/escape.dylib (compatibility version 1.0.0, current version 1.0.0)\n'
    elif self.retained_fat and not p.endswith('/ac_server'):out=retained_otool(p)
    else:out+='\t@rpath/SDL2.framework/Versions/A/SDL2 (compatibility version 1.0.0, current version 1.0.0)\n\t/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1.0.0)\n'
   else:
    paths=[str(self.base/'deps-signed'),str(self.base/'deps-signed/SDL2.framework/Versions/A/Frameworks')] if p.endswith('/ac_server') else ['@loader_path/Frameworks']
    out+=''.join('Load command 0\n cmd LC_RPATH\n cmdsize 32\n path '+x+' (offset 12)\n' for x in paths)
  elif '--display' in argv:err=('Signature=other' if self.wrong_signature else 'Signature=adhoc')+'\nFIXTURE_ONLY not real signing\n'
  if bad:err='FIXTURE_ONLY injected '+self.failure
  row={'index':i,'kind':kind,'argv':list(argv),'environment':self.env,'timeout_s':120,'exit':1 if bad else 0,'timed_out':self.failure=='timeout' and bad,'overflow':self.failure=='overflow' and bad,'kill_fallback':False,'group_reaped':True,'elapsed_ms':1.0,'stdout_path':f'logs/{i:03d}.stdout','stderr_path':f'logs/{i:03d}.stderr','stdout_sha256':stage.sha(out.encode()),'stderr_sha256':stage.sha(err.encode())};self.records.append(row)
  if self.persist:
   for k,s in [('stdout',out),('stderr',err)]:(self.base/row[k+'_path']).write_text(s)
  if bad:raise stage.Refused('FIXTURE_ONLY command '+self.failure)
  return i,out,err

REAL_PROTECTED=stage.protected_inventory
CAPTURE_RUNNER=build.Runner
class Preparation(unittest.TestCase):
 def setUp(self):
  self.patches=[patch('subprocess.Popen',side_effect=AssertionError('REAL PROCESS FORBIDDEN')),patch('subprocess.run',side_effect=AssertionError('REAL PROCESS FORBIDDEN')),patch('subprocess.check_output',side_effect=AssertionError('REAL PROCESS FORBIDDEN')),patch('socket.socket',side_effect=AssertionError('REAL SOCKET FORBIDDEN')),patch('os.system',side_effect=AssertionError('REAL PROCESS FORBIDDEN')),patch('os.posix_spawn',side_effect=AssertionError('REAL PROCESS FORBIDDEN'))]
  for p in self.patches:p.start()
  self.tmp=tempfile.TemporaryDirectory(prefix='T092-FIXTURE_ONLY-');self.f=Fixture(Path(self.tmp.name));self.patches += [patch.object(stage,'View',lambda root:self.f.view),patch.object(stage,'protected_inventory',lambda root,active=None,omit_container=False:REAL_PROTECTED(root,active,omit_container,browser_sdk=None)),patch.object(build,'Runner',FakeRunner),patch.object(verify,'Runner',FakeRunner)]
  for p in self.patches[6:]:p.start()
  FakeRunner.failure=None;FakeRunner.include_undeclared=False;FakeRunner.wrong_signature=False;FakeRunner.wrong_dylib=False;FakeRunner.retained_fat=False
 def tearDown(self):
  for p in reversed(self.patches):p.stop()
  self.tmp.cleanup()
 def gate(self):return stage.authorize(self.f.pin.read_bytes(),self.f.digest,self.f.ident,self.f.view)
 def pipeline(self):return build.execute(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_fixed_plan_no_effects(self):
  p=build.plan(self.f.root,self.f.ident);self.assertEqual(p['status'],'NOT_RUN');spec=p['recipe'];self.assertEqual(sum(len(m['units']) for m in spec['modes'].values()),32);self.assertEqual(len(spec['sign']),2);self.assertTrue(spec['sign'][0][-1].endswith('hidapi.framework'));self.assertFalse(self.f.output().exists())
 def test_fixture_gate_and_shared_package(self):
  self.gate();self.assertIn('source/game/portable.h',self.f.view.source_entries);self.assertIn('notes/decisions/OTHER.md',self.f.view.source_entries)
 def test_negative_schema_identity_authority(self):
  original=copy.deepcopy(self.f.auth)
  changes=[lambda p:p.update(schema_version=True),lambda p:p.update(authority='worker'),lambda p:p.update(status='PREPARED'),lambda p:p.update(execution_release='OTHER'),lambda p:p.update(recipe='other'),lambda p:p.update(candidate_id='../x'),lambda p:p.update(extra='x'),lambda p:p.update(source_revision='2'*40),lambda p:p['bindings'].update(system_sdk='/tmp/latest'),lambda p:p['observation']['tools']['cc'].update(path='/bin/sh'),lambda p:p['observation']['flags']['release'].append('-DFAKE'),lambda p:p['observation']['units']['c'].pop(),lambda p:p['observation']['inputs'].pop(stage.CLT+'/usr/bin/ld')]
  for i,change in enumerate(changes):
   with self.subTest(case=i):
    self.f.auth=copy.deepcopy(original);change(self.f.auth);self.f.write()
    with self.assertRaises((stage.Refused,KeyError)):self.gate()
    self.assertFalse(self.f.output().exists())
 def test_duplicate_json_and_digest(self):
  with self.assertRaises(stage.Refused):stage.loads('{"a":1,"a":2}')
  with self.assertRaises(stage.Refused):stage.authorize(self.f.pin.read_bytes(),'0'*64,self.f.ident,self.f.view)
 def test_changed_header_no_historical_exception(self):
  self.f.put('source/src/sound.h',b'FIXTURE_ONLY changed guarded header')
  with self.assertRaises(stage.Refused):self.gate()
 def test_opaque_history_link_preserved_not_consumed(self):
  self.gate();record=self.f.auth['observation']['preservation'];name=self.f.root+'/web/server/deps-signed/opaque';self.assertEqual(record['links'][name]['target'],'/FIXTURE_ONLY/nonexistent/outside');self.assertNotIn(name,record['files']);self.assertNotIn(name,self.f.auth['observation']['inputs'])
  Path(name).unlink();Path(name).symlink_to('/changed')
  with self.assertRaises(stage.Refused):self.gate()
 def test_framework_escape_and_missing_member(self):
  self.f.auth['observation']['source_framework']['Headers']['target']='../../outside';self.f.write()
  with self.assertRaises(stage.Refused):self.gate()
 def test_atomic_reservation_no_overwrite_or_alias(self):
  self.gate();base=stage.reserve(self.f.root,self.f.ident);(base/'keep').write_text('FIXTURE_ONLY')
  with self.assertRaises(FileExistsError):stage.reserve(self.f.root,self.f.ident)
  self.assertEqual((base/'keep').read_text(),'FIXTURE_ONLY')
  with self.assertRaises(stage.Refused):stage.reserve(self.f.root,'../escape')
 def test_fixture32_objects_independent_verifier_receipt(self):
  r=self.pipeline();self.assertEqual(r['status'],'NATIVE_LINKED_NOT_RUN');self.assertEqual(sum(x['kind']=='compile' for x in r['steps']),32);self.assertEqual(sum(x['kind']=='link' for x in r['steps']),2)
  receipt=self.f.output()/'verification/receipt.json';v=verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest,receipt);self.assertEqual(v['status'],'VERIFIED_BUILD_ONLY_NOT_RUN');self.assertTrue(all(x is False for x in v['claims'].values()))
  with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest,receipt)
 def test_undeclared_consumed_header_rejected(self):
  # Historical unconsumed header is valid preserved provenance; consuming it is not.
  self.gate();FakeRunner.include_undeclared=True;r=self.pipeline();self.assertEqual(r['status'],'FAILED');self.assertFalse(any(x['kind']=='compile' for x in r['steps']));self.assertTrue(self.f.output().exists())
 def test_failed_command_and_timeout_retained(self):
  FakeRunner.failure='timeout';r=self.pipeline();self.assertEqual(r['status'],'FAILED');self.assertTrue(any(s['timed_out'] for s in r['steps']));self.assertTrue((self.f.output()/'freeze.json').exists())
  with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_corrupt_object_log_and_terminal_membership(self):
  r=self.pipeline();self.assertEqual(r['status'],'NATIVE_LINKED_NOT_RUN');obj=Path(r['modes']['release']['units'][0]['object']);obj.write_bytes(b'FIXTURE_ONLY corrupt')
  with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_malformed_macho_and_rpaths(self):
  for data in (b'bad',fake_macho(1),fake_macho(2)[:-1]):
   with self.assertRaises(stage.Refused):stage.macho(data,2)
  with self.assertRaises(stage.Refused):stage.rpaths('cmd LC_RPATH\n cmdsize32\n path /old (offset12)\n',['/one','/two'])
 def test_source_only_syntax_and_no_old_helper_execution(self):
  for name in ('stage.py','build.py','verify.py','test_preparation.py'):ast.parse((Path(__file__).parent/name).read_text())
  text=(Path(__file__).parent/'build.py').read_text();self.assertNotIn('xcrun',text);self.assertNotIn('shell=True',text);self.assertNotIn('build_signed',text)
 def reseal(self):
  base=self.f.output();p=base/'freeze.json';doc=stage.loads(p.read_bytes());items=stage.inventory(base,False);items.pop('freeze.json',None);items.pop('verification/receipt.json',None);doc['files']=items;p.write_text(stage.canonical_json(doc))
 def test_sdk_missing_or_changed_and_authoring_closure(self):
  original=copy.deepcopy(self.f.auth)
  changes=[lambda p:p['observation']['system_sdk']['files'].update({'usr/include/zlib.h':'0'*64}),lambda p:p['observation']['inputs'].pop(stage.PYTHON+'/bin/python3'),lambda p:p['observation']['system_sdk'].update(root='/elsewhere'),lambda p:p['observation']['preservation']['directories'].append('/unsorted-extra')]
  for change in changes:
   self.f.auth=copy.deepcopy(original);change(self.f.auth);self.f.write()
   with self.assertRaises(stage.Refused):self.gate()
 def test_source_manifest_entry_hash_mode_and_missing(self):
  path=Path(self.f.root)/'web/repro/source-manifest.json';original=path.read_bytes();auth_original=copy.deepcopy(self.f.auth)
  for field,value in [('mode',True),('sha256','0'*64),('path','../escape')]:
   doc=stage.loads(original);doc['entries'][0][field]=value;path.write_text(stage.canonical_json(doc));self.f.auth=copy.deepcopy(auth_original);h=stage.sha(path.read_bytes());self.f.auth['source_manifest']['sha256']=h;self.f.auth['observation']['inputs'][str(path)]=h;self.f.auth['observation']['preservation']['files'][str(path)]=h;self.f.write()
   with self.assertRaises(stage.Refused):self.gate()
  path.write_bytes(original);self.f.auth=auth_original;self.f.write()
  alias=Path(self.f.root)/'source/src/alias.h';alias.symlink_to('sound.h');self.f.view.declared_inputs=self.f.auth['observation']['inputs'];self.f.view.source_entries={e['path'] for e in stage.loads(original)['entries']}
  with self.assertRaises(stage.Refused):stage.dependency_paths('/fixture.o: '+str(alias),'/fixture.o',self.f.view,self.f.ident)
 def test_preserved_absent_root_and_link_membership(self):
  self.assertIn(self.f.root+'/config',self.f.auth['observation']['preservation']['absent_roots']);self.f.put('config/unexpected.cfg')
  with self.assertRaises(stage.Refused):self.gate()
 def test_output_symlink_parent_rejected(self):
  parent=Path(self.f.root)/'web/server/candidate-attempts';parent.symlink_to(Path(self.f.root)/'EXTERNAL',target_is_directory=True)
  with self.assertRaises(OSError):stage.reserve(self.f.root,self.f.ident)
  self.assertFalse((Path(self.f.root)/'EXTERNAL'/self.f.ident).exists())
 def test_failed_exit_overflow_and_signature_records_preserved(self):
  FakeRunner.failure='overflow';r=self.pipeline();self.assertEqual(r['status'],'FAILED');self.assertTrue(any(s['overflow'] for s in r['steps']));self.assertTrue((self.f.output()/'report.json').exists())
 def test_resealed_bad_command_runtime_claim_and_extra_step(self):
  r=self.pipeline();path=self.f.output()/'report.json';original=copy.deepcopy(r)
  for change in [lambda x:x.update(object_reuse=True),lambda x:x['claims'].update(native_runtime=True),lambda x:x['steps'][0]['argv'].append('--unknown'),lambda x:x['steps'].append(copy.deepcopy(x['steps'][-1]))]:
   changed=copy.deepcopy(original);change(changed);path.write_text(stage.canonical_json(changed));self.reseal()
   with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_log_and_extra_terminal_member_rejected(self):
  self.pipeline();base=self.f.output();log=base/'logs/000.stdout';original=log.read_bytes();log.write_text('FIXTURE_ONLY corrupt log');self.reseal()
  with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
  log.write_bytes(original);self.reseal();(base/'tmp/extra-unlisted').write_text('FIXTURE_ONLY')
  with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_live_readonly_signature_check_independent(self):
  self.pipeline();FakeRunner.wrong_signature=True
  with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_live_readonly_dylib_check_independent(self):
  self.pipeline();FakeRunner.wrong_dylib=True
  with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_combined_command_log_bound(self):
  r=self.pipeline();row=r['steps'][0];data=b'X'*160;(self.f.output()/row['stderr_path']).write_bytes(data);row['stderr_sha256']=stage.sha(data);(self.f.output()/'report.json').write_text(stage.canonical_json(r));self.reseal()
  with patch.object(stage,'MAX_LOG',160):
   with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_retained_fat2_actual_format_and_thin(self):
  for name,count in [('SDL2',42),('hidapi',8)]:
   path='/FIXTURE_ONLY/'+name;names=stage.otool_dependencies(retained_otool(path),path);self.assertEqual(len(names),count);self.assertIn('/usr/lib/libSystem.B.dylib',names)
  path='/FIXTURE_ONLY/ac_server';self.assertEqual(stage.otool_dependencies(path+':\n\t/usr/lib/libSystem.B.dylib (compatibility version 1.0.0, current version 1.0.0)\n',path),['/usr/lib/libSystem.B.dylib'])
 def test_retained_fat2_build_and_independent_verifier(self):
  FakeRunner.retained_fat=True;r=self.pipeline();self.assertEqual(r['status'],'NATIVE_LINKED_NOT_RUN');self.assertEqual(verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)['status'],'VERIFIED_BUILD_ONLY_NOT_RUN')
  path=r['framework_checks'][0]['path'];step=r['steps'][r['framework_checks'][0]['steps']['dependencies']];self.assertEqual((self.f.output()/step['stdout_path']).read_text(),retained_otool(path))
 def test_malformed_unknown_or_forged_otool_sections(self):
  path='/FIXTURE_ONLY/SDL2';valid=retained_otool(path);lines=valid.splitlines(keepends=True);arm=next(i for i,s in enumerate(lines) if '(architecture arm64):' in s)
  bad=[valid.replace(path+' (architecture arm64):','/forged (architecture arm64):'),valid.replace('architecture arm64','architecture unknown'),valid.replace('architecture arm64','architecture x86_64'),''.join(lines[1:]),valid+'unexpected diagnostic\n',valid.replace('\t/usr/lib/libSystem.B.dylib','/usr/lib/libSystem.B.dylib'),''.join([lines[0],*lines[arm:]]),''.join(lines[arm:]),valid.replace('compatibility version 1.0.0','compatibility version bogus'),path+':\n'+valid]
  for text in bad:
   with self.subTest(text=text[:70]):
    with self.assertRaises(stage.Refused):stage.otool_dependencies(text,path)
 def test_foreign_dylib_in_fat_section_rejected_by_producer(self):
  original=retained_otool
  with patch(__name__+'.retained_otool',side_effect=lambda path:original(path).replace('/usr/lib/libSystem.B.dylib','/FIXTURE_ONLY/escape.dylib',1)):
   FakeRunner.retained_fat=True;r=self.pipeline();self.assertEqual(r['status'],'FAILED')
 def test_foreign_dylib_in_fat_section_rejected_live(self):
  FakeRunner.retained_fat=True;self.pipeline();original=retained_otool
  with patch(__name__+'.retained_otool',side_effect=lambda path:original(path).replace('/usr/lib/libSystem.B.dylib','/FIXTURE_ONLY/escape.dylib',1)):
   with self.assertRaises(stage.Refused):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_resealed_escaping_tmp_link_rejected(self):
  self.pipeline();(self.f.output()/'tmp/escape').symlink_to(self.f.root+'/EXTERNAL');self.reseal()
  with self.assertRaisesRegex(stage.Refused,'owned link'):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_resealed_same_content_log_link_rejected_before_read(self):
  self.pipeline();base=self.f.output();log=base/'logs/000.stdout';target=base/'tmp/same-log';log.rename(target);log.symlink_to('../tmp/same-log');self.reseal();original=Path.read_bytes
  def read(path):
   self.assertNotEqual(path,log,'verifier followed owned log link');return original(path)
  with patch.object(Path,'read_bytes',read):
   with self.assertRaisesRegex(stage.Refused,'owned link'):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_resealed_log_ancestor_link_rejected(self):
  self.pipeline();base=self.f.output();(base/'logs').rename(base/'tmp/log-storage');(base/'logs').symlink_to('tmp/log-storage',target_is_directory=True);self.reseal()
  with self.assertRaisesRegex(stage.Refused,'owned link'):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_resealed_records_dependencies_objects_binaries_links_rejected(self):
  r=self.pipeline();base=self.f.output();unit=r['modes']['release']['units'][0];paths=['report.json','freeze.json','verification/receipt.json',str(Path(unit['object']).relative_to(base)),str(Path(unit['dep']).relative_to(base)),str(Path(unit['pre_dep']).relative_to(base)),'release/ac_server']
  for name in paths:
   with self.subTest(path=name):
    path=base/name;existed=path.exists()
    if not existed:path.write_text('FIXTURE_ONLY receipt')
    target=base/'tmp/link-target';path.rename(target);path.symlink_to(target);self.reseal() if name!='freeze.json' else None
    with self.assertRaisesRegex(stage.Refused,'owned link'):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
    path.unlink();target.rename(path)
    if not existed:path.unlink()
    self.reseal()
 def test_resealed_extra_inside_framework_alias_rejected(self):
  self.pipeline();base=self.f.output();(base/'deps-signed/SDL2.framework/extra-headers').symlink_to('Versions/A/Headers');self.reseal()
  with self.assertRaisesRegex(stage.Refused,'owned framework link'):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_changed_framework_link_text_or_mode_rejected(self):
  self.pipeline();base=self.f.output();link=base/'deps-signed/SDL2.framework/Headers';link.unlink();link.symlink_to('Versions/A/Headers');self.reseal()
  with self.assertRaisesRegex(stage.Refused,'owned framework link'):verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)
 def test_producer_refuses_invalid_owned_link_before_seal(self):
  original=FakeRunner.run
  def inject(runner,kind,argv):
   result=original(runner,kind,argv)
   if '--display' in argv and argv[-1]==str(self.f.output()/'debug/ac_server'):(self.f.output()/'tmp/escape').symlink_to('/FIXTURE_ONLY/outside')
   return result
  with patch.object(FakeRunner,'run',inject):r=self.pipeline()
  self.assertEqual(r['status'],'FAILED');self.assertTrue(any('owned seal refused' in e for e in r['errors']));self.assertTrue((self.f.output()/'report.json').is_file());self.assertFalse((self.f.output()/'freeze.json').exists());self.assertTrue((self.f.output()/'tmp/escape').is_symlink())
 def test_owned_file_ancestor_guard(self):
  root=Path(self.f.root);base=root/'guard';base.mkdir();(base/'ordinary').mkdir();(base/'ordinary/file').write_text('FIXTURE_ONLY');(base/'alias').symlink_to('ordinary',target_is_directory=True)
  with self.assertRaises(stage.Refused):stage.owned_path(base,base/'alias/file')
  with self.assertRaises(stage.Refused):stage.owned_path(base,base/'alias/new',absent=True)
  self.assertEqual(stage.owned_path(base,base/'ordinary/file'),base/'ordinary/file')
 def pthread_ready(self):
  self.gate();self.f.view.declared_inputs=self.f.auth['observation']['inputs'];return stage.SDK_PTHREAD_ALIAS
 def pthread_dep(self,name):return stage.dependency_paths('/FIXTURE_ONLY.o: '+name+'\n','/FIXTURE_ONLY.o',self.f.view,self.f.ident)
 def test_sdk_pthread_fixed_alias_pin_and_retained_raw_format(self):
  alias,raw,mode,target=self.pthread_ready();self.assertFalse(self.f.view.ordinary(alias));self.assertTrue(self.f.view.ordinary(target));self.assertEqual(self.f.view.link_identity(alias),{'target':raw,'mode':mode});self.assertNotIn(alias,self.f.auth['observation']['inputs']);self.assertIn(target,self.f.auth['observation']['inputs']);self.assertIn('usr/include/pthread/pthread.h',self.f.auth['observation']['system_sdk']['files'])
  retained=stage.loads((Path(__file__).parent/'preparation-T104-20261108-1/retained-pthread-dependencies.json').read_bytes())
  for record in retained['records']:
   line=record['matching_lines'][0]['raw'].replace('/Library/Developer/CommandLineTools/SDKs/MacOSX.sdk',stage.SDK);text='/FIXTURE_ONLY.o: \\\n'+line+'\n  '+stage.SDK+'/usr/include/zlib.h\n';result=stage.dependency_paths(text,'/FIXTURE_ONLY.o',self.f.view,self.f.ident);self.assertIn(target,result);self.assertNotIn(alias,result);self.assertIn(alias,text)
 def test_sdk_pthread_full_pipeline_keeps_raw_dependency(self):
  r=self.pipeline();self.assertEqual(r['status'],'NATIVE_LINKED_NOT_RUN');alias,_,_,target=stage.SDK_PTHREAD_ALIAS
  for mode in r['modes'].values():
   for unit in mode['units']:
    self.assertIn(target,unit['dependencies']);self.assertNotIn(alias,unit['dependencies']);self.assertIn(alias,Path(unit['pre_dep']).read_text());self.assertIn(alias,Path(unit['dep']).read_text())
  self.assertEqual(verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)['status'],'VERIFIED_BUILD_ONLY_NOT_RUN')
 def test_sdk_pthread_alias_identity_before_any_effects(self):
  alias,raw,mode,target=stage.SDK_PTHREAD_ALIAS
  for identity in [None,{'target':'./'+raw,'mode':mode},{'target':raw,'mode':0o777}]:
   with self.subTest(identity=identity),patch.object(self.f.view,'link_identity',return_value=identity),patch.object(FakeRunner,'run',side_effect=AssertionError('EFFECT BEFORE ALIAS GATE')):
    with self.assertRaises(stage.Refused):self.pipeline()
    self.assertFalse(self.f.output().exists())
 def test_sdk_pthread_undeclared_target_before_any_effects(self):
  original=copy.deepcopy(self.f.auth);target=stage.SDK_PTHREAD_ALIAS[3]
  for field in ('inputs','system_sdk'):
   self.f.auth=copy.deepcopy(original)
   if field=='inputs':self.f.auth['observation']['inputs'].pop(target)
   else:self.f.auth['observation']['system_sdk']['files'].pop('usr/include/pthread/pthread.h')
   self.f.write()
   with patch.object(FakeRunner,'run',side_effect=AssertionError('EFFECT BEFORE TARGET PIN')):
    with self.assertRaises(stage.Refused):self.pipeline()
   self.assertFalse(self.f.output().exists())
 def test_sdk_pthread_target_bytes_changed_when_consumed(self):
  alias,_,_,target=self.pthread_ready();self.f.view.mapped(target).write_text('FIXTURE_ONLY changed pthread bytes')
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
 def test_sdk_pthread_nested_target_rejected(self):
  alias,_,_,target=self.pthread_ready();p=self.f.view.mapped(target);other=p.with_name('same-bytes.h');p.rename(other);p.symlink_to('same-bytes.h')
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  with self.assertRaises(stage.Refused):self.gate()
 def test_sdk_pthread_linked_ancestor_rejected(self):
  alias,_,_,target=self.pthread_ready();parent=self.f.view.mapped(target).parent;other=parent.with_name('same-directory');parent.rename(other);parent.symlink_to('same-directory',target_is_directory=True)
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  with self.assertRaises(stage.Refused):self.gate()
 def test_sdk_pthread_unknown_same_content_alias_rejected(self):
  alias,_,_,target=self.pthread_ready();unknown=stage.SDK+'/usr/include/also-pthread.h';self.f.view.mapped(unknown).symlink_to('pthread/pthread.h')
  self.assertEqual(self.f.view.hash(unknown),self.f.view.hash(target))
  with self.assertRaises(stage.Refused):self.pthread_dep(unknown)
 def test_sdk_pthread_changed_raw_escape_and_dangling_rejected(self):
  alias,raw,mode,target=self.pthread_ready();p=self.f.view.mapped(alias)
  for text in ['./'+raw,'pthread/../pthread/pthread.h','../outside.h','/FIXTURE_ONLY/outside.h','pthread/missing.h']:
   p.unlink();p.symlink_to(text);os.lchmod(p,mode)
   with self.subTest(raw=text):
    with self.assertRaises(stage.Refused):self.pthread_dep(alias)
    with self.assertRaises(stage.Refused):self.gate()
 def test_sdk_pthread_ordinary_or_missing_alias_rejected(self):
  alias,_,_,target=self.pthread_ready();p=self.f.view.mapped(alias);p.unlink();p.write_bytes(self.f.view.mapped(target).read_bytes())
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  with self.assertRaises(stage.Refused):self.gate()
  p.unlink()
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  with self.assertRaises(stage.Refused):self.gate()
 def test_sdk_pthread_mode_changed_after_gate_rejected(self):
  alias,_,_,_=self.pthread_ready();os.lchmod(self.f.view.mapped(alias),0o700)
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  with self.assertRaises(stage.Refused):self.gate()
 def test_sdk_pthread_missing_target_rejected(self):
  alias,_,_,target=self.pthread_ready();self.f.view.mapped(target).unlink()
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  with self.assertRaises(stage.Refused):self.gate()
 def test_sdk_pthread_legacy_sdk_selector_still_rejected(self):
  alias,_,_,target=self.pthread_ready();old=alias.replace('MacOSX15.5.sdk','MacOSX.sdk');original=self.f.view.canonical
  with patch.object(self.f.view,'canonical',side_effect=lambda name:target if name==old else original(name)):
   with self.assertRaises(stage.Refused):self.pthread_dep(old)
 def test_sdk_pthread_fake_pipeline_reads_no_real_external_files(self):
  patches=[]
  for method in ('open','stat','lstat','resolve'):
   original=getattr(Path,method)
   def guarded(path,*args,_original=original,**kwargs):
    self.assertFalse(str(path).startswith(('/Library/Developer/CommandLineTools','/Library/Frameworks/Python.framework','/usr/bin/')),'REAL EXTERNAL FILE READ FORBIDDEN');return _original(path,*args,**kwargs)
   patches.append(patch.object(Path,method,guarded))
  for p in patches:p.start()
  try:self.assertEqual(self.pipeline()['status'],'NATIVE_LINKED_NOT_RUN');self.assertEqual(verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)['status'],'VERIFIED_BUILD_ONLY_NOT_RUN')
  finally:
   for p in reversed(patches):p.stop()
 def sched_no_effects(self):
  with patch.object(FakeRunner,'run',side_effect=AssertionError('EFFECT BEFORE SCHED GATE')):
   with self.assertRaises(stage.Refused):self.pipeline()
  self.assertFalse(self.f.output().exists())
 def test_sched_retained_failed_dependency_and_both_alias_pipeline(self):
  self.pthread_ready();p=Path(__file__).parent/'preparation-T106-20261108-1/failed-log.pre.d';raw=p.read_text();self.assertEqual(stage.sha(p.read_bytes()),'c4fd1b45db65f65e251d9b6633a1923197787c8e98d4cb097b115cfafd5786c3');lines=[line for line in raw.splitlines() if any(a in line for a,_,_,_ in stage.SDK_HEADER_ALIASES)];self.assertEqual(len(lines),2)
  text='/FIXTURE_ONLY.o: \\\n'+'\n'.join(lines)+'\n '+stage.SDK+'/usr/include/zlib.h\n';deps=stage.dependency_paths(text,'/FIXTURE_ONLY.o',self.f.view,self.f.ident)
  for alias,_,_,target in stage.SDK_HEADER_ALIASES:self.assertIn(alias,text);self.assertIn(target,deps);self.assertNotIn(alias,deps)
  r=self.pipeline();self.assertEqual(r['status'],'NATIVE_LINKED_NOT_RUN')
  for mode in r['modes'].values():
   for unit in mode['units']:
    for alias,_,_,target in stage.SDK_HEADER_ALIASES:self.assertIn(alias,Path(unit['dep']).read_text());self.assertIn(target,unit['dependencies']);self.assertNotIn(alias,unit['dependencies'])
  self.assertEqual(verify.verify(self.f.root,self.f.ident,self.f.pin,self.f.digest)['status'],'VERIFIED_BUILD_ONLY_NOT_RUN')
 def test_sched_raw_identity_type_text_mode_before_effects(self):
  alias,raw,mode,_=stage.SDK_SCHED_ALIAS;original=self.f.view.link_identity
  for identity in [None,{'target':'./'+raw,'mode':mode},{'target':'pthread/pthread.h','mode':mode},{'target':raw,'mode':0o777}]:
   with self.subTest(identity=identity),patch.object(self.f.view,'link_identity',side_effect=lambda name:identity if name==alias else original(name)):self.sched_no_effects()
 def test_sched_missing_undeclared_changed_target_before_effects(self):
  original=copy.deepcopy(self.f.auth);target=stage.SDK_SCHED_ALIAS[3]
  for change in [lambda p:p['observation']['inputs'].pop(target),lambda p:p['observation']['system_sdk']['files'].pop('usr/include/pthread/sched.h'),lambda p:p['observation']['inputs'].update({target:'0'*64})]:
   self.f.auth=copy.deepcopy(original);change(self.f.auth);self.f.write();self.sched_no_effects()
 def test_sched_physical_wrong_raw_escape_dangling_before_effects(self):
  alias,raw,mode,_=stage.SDK_SCHED_ALIAS;p=self.f.view.mapped(alias)
  for text in ['./'+raw,'pthread/pthread.h','../outside.h','/FIXTURE_ONLY/escape.h','pthread/missing.h']:
   p.unlink();p.symlink_to(text);os.lchmod(p,mode);self.sched_no_effects()
 def test_sched_missing_or_ordinary_alias_before_effects(self):
  alias,_,_,target=stage.SDK_SCHED_ALIAS;p=self.f.view.mapped(alias);p.unlink();p.write_bytes(self.f.view.mapped(target).read_bytes());self.sched_no_effects();p.unlink();self.sched_no_effects()
 def test_sched_nested_target_before_effects(self):
  target=self.f.view.mapped(stage.SDK_SCHED_ALIAS[3]);other=target.with_name('same-bytes.h');target.rename(other);target.symlink_to('same-bytes.h');self.sched_no_effects()
 def test_sched_linked_ancestor_before_effects(self):
  parent=self.f.view.mapped(stage.SDK_SCHED_ALIAS[3]).parent;other=parent.with_name('same-directory');parent.rename(other);parent.symlink_to('same-directory',target_is_directory=True);self.sched_no_effects()
 def test_sched_missing_or_changed_ordinary_target_before_effects(self):
  target=self.f.view.mapped(stage.SDK_SCHED_ALIAS[3]);target.write_text('FIXTURE_ONLY changed sched bytes');self.sched_no_effects();target.unlink();self.sched_no_effects()
 def test_sched_consumed_rechecks_mode_target_hash_and_declarations(self):
  self.pthread_ready();alias,_,mode,target=stage.SDK_SCHED_ALIAS;p=self.f.view.mapped(alias);os.lchmod(p,0o700)
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  os.lchmod(p,mode);ordinary=self.f.view.mapped(target);old=ordinary.read_bytes();ordinary.write_text('FIXTURE_ONLY late target change')
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  ordinary.write_bytes(old);saved=self.f.view.declared_inputs.pop(target)
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
  self.f.view.declared_inputs[target]=saved;self.f.view.sdk_files.pop('usr/include/pthread/sched.h')
  with self.assertRaises(stage.Refused):self.pthread_dep(alias)
 def test_sched_unknown_same_byte_alias_and_unknown_helper_selector_refused(self):
  self.pthread_ready();unknown=stage.SDK+'/usr/include/same-sched.h';self.f.view.mapped(unknown).symlink_to('pthread/sched.h');self.assertEqual(self.f.view.hash(unknown),self.f.view.hash(stage.SDK_SCHED_ALIAS[3]))
  with self.assertRaises(stage.Refused):self.pthread_dep(unknown)
  with patch.object(self.f.view,'ordinary_ancestors',side_effect=AssertionError('UNKNOWN SELECTOR TOUCHED FILESYSTEM')):
   with self.assertRaises(stage.Refused):stage.sdk_header_alias(self.f.view,self.f.view.declared_inputs,self.f.view.sdk_files,unknown)
 def test_capture_wrapper_effect_double_success_and_timeout(self):
  # Exercise real capture/control logic with fake process/fd/selector/signals only.
  import types
  for timed in (False,True):
   base=Path(self.f.root)/('capture-timeout' if timed else 'capture-ok');(base/'logs').mkdir(parents=True);(base/'tmp').mkdir();state={'alive':True,'code':None,'reads':{1:0,2:0},'signals':[],'clock':0}
   class Stream:
    def __init__(self,fd):self.fd=fd
    def close(self):pass
   class Child:
    pid=987654321
    stdout=Stream(1);stderr=Stream(2)
    @property
    def returncode(self):return state['code']
    def poll(self):return state['code']
    def wait(self,timeout):state['code']=-15 if timed else 0;state['alive']=False;return state['code']
   class Selector:
    def __init__(self):self.keys={}
    def __enter__(self):return self
    def __exit__(self,*a):pass
    def register(self,s,events,data):self.keys[s]=types.SimpleNamespace(fd=s.fd,fileobj=s,data=data)
    def unregister(self,s):self.keys.pop(s)
    def get_map(self):return self.keys
    def select(self,timeout):return [] if timed else [(k,1) for k in self.keys.values()]
   def read(fd,n):state['reads'][fd]+=1;return b'FIXTURE_ONLY' if state['reads'][fd]==1 else b''
   def kill(pid,signal):
    self.assertEqual(pid,Child.pid)
    if not state['alive']:raise ProcessLookupError()
    if signal:state['signals'].append(signal);state['alive']=False
   def clock():state['clock']+=60 if timed else .001;return state['clock']
   with patch('subprocess.Popen',return_value=Child()),patch('selectors.DefaultSelector',Selector),patch('os.read',side_effect=read),patch('os.killpg',side_effect=kill),patch.object(build.time,'monotonic',side_effect=clock):
    runner=CAPTURE_RUNNER(self.f.root,base)
    if timed:
     with self.assertRaises(stage.Refused):runner.run('FIXTURE_ONLY_CAPTURE',[stage.TOOLS['cc'],'--version'])
     self.assertTrue(runner.records[0]['timed_out']);self.assertTrue(state['signals'])
    else:self.assertEqual(runner.run('FIXTURE_ONLY_CAPTURE',[stage.TOOLS['cc'],'--version'])[1],'FIXTURE_ONLY')
    self.assertTrue(runner.records[0]['group_reaped'])

if __name__=='__main__':unittest.main(verbosity=2)
