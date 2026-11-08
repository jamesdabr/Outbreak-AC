#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. T032 original data only; never plays audio."""
import argparse
import hashlib
import io
import json
from pathlib import Path, PurePosixPath
import struct
import sys
import wave

HERE=Path(__file__).resolve().parent
RATE=22050
PREFIX='packages/audio/outbreak/'
NOTICE=(HERE/'LICENSE.txt').read_bytes()
# (duration milliseconds, segments(start ms, end ms, start Hz, end Hz, noise percent))
SPECS={
 'proof_tone':(300,[(0,300,440,440,0)]),
 'pistol':(180,[(0,180,520,80,70)]),
 'rifle':(120,[(0,120,740,110,85)]),
 'reload':(450,[(0,90,900,600,50),(200,290,650,450,50),(360,450,1050,800,40)]),
 'footstep':(200,[(0,200,95,45,65)]),
 'walker_attack':(400,[(0,400,170,65,35)]),
 'predator_front':(600,[(0,200,330,330,0),(300,600,660,660,0)]),
 'predator_flank':(750,[(0,150,660,660,0),(250,400,440,440,0),(500,750,220,220,0)]),
 'extraction':(900,[(0,230,262,262,0),(300,530,330,330,0),(600,900,524,524,0)])
}


def canonical(data):
    return json.dumps(data,indent=2,sort_keys=True)+'\n'


