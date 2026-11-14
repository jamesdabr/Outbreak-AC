#!/usr/bin/env python3
"""T057 clean, pinned, bounded component supervisor; no game/native/browser child."""
import argparse,hashlib,json,os,pathlib,selectors,signal,socket,subprocess,tempfile,time
ROOT=pathlib.Path(__file__).resolve().parents[3]
NODE=pathlib.Path('/private/tmp/outbreak-web-sdk/node/24.19.0_64bit/bin/node')
NODE_SHA='27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1'
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser();p.add_argument('--attempt',required=True);p.add_argument('--rationale',required=True);args=p.parse_args()
 if not args.attempt.startswith('attempt-') or not args.attempt[8:].isdigit():raise ValueError('attempt_name')
 destination=ROOT/'web/transport/results/gateway-T057'/args.attempt
 destination.mkdir(parents=True,exist_ok=False)
 report={'kind':'T057 COMPONENT WITH SYNTHETIC UDP, NOT GAME','rationale':args.rationale,'status':'NOT RUN','preflight':{},'cleanup':{}}
 assert sha(NODE)==NODE_SHA
 manifest=json.loads((ROOT/'web/transport/results/T050-vendor.json').read_text())
 vendor=ROOT/'web/transport/vendor/ws-8.21.0'
 assert {x.relative_to(vendor).as_posix():sha(x) for x in vendor.rglob('*') if x.is_file()}==manifest['files']
 report['preflight']['node']={'path':str(NODE),'sha256':NODE_SHA}
 report['preflight']['vendor_files']=manifest['files']
 report['preflight']['source_hashes']={str(x.relative_to(ROOT)):sha(x) for x in [ROOT/'web/transport/gateway.cjs',ROOT/'web/transport/gateway-limits.cjs',pathlib.Path(__file__),*sorted((ROOT/'web/transport/tests').glob('gateway-*.cjs'))]}
 for relative,pinned in report['preflight']['source_hashes'].items():
  snapshot=destination/'source'/relative;snapshot.parent.mkdir(parents=True,exist_ok=True)
  snapshot.write_bytes((ROOT/relative).read_bytes());assert sha(snapshot)==pinned
 output_root=ROOT/'web/build/out'
 frozen={x.relative_to(output_root).as_posix():sha(x) for x in output_root.rglob('*') if x.is_file()}
 probes=[]
 try:
  for kind,port in [(socket.SOCK_STREAM,29865),(socket.SOCK_DGRAM,29863)]:
   probe=socket.socket(socket.AF_INET,kind);probes.append(probe)
   if kind==socket.SOCK_STREAM:probe.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
   probe.bind(('127.0.0.1',port))
 except OSError as error:
  report['preflight']['port_error']={'errno':error.errno,'port':port}
  listing=subprocess.run(['/usr/sbin/lsof','-nP','-i',f':{port}'],capture_output=True,text=True,timeout=1)
  report['preflight']['owner_listing']=listing.stdout[:8192]
  (destination/'result.json').write_text(json.dumps(report,indent=2)+'\n');return 2
 finally:
  for probe in probes:probe.close()
 report['preflight']['fixed_ports_available']=True
 started=time.monotonic()
 with tempfile.TemporaryDirectory(prefix='outbreak-t057-',dir='/private/tmp') as cwd:
  env={'PATH':'/usr/bin:/bin','WS_NO_BUFFER_UTIL':'1','WS_NO_UTF_8_VALIDATE':'1','TMPDIR':cwd}
  command=[str(NODE),str(ROOT/'web/transport/tests/gateway-component.cjs')]
  report.update(command=command,cwd=cwd,environment=env)
  child=subprocess.Popen(command,cwd=cwd,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE,start_new_session=True)
  selector=selectors.DefaultSelector();selector.register(child.stdout,selectors.EVENT_READ,'stdout');selector.register(child.stderr,selectors.EVENT_READ,'stderr')
  buffers={'stdout':bytearray(),'stderr':bytearray()};violation=None
  while selector.get_map():
   if time.monotonic()-started>=20:violation='20_second_child_deadline';break
   for key,_ in selector.select(.05):
    data=os.read(key.fileobj.fileno(),65536)
    if not data:selector.unregister(key.fileobj);continue
    if sum(map(len,buffers.values()))+len(data)>8388608:violation='8MiB_output_limit';break
    buffers[key.data].extend(data)
   if violation:break
  if violation:os.killpg(child.pid,signal.SIGKILL)
  child.wait(timeout=2)
  selector.close();child.stdout.close();child.stderr.close()
  report.update(elapsed_seconds=time.monotonic()-started,exit_code=child.returncode,child_reaped=True,violation=violation,combined_output_bytes=sum(map(len,buffers.values())))
  for name,data in buffers.items():(destination/f'{name}.txt').write_bytes(data)
  try:report['child_result']=json.loads(buffers['stdout'])
  except (ValueError,UnicodeDecodeError):report['child_result']={'status':'FAIL','reason':'missing_valid_json'}
 for port,kind in [(29865,socket.SOCK_STREAM),(29863,socket.SOCK_DGRAM)]:
  entry={};probe=socket.socket(socket.AF_INET,kind)
  try:
   if kind==socket.SOCK_STREAM:probe.setsockopt(socket.SOL_SOCKET,socket.SO_REUSEADDR,1)
   probe.bind(('127.0.0.1',port));entry['bind_close']='PASS'
  except OSError as error:entry.update(bind_close='FAIL',errno=error.errno)
  finally:probe.close()
  if kind==socket.SOCK_STREAM:
   q=subprocess.run(['/usr/sbin/lsof','-nP','-a',f'-iTCP:{port}','-sTCP:LISTEN'],capture_output=True,text=True,timeout=1)
   entry.update(no_listener=q.returncode==1 and not q.stdout and not q.stderr,lsof_exit=q.returncode,lsof_stdout=q.stdout[:8192],lsof_stderr=q.stderr[:8192])
  report['cleanup'][str(port)]=entry
 report['frozen_runtime_unchanged']=frozen=={x.relative_to(output_root).as_posix():sha(x) for x in output_root.rglob('*') if x.is_file()}
 report['status']='PASS' if report['exit_code']==0 and not violation and report['child_result']['status']=='PASS' and all(v['bind_close']=='PASS' for v in report['cleanup'].values()) and report['cleanup']['29865']['no_listener'] and report['frozen_runtime_unchanged'] else 'FAIL'
 (destination/'result.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps({'status':report['status'],'result':str(destination/'result.json'),'elapsed_seconds':report['elapsed_seconds']}))
 return 0 if report['status']=='PASS' else 1
if __name__=='__main__':raise SystemExit(main())
