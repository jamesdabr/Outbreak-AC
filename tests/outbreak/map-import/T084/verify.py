"""Inspected local T084 compiler/runtime gate. No project helper imports/services."""
import hashlib
import itertools
import json
import os
from pathlib import Path
import random
import shutil
import struct
import subprocess
import sys
import zlib
sys.dont_write_bytecode=True
HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[3]
SDK=Path('/private/tmp/outbreak-web-sdk')
MAX=1048576
SOURCES=[ROOT/'source/outbreak/map_import.h',ROOT/'source/outbreak/map_import.cpp',
         HERE/'wrapper.cpp',HERE/'wasm_runner.mjs',Path(__file__).resolve(),
         ROOT/'MVP/PORTABLE_FORMAT_FOUNDATION.md',ROOT/'tickets/T084.md',
         ROOT/'web/world/reviews/T076/measurements-2.json',ROOT/'web/assets/original/generate_pack.py']
MAPS=[('web/assets/network-profile/pack-root/packages/maps/dev_outbreak_browser.cgz',
       '856173969726f632812fd8ebd2ada746831d7e81f7452dd98f7235a2bd398134'),
      ('web/assets/blackwood-candidate/pack-root/packages/maps/blackwood_greybox_v1.cgz',
       'e68314e911130d2822fdfa65d77dfaba302d4f5c3552ff91c698b84768d5ddf1')]


def digest(data):return hashlib.sha256(data).hexdigest()
def snapshot(roots):
    values={}
    for root in roots:
        if not root.exists():raise RuntimeError('Missing input '+str(root))
        for p in ([root] if root.is_file() else sorted(root.rglob('*'))):
            if p.is_symlink():values[str(p)]='symlink:'+os.readlink(p)
            elif p.is_file():values[str(p)]=digest(p.read_bytes())
    return values
def write(path,value):path.write_text(json.dumps(value,indent=2,sort_keys=True)+'\n')


class Invalid(Exception):pass
def need(condition,error):
    if not condition:raise Invalid(error)


def oracle(raw,declared,capacity,nulls):
    """Independent struct/integer parser, producing actual complete cell fields."""
    try:
        need(not nulls,1);need(980<=declared<=MAX,2)
        data=raw[:declared]
        need(data[:4]==b'ACMP',3)
        version,header,factor,count=struct.unpack_from('<iiii',data,4)
        need(version==10,4);need(980<=header<=5076 and header<=declared,5)
        need(6<=factor<=8,6);need(0<=count<=1024,7)
        start=header+count*16;need(start<declared,7)
        revision=struct.unpack_from('<i',data,924)[0];need(1<=revision<=2147483647,11)
        need(struct.unpack_from('<i',data,916)[0]==-10000 and struct.unpack_from('<i',data,932)[0]==0,9)
        side=2**factor;need(capacity>=side**2,10)
        ext=data[980:header];records=0
        while ext:
            records+=1;need(records<=16 and len(ext)>=2,8)
            n,flag=ext[:2];need(1<=n<=127 and n<=len(ext)-2,8);need(flag==65,9)
            payload=ext[2:2+n];need(payload.count(0)>=2 and payload[-1]==0,8);ext=ext[2+n:]
        for fields in struct.iter_unpack('<hhhhBBBBhbB',data[header:start]):
            x,y,z,a1,kind,a2,a3,a4,a5,a6,a7=fields
            need(0<=x<side and 0<=y<side and -128<=z<=127,7)
            need(kind in (1,2),9);need(a5==a6==a7==0,7)
            need((1<=a1<=255) if kind==1 else (0<=a1<=3599 and a2 in (0,1,100) and a3==a4==0),7)
        stream=memoryview(data)[start:];at=0;cells=[]
        while len(cells)<side**2:
            need(at<len(stream),13);kind=stream[at];at+=1
            if kind==255:
                need(at<len(stream) and len(cells)>0,14);repeat=stream[at];at+=1
                need(1<=repeat<=side**2-len(cells),14);cells.extend([cells[-1]]*repeat)
            elif kind==0:
                need(at+2<=len(stream),13);need(stream[at+1]==0,9);at+=2;cells.append((0,0,0,0))
            elif kind==4:
                need(at+8<=len(stream),13)
                floor,ceiling=struct.unpack_from('<bb',stream,at)
                need(floor<ceiling,13);need(stream[at+5]==stream[at+7]==0,9)
                at+=8;cells.append((4,floor,ceiling,0))
            else:raise Invalid(12)
        need(at==len(stream),15)
        body=b''.join(struct.pack('<BbbB',*cell) for cell in cells)
        return struct.pack('<10I',1,0,side,revision,count,1,1,1,1,len(cells))+body
    except Invalid as error:
        return struct.pack('<10I',0,error.args[0],0xa5a5,0xa5a5a5a5,0xa5a5,1,1,1,1,0)