def samples(name):
    duration,segments=SPECS[name]
    total=duration*RATE//1000
    result=[0]*total
    seed=0x013579bd+sum((i+1)*ord(c) for i,c in enumerate(name))
    attack=RATE*5//1000
    release=RATE*25//1000
    for start_ms,end_ms,low,high,noise_percent in segments:
        start,end=start_ms*RATE//1000,end_ms*RATE//1000
        length=end-start
        phase=0
        for local in range(length):
            index=start+local
            frequency=low+(high-low)*local//max(1,length-1)
            phase=(phase+frequency)%RATE
            triangle=32767-4*abs(phase-RATE//2)*32767//RATE
            triangle=max(-32767,min(32767,triangle))
            seed=(1664525*seed+1013904223)&0xffffffff
            noise=((seed>>16)&65535)-32768
            signal=(triangle*(100-noise_percent)+noise*noise_percent)//100
            local_env=min(32767,local*32767//max(1,attack),(length-1-local)*32767//max(1,release))
            global_env=min(32767,index*32767//max(1,attack),(total-1-index)*32767//max(1,release))
            envelope=min(local_env,global_env)
            result[index]=signal*6000*envelope//(32768*32767)
    return result


def wav(name):
    values=samples(name)
    data=struct.pack('<'+'h'*len(values),*values)
    fmt=struct.pack('<HHIIHH',1,1,RATE,RATE*2,2,16)
    body=b'WAVE'+b'fmt '+struct.pack('<I',16)+fmt+b'data'+struct.pack('<I',len(data))+data
    return b'RIFF'+struct.pack('<I',len(body))+body


def declared_files():
    files={PREFIX+'LICENSE.txt':NOTICE}
    for name in sorted(SPECS):
        files[PREFIX+name+'.wav']=wav(name)
        files[PREFIX+name+'.wav.LICENSE.txt']=NOTICE
    return files


def safe(root,name):
    p=PurePosixPath(name)
    if p.is_absolute() or '..' in p.parts or str(p)!=name or not name.startswith(PREFIX) or '\\' in name:
        raise ValueError('invalid audio path: '+name)
    path=root/name
    if any(item.is_symlink() for item in (root,path,*[root/parent for parent in p.parents])):
        raise ValueError('audio symlink: '+name)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('audio path escape: '+name)
    return path


def generate(root):
    root=Path(root)
    if root.is_symlink():
        raise ValueError('audio root symlink')
    files=declared_files()
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()} if root.exists() else set()
    if actual-set(files):
        raise ValueError('undeclared files: '+','.join(sorted(actual-set(files))))
    for name in files:
        safe(root,name)
    entries=[]
    for name,data in sorted(files.items()):
        path=safe(root,name)
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        entry=dict(path=name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),license='MIT',notice=PREFIX+'LICENSE.txt',original=True)
        if name.endswith('.wav'):
            cue=Path(name).stem
            frames=SPECS[cue][0]*RATE//1000
            entry['notice']=name+'.LICENSE.txt'
            entry.update(cue=cue,integration_name='outbreak/'+cue,format='PCM16 signed little-endian',sample_rate=RATE,channels=1,sample_width=2,frames=frames,duration_seconds=frames/RATE,provenance=dict(method='original integer triangle/chirp plus seeded integer LCG noise; 5ms attack/25ms release per pulse and globally; gain 6000',duration_ms=SPECS[cue][0],segments=SPECS[cue][1],seed='0x013579bd + weighted cue-name codepoints',source='audio_pack.py'))
        entries.append(entry)
    return dict(schema_version=1,ticket='T032 revision 0.7',profile='original-audio-prerequisite',entries=entries,raw_bytes=sum(e['bytes'] for e in entries),cue_count=9,staged_only=True,playback_verified=False,engine_decode_verified=False)


def decode(raw):
    if len(raw)<44 or len(raw)>44144 or raw[:4]!=b'RIFF' or raw[8:12]!=b'WAVE':
        raise ValueError('WAV signature/size bound')
    if struct.unpack_from('<I',raw,4)[0]!=len(raw)-8:
        raise ValueError('RIFF length')
    if raw[12:16]!=b'fmt ' or struct.unpack_from('<I',raw,16)[0]!=16:
        raise ValueError('PCM fmt chunk')
    if struct.unpack_from('<HHIIHH',raw,20)!=(1,1,22050,44100,2,16):
        raise ValueError('PCM format/rate/channels/width')
    if raw[36:40]!=b'data' or struct.unpack_from('<I',raw,40)[0]!=len(raw)-44 or (len(raw)-44)%2:
        raise ValueError('PCM data length')
    values=list(struct.unpack('<'+'h'*((len(raw)-44)//2),raw[44:]))
    if not 1<len(values)<=22050 or max(map(abs,values),default=0)>8191 or not any(values):
        raise ValueError('duration/amplitude/nonzero')
    if values[0]!=0 or values[-1]!=0:
        raise ValueError('envelope endpoints')
    # Independent absolute-amplitude ceiling for the specified envelope; does not resynthesize.
    attack=110; release=551
    for index,value in enumerate(values):
        ceiling=min(8191,8191*index//attack,8191*(len(values)-1-index)//release)
        if abs(value)>ceiling+1:
            raise ValueError('attack/release envelope')
    with wave.open(io.BytesIO(raw),'rb') as reader:
        if (reader.getnchannels(),reader.getsampwidth(),reader.getframerate(),reader.getnframes(),reader.getcomptype())!=(1,2,22050,len(values),'NONE') or reader.readframes(len(values))!=raw[44:]:
            raise ValueError('independent wave parser mismatch')
    return values


def validate(root,manifest):
    root=Path(root)
    expected={PREFIX+'LICENSE.txt'}|{PREFIX+n+suffix for n in SPECS for suffix in ('.wav','.wav.LICENSE.txt')}
    entries=manifest['entries']
    names=[e['path'] for e in entries]
    if names!=sorted(expected):
        raise ValueError('manifest exact membership/order')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    if actual!=expected:
        raise ValueError('undeclared/missing audio files')
    measurements={}
    for entry in entries:
        raw=safe(root,entry['path']).read_bytes()
        if len(raw)!=entry['bytes'] or hashlib.sha256(raw).hexdigest()!=entry['sha256']:
            raise ValueError('audio hash/size mismatch: '+entry['path'])
        expected_notice=entry['path']+'.LICENSE.txt' if entry['path'].endswith('.wav') else PREFIX+'LICENSE.txt'
        if entry.get('license')!='MIT' or entry.get('original') is not True or entry.get('notice')!=expected_notice:
            raise ValueError('audio notice/provenance metadata')
        if entry['path'].endswith('.wav'):
            values=decode(raw)
            cue=Path(entry['path']).stem
            if entry.get('sample_rate')!=22050 or entry.get('channels')!=1 or entry.get('sample_width')!=2 or entry.get('frames')!=len(values) or entry.get('duration_seconds')!=len(values)/22050:
                raise ValueError('manifest PCM metadata mismatch')
            active=[False]*len(values)
            for start_ms,end_ms,*_ in SPECS[cue][1]:
                start,end=start_ms*22050//1000,end_ms*22050//1000
                for index in range(start,end):
                    active[index]=True
                    bound=min(8191,8191*(index-start)//110,8191*(end-1-index)//551)
                    if abs(values[index])>bound+1:
                        raise ValueError('per-pulse attack/release envelope')
            if any(value for index,value in enumerate(values) if not active[index]):
                raise ValueError('non-silent declared pulse gap')
            measurements[cue]=dict(frames=len(values),duration_seconds=len(values)/22050,peak=max(map(abs,values)),nonzero_samples=sum(v!=0 for v in values),first_sample=values[0],last_sample=values[-1],silent_gaps_ms=[])
            # Validate intended temporal patterns by detecting long silent gaps in the actual data.
            silence_start=None
            for i,value in enumerate(values+[1]):
                if value==0 and silence_start is None:
                    silence_start=i
                elif value!=0 and silence_start is not None:
                    if i-silence_start>=220:
                        measurements[cue]['silent_gaps_ms'].append([silence_start*1000//RATE,i*1000//RATE])
                    silence_start=None
        elif raw!=NOTICE:
            raise ValueError('audio per-file MIT notice')
    if sum(e['bytes'] for e in entries)!=manifest['raw_bytes']:
        raise ValueError('audio aggregate bytes')
    if len(measurements['predator_front']['silent_gaps_ms'])!=1 or len(measurements['predator_flank']['silent_gaps_ms'])!=2:
        raise ValueError('Predator temporal pattern distinction')
    return dict(status='PASS',cue_count=9,declared_files=19,raw_bytes=manifest['raw_bytes'],measurements=measurements,listening='NOT RUN',SDL_OpenAL_decode='NOT RUN',browser_gesture_playback='NOT RUN')


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('action',choices=('generate','validate','verify'))
    args=parser.parse_args()
    root=HERE/'pack-root'
    if args.action in ('generate','verify'):
        first=generate(root)
        (HERE/'manifest.json').write_text(canonical(first))
    if args.action=='verify':
        before={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
        second=generate(root)
        after={p.relative_to(root).as_posix():p.read_bytes() for p in root.rglob('*') if p.is_file()}
        if before!=after or canonical(first)!=canonical(second):
            raise ValueError('audio generation not byte-identical')
    if args.action in ('validate','verify'):
        result=validate(root,json.loads((HERE/'manifest.json').read_text()))
        result['two_runs_byte_identical']=args.action=='verify'
        result['python']=sys.version
        result['manifest_sha256']=hashlib.sha256((HERE/'manifest.json').read_bytes()).hexdigest()
        result['tool_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
        (HERE/'validation.json').write_text(canonical(result))
        print(canonical(result))
    else:
        print(f'Generated 9 cues, 19 declared files, {first["raw_bytes"]} raw bytes; playback NOT RUN')
    return 0


if __name__=='__main__':
    sys.exit(main())