def encode_cells(cells):
    result=bytearray();i=0
    while i<len(cells):
        kind,floor,ceiling,tag=cells[i]
        result+=bytes((0,231,0)) if kind==0 else struct.pack('<Bbb6B',4,floor,ceiling,255,128,0,0,255,tag)
        j=i+1
        while j<len(cells) and cells[j]==cells[i]:j+=1
        remaining=j-i-1
        while remaining:
            n=min(255,remaining);result+=bytes((255,n));remaining-=n
        i=j
    return bytes(result)


def make(factor=6,cells=None,ext=b'',entities=b'',revision=1):
    header=bytearray(980)
    struct.pack_into('<4s4i',header,0,b'ACMP',10,980+len(ext),factor,len(entities)//16)
    struct.pack_into('<i',header,916,-10000);struct.pack_into('<i',header,924,revision)
    if cells is None:cells=[(4,-128,127,0)]*(4**factor)
    return bytes(header)+ext+entities+encode_cells(cells)


def owned():
    results=[]
    report_path=ROOT/'web/world/reviews/T076/measurements-2.json'
    assert digest(report_path.read_bytes())=='33b29fc02f340a62b7aa6fce6d74574f735dd1a95a51c658c0b870270c3be9e3'
    report=json.loads(report_path.read_text())['proposal']
    for index,(path,pin) in enumerate(MAPS):
        packed=(ROOT/path).read_bytes();assert digest(packed)==pin
        inflater=zlib.decompressobj(31);raw=inflater.decompress(packed,MAX+1)
        assert inflater.eof and not inflater.unused_data and not inflater.unconsumed_tail and len(raw)<=MAX
        golden=[];side=64 if index==0 else 128
        for y in range(side):
            for x in range(side):
                if index==0:
                    building=26<=x<38 and 24<=y<40
                    inner=28<=x<36 and 26<=y<38
                    doorway=30<=y<34 and (26<=x<28 or 36<=x<38)
                    blocked=not(8<=x<56 and 8<=y<56) or (building and not inner and not doorway)
                    ceiling=8 if building else 12
                else:
                    rectangles=report['geometry_rectangles']['building']+report['geometry_rectangles']['screens']
                    blocked=not(8<=x<120 and 8<=y<120) or any(a<=x<c and b<=y<d for a,b,c,d in rectangles)
                    ceiling=12 if 50<=x<78 and 50<=y<78 else 16
                golden.append((0,0,0,0) if blocked else (4,0,ceiling,0))
        actual=oracle(raw,len(raw),65536,0)
        assert struct.unpack_from('<I',actual)[0]==1
        assert actual[40:]==b''.join(struct.pack('<BbbB',*cell) for cell in golden)
        results.append(raw)
    return results


def cases():
    base=make()
    def case(label,raw=base,capacity=65536,nulls=0,declared=None):
        return (label,raw,len(raw) if declared is None else declared,capacity,nulls)
    for i,raw in enumerate(owned()):yield case('owned-independent-geometry-%d'%i,raw)
    for factor in (6,7,8):
        cells=[(0,0,0,0) if (x+y)%7==0 else (4,-128+(x%120),1+y%127,0)
               for y in range(2**factor) for x in range(2**factor)]
        yield case('synthetic-factor-%d'%factor,make(factor,cells))
        for capacity in (0,1,4**factor-1,4**factor,4**factor+1,65536,0xffffffff):
            yield case('capacity-%d-%d'%(factor,capacity),make(factor),capacity)
    for nulls in (1,2,3):
        for size in (0,980,len(base)):
            yield case('null-%d-%d'%(nulls,size),base,nulls=nulls,declared=size)
    # Every short header and every truncation of the accepted candidate raw.
    for n in range(980):yield case('short-%d'%n,base[:n])
    candidate=owned()[1]
    for n in range(980,len(candidate)):yield case('candidate-truncation-%d'%n,candidate[:n])
    for n in (MAX-1,MAX,MAX+1):yield case('raw-size-%d'%n,base+b'\0'*(n-len(base)))
    edits=[(0,b'BAD!')]
    for offset,values in [(4,[-1,0,9,11,2147483647]),(8,[-1,0,979,980,981,5076,5077,2147483647]),
                         (12,[-1,0,5,6,7,8,9,31]),(16,[-1,0,1,1024,1025,2147483647]),
                         (916,[-10001,-9999,0]),(924,[-2147483648,-1,0,1,2147483647]),(932,[-1,1,2147483647])]:
        edits.extend((offset,struct.pack('<i',n)) for n in values)
    for n,(offset,value) in enumerate(edits):yield case('header-edit-%d'%n,base[:offset]+value+base[offset+len(value):])
    for n in (0,1,2,16,17):yield case('metadata-count-%d'%n,make(ext=b'\x02\x41\0\0'*n))
    for ext in (b'\x00',b'\0A',b'\x80A'+b'\0'*128,b'\x7fA\0\0',b'\x02B\0\0',
                b'\x02Axy',b'\x02Ax\0',b'\x03A\0\0x',b'\x7fA'+b'x'*125+b'\0\0'):
        yield case('metadata-malformed-'+ext[:2].hex(),make(ext=ext))
    for entity_count in (1,1024):
        e=struct.pack('<hhhhBBBBhbB',63,0,-128,255,1,255,128,255,0,0,0)
        yield case('entity-count-%d'%entity_count,make(entities=e*entity_count))
    for z in (-129,-128,0,127,128):
        for kind in (1,2):yield case('entity-z-%d-%d'%(z,kind),make(entities=struct.pack('<hhhhBBBBhbB',0,63,z,1,kind,0,0,0,0,0,0)))
    for kind in range(256):yield case('entity-kind-%d'%kind,make(entities=struct.pack('<hhhhBBBBhbB',0,0,0,1,kind,0,0,0,0,0,0)))
    for kind in (1,2):
        e=struct.pack('<hhhhBBBBhbB',0,0,0,1,kind,0,0,0,0,0,0)
        for off,value in [(0,struct.pack('<h',-1)),(0,struct.pack('<h',64)),(2,struct.pack('<h',-1)),(2,struct.pack('<h',64)),
                          (6,struct.pack('<h',-1)),(6,struct.pack('<h',0)),(6,struct.pack('<h',255)),(6,struct.pack('<h',256)),
                          (6,struct.pack('<h',3599)),(6,struct.pack('<h',3600)),(9,b'\x01'),(9,b'\x02'),(9,b'\x64'),
                          (10,b'\x01'),(11,b'\x01'),(12,b'\x01\x00'),(14,b'\x01'),(15,b'\x01')]:
            yield case('entity-field-%d-%d-%s'%(kind,off,value.hex()),make(entities=e[:off]+value+e[off+len(value):]))
    header=base[:980]
    yield case('entity-stream-start-equals-eof',header)
    yield case('entity-stream-start-past-eof',header[:16]+struct.pack('<i',1)+header[20:])
    yield case('sixteen-max-informational-records',make(ext=(b'\x7fA'+b'x'*125+b'\0\0')*16))
    for kind in range(256):yield case('cell-kind-%d'%kind,header+bytes((kind,))+base[981:])
    for floor in range(-128,127):yield case('signed-floor-%d'%floor,make(cells=[(4,floor,floor+1,0)]*4096))
    for floor,ceiling in ((0,0),(1,0),(127,-128),(-128,-128),(127,127)):
        yield case('invalid-height-%d-%d'%(floor,ceiling),header+struct.pack('<Bbb6B',4,floor,ceiling,0,0,0,0,0,0))
    for tail in (b'',b'\xff',b'\xff\x01',b'\0',b'\0\0',b'\0\0\x01',b'\4\0',b'\4\0\x10\0\0\0\1\0\0',
                 b'\4\0\x10\0\0\0\0\0\1',b'\0\0\0\xff\0'):
        yield case('rle-truncated-first-unsupported-'+tail.hex(),header+tail)
    for repeat in (0,1,254,255):
        yield case('repeat-limit-%d'%repeat,header+b'\0\0\0'+b'\xff\xff'*16+bytes((255,repeat)))
    for n in (0,1,2,3,8):yield case('late-truncation-%d'%n,base[:-n] if n else base)
    for tail in (b'\0',b'\xff\0',b'\4\0\x10\0\0\0\0\0\0'):yield case('trailing-'+tail.hex(),base+tail)
    # Expand all but final cell, then a late unsupported type/data/repeat failure.
    prefix=header+encode_cells([(4,0,16,0)]*4095)
    for tail in (b'\x01',b'\xff\0',b'\xff\2',b'\4\x10\0\0\0\0\0\0\0',b'\0\0\1'):
        yield case('late-failure-'+tail.hex(),prefix+tail)
    rng=random.Random(84057)
    for n in range(2048):
        raw=bytearray(candidate if n%2 else base)
        for _ in range(rng.randrange(1,5)):raw[rng.randrange(len(raw))]=rng.randrange(256)
        yield case('mutated-%d'%n,bytes(raw))


def main():
    assert sys.argv[1:] in ([],['--native-wasm-only'])
    sanitizer_pending=bool(sys.argv[1:])
    number=1
    while (HERE/('attempt-%d'%number)).exists():number+=1
    attempt=HERE/('attempt-%d'%number);attempt.mkdir()
    for name in ('tmp','logs','node-cache','clang-cache'): (attempt/name).mkdir()
    env=dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin',TMPDIR=str(attempt/'tmp'),
             CLANG_MODULE_CACHE_PATH=str(attempt/'clang-cache'),NODE_COMPILE_CACHE=str(attempt/'node-cache'),
             PYTHONDONTWRITEBYTECODE='1',ASAN_OPTIONS='detect_leaks=0:halt_on_error=1',UBSAN_OPTIONS='halt_on_error=1:print_stacktrace=1')
    native=Path('/usr/bin/clang++');clang=SDK/'upstream/bin/clang++';linker=SDK/'upstream/bin/wasm-ld';node=SDK/'node/24.19.0_64bit/bin/node'
    assert digest(node.read_bytes())=='27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1'
    protected_roots=[ROOT/n for n in ('source/src','source/enet','web/assets','web/runtime','web/build/out','web/server/out',
                                      'web/build/.cache','web/build/generated/t066/attempt-T070-1/bundle','source/outbreak/fixed.h','source/outbreak/fixed.cpp')]+[SDK]
    protected=snapshot(protected_roots);write(attempt/'protected-before.json',protected)
    input_roots=SOURCES+[ROOT/p for p,_ in MAPS];inputs=snapshot(input_roots)
    cache=attempt/'cache'
    common=['-std=c++11','-O2','-Wall','-Wextra','-Werror','-fno-exceptions','-fno-rtti','-fno-builtin','-Wframe-larger-than=4096','-fstack-usage','-I',str(ROOT/'source/outbreak')]
    source=str(ROOT/'source/outbreak/map_import.cpp');wrapper=str(HERE/'wrapper.cpp')
    commands=[]
    for name,extra in [('native',[]),('sanitized',['-fsanitize=address,undefined','-fno-sanitize-recover=all','-g'])]:
        for part,file in [('map',source),('wrapper',wrapper)]:
            commands.append([str(native)]+common+extra+['-DT084_NATIVE','-c',file,'-o',str(attempt/(name+'-'+part+'.o'))])
        commands.append([str(native)]+extra+[str(attempt/(name+'-map.o')),str(attempt/(name+'-wrapper.o')),'-o',str(attempt/name)])
    commands.extend([
      [str(clang),'--target=wasm32-unknown-emscripten','--sysroot='+str(cache/'sysroot')]+common+['-c',source,'-o',str(attempt/'map_import.o')],
      [str(clang),'--target=wasm32-unknown-emscripten','--sysroot='+str(cache/'sysroot')]+common+['-c',wrapper,'-o',str(attempt/'wrapper.o')],
      [str(linker),'--no-entry','--export=run','--export=input_ptr','--export=output_ptr','--export=output_bytes',str(attempt/'map_import.o'),str(attempt/'wrapper.o'),'-o',str(attempt/'map.wasm')]])
    targets=['native','wasm'] if sanitizer_pending else ['native','sanitized','wasm']
    execution_map={'native':[str(attempt/'native')],'sanitized':[str(attempt/'sanitized')],
                   'wasm':[str(node),str(HERE/'wasm_runner.mjs'),str(attempt/'map.wasm')]}
    executions=[execution_map[name] for name in targets]
    write(attempt/'plan.json',dict(commands=commands,executions=executions,environment=env,inputs=inputs,
          tools=snapshot([native,clang,linker,node,Path(sys.executable).resolve()]),platform=list(os.uname()),python=sys.version,
          scope='Actual same production source; isolated direct Wasm with no imports or library fallback',batch_limit=128,
          sanitizer_status='PENDING QUESTION; compile only' if sanitizer_pending else 'actual execution requested'))
    shutil.copytree(ROOT/'web/build/.cache/sysroot',cache/'sysroot',symlinks=True)
    for i,command in enumerate(commands):
        result=subprocess.run(command,cwd=attempt,env=env,capture_output=True,timeout=60)
        (attempt/'logs'/('build-%d.stdout'%i)).write_bytes(result.stdout);(attempt/'logs'/('build-%d.stderr'%i)).write_bytes(result.stderr)
        if result.returncode:raise RuntimeError('Build failed %d; preserved logs, no fallback'%i)
    for i,tool in enumerate((native,clang,linker,node)):
        result=subprocess.run([str(tool),'--version'],cwd=attempt,env=env,capture_output=True,timeout=10,check=True)
        (attempt/'logs'/('tool-%d.version'%i)).write_bytes(result.stdout+result.stderr)
    count=0;batches=0;positives=0;errors={};iterator=iter(cases());labels=[];failures=[]
    streams={name:(attempt/(name+'.bin')).open('wb') for name in ['corpus','expected']+targets}
    try:
        while True:
            batch=list(itertools.islice(iterator,128))
            if not batch:break
            payload=b'';expected=b''
            for label,raw,declared,capacity,nulls in batch:
                record=struct.pack('<4I',len(raw),declared,capacity,nulls)+raw
                want=oracle(raw,declared,capacity,nulls);payload+=record;expected+=want
                status,error=struct.unpack_from('<2I',want);positives+=status;errors[str(error)]=errors.get(str(error),0)+1
                labels.append(dict(index=count,label=label,raw_sha256=digest(raw),declared=declared,capacity=capacity,nulls=nulls,status=status,error=error));count+=1
            streams['corpus'].write(payload);streams['expected'].write(expected)
            for name,command in zip(targets,executions):
                result=subprocess.run(command,input=payload,cwd=attempt,env=env,capture_output=True,timeout=60)
                streams[name].write(result.stdout)
                (attempt/'logs'/('%s-%d.stderr'%(name,batches))).write_bytes(result.stderr)
                if result.returncode or result.stderr or result.stdout!=expected:
                    failures.append(dict(target=name,batch=batches,returncode=result.returncode,expected_bytes=len(expected),actual_bytes=len(result.stdout)))
            batches+=1
    finally:
        for stream in streams.values():stream.close()
    write(attempt/'cases.json',labels)
    after=snapshot(protected_roots);write(attempt/'protected-after.json',after)
    changed=[p for p in sorted(set(protected)|set(after)) if protected.get(p)!=after.get(p)]
    stacks={str(p.relative_to(attempt)):p.read_text() for p in attempt.glob('*.su')}
    write(attempt/'result.json',dict(passed=not failures and not changed and inputs==snapshot(input_roots),cases=count,batches=batches,
          positive_cases=positives,negative_cases=count-positives,by_error=errors,failures=failures,protected_files=len(protected),changed_protected=changed,
          inputs_unchanged=inputs==snapshot(input_roots),stack_usage=stacks,
          hashes=snapshot([attempt/(n+'.bin') for n in ['corpus','expected']+targets]+[attempt/'native',attempt/'sanitized',attempt/'map.wasm']),
          actual_native_wasm_full_field_oracle=not failures,
          asan_ubsan='NOT RUN; pending question' if sanitizer_pending else ('PASS' if not failures else 'FAIL'),
          full_ticket_pass=not sanitizer_pending and not failures and not changed and inputs==snapshot(input_roots),
          game_native_import_navigation_render_gameplay='NOT RUN'))
    print(json.dumps(dict(cases=count,positive=positives,negative=count-positives,failures=failures,changed_protected=len(changed))))
    if failures or changed or inputs!=snapshot(input_roots):return 1
    return 0


if __name__=='__main__':sys.exit(main())
