#!/usr/bin/env python3
"""Strict T080 DATA validation, no native decoder/config/runtime execution."""
import binascii
import json
from pathlib import Path
import struct
import sys
import zlib

sys.dont_write_bytecode=True
import candidate as c


def exact(actual,expected,label):
    c.require(type(actual) is type(expected),'schema type: '+label)
    if isinstance(expected,dict):
        c.require(set(actual)==set(expected),'schema keys: '+label)
        for key in expected:exact(actual[key],expected[key],label+'.'+key)
    elif isinstance(expected,list):
        c.require(len(actual)==len(expected),'schema length: '+label)
        for n,(a,b) in enumerate(zip(actual,expected)):exact(a,b,label+'[%d]'%n)
    else:c.require(actual==expected,'source value mismatch: '+label)


def decode(data):
    c.require(18<=len(data)<=1024*1024 and data[:10]==c.GZIP,'canonical gzip header/bounds')
    try:
        inflater=zlib.decompressobj(31);raw=inflater.decompress(data,1024*1024+1)
        c.require(inflater.eof and not inflater.unused_data and not inflater.unconsumed_tail and len(raw)<=1024*1024,'gzip EOF/expansion/trailing bounds')
    except zlib.error as e:raise ValueError('gzip CRC/deflate: '+str(e)) from e
    c.require(struct.unpack('<II',data[-8:])==(binascii.crc32(raw)&0xffffffff,len(raw)),'gzip footer')
    c.require(len(raw)>=980,'header truncated')
    magic,version,header,factor,count=struct.unpack_from('<4s4i',raw)
    c.require((magic,version,factor,count)==(b'ACMP',10,7,21),'native header/count')
    c.require(980<header<=5076 and header+16*count<len(raw),'native offsets')
    c.require(struct.unpack_from('<i',raw,924)[0]==1,'map revision')
    c.require(struct.unpack_from('<2i',raw,932)==(0,0),'no inline config/timestamp')
    for n in range(3):c.require(raw[148+n*256:404+n*256]==bytes(range(256)),'texture slots')
    extra=raw[980:header]
    c.require(len(extra)>2 and extra[0]==len(extra)-2 and extra[1]==65 and extra[2:].startswith(b'MIT\0') and extra[-1:]==b'\0','single bounded original HX_MAPINFO')
    entities=[c.ENTITY.unpack_from(raw,header+16*n) for n in range(count)]
    offset=header+16*count;cells=[]
    while len(cells)<16384:
        c.require(offset<len(raw),'RLE truncated');code=raw[offset];offset+=1
        if code==255:
            c.require(bool(cells) and offset<len(raw),'RLE missing predecessor/count')
            n=raw[offset];offset+=1;c.require(0<n<=16384-len(cells),'RLE overflow/zero')
            cells.extend([cells[-1]]*n)
        elif code==0:
            c.require(raw[offset:offset+2]==b'\x02\0','solid texture/delta');offset+=2;cells.append((0,0,0))
        elif code==4:
            c.require(offset+8<=len(raw),'SPACE bounds')
            floor,ceil,wall,ftex,ctex,delta,upper,tag=struct.unpack_from('<bb6B',raw,offset);offset+=8
            c.require(floor==0 and ceil in (12,16) and (wall,ftex,ctex,delta,upper,tag)==(2,3,4,0,2,0),'SPACE attrs')
            cells.append((4,floor,ceil))
        else:raise ValueError('unsupported native cell')
    c.require(offset==len(raw),'RLE exact EOF')
    return raw,entities,cells


def validate_map(data,p):
    raw,entities,cells=decode(data)
    # Independent inverse of physics yaw: source forward angle is native yaw-90.
    aims=(45,90,135,180,225,270,315,0)
    native=[]
    for i,e in enumerate(entities[:8]):
        x,y,z,angle,kind,a2,a3,a4,a5,a6,a7=e
        c.require((x,y)==tuple(p['cluster_centers'][i]) and z==5,'integer technical centres/eye z5')
        c.require((kind,a2,a3,a4,a5,a6,a7)==(2,100,0,0,0,0,0),'FFA fields')
        c.require(0<=angle<3600 and angle%10==0 and (angle//10-90)%360==aims[i],'source-derived native yaw inverse')
        native.append(angle)
    c.require(len(entities[8:])==13,'light budget')
    for e,xy in zip(entities[8:],c.LIGHTS):
        c.require(e==(*xy,10,24,1,220,0,0,0,0,0),'deterministic light layout/palette')
        c.require(cells[xy[1]*128+xy[0]][0]==4,'light solid position')
    rects=p['geometry_rectangles']['screens']+p['geometry_rectangles']['building']
    for i,actual in enumerate(cells):
        x,y=i%128,i//128
        blocked=x<8 or y<8 or x>=120 or y>=120 or any(x>=r[0] and y>=r[1] and x<r[2] and y<r[3] for r in rects)
        expected=(0,0,0) if blocked else (4,0,12 if 50<=x<78 and 50<=y<78 else 16)
        c.require(actual==expected,'source rectangle/floor/ceiling mismatch')
    c.require(data==c.map_bytes(p),'exact native header/extra/encoding determinism')
    return dict(cells=len(cells),open_cells=sum(e[0]==4 for e in cells),entities=len(entities),technical_ffa=8,
                lights=13,native_yaw_tenths=native,raw_bytes=len(raw),gzip_crc_isize_eof=True)


def validate_sidecar(data,p):
    side=json.loads(data)
    # Approved typed schema, order, fields and canonical coordinates; no grants.
    exact(side,c.sidecar(p),'sidecar')
    ids=[]
    for key in ('regions','deployment_clusters','loot','barricades','walkers','reinforcements','predators','portals','reserved_corridors'):
        rows=side[key];c.require([r['id'] for r in rows]==sorted(r['id'] for r in rows),'ID order')
        ids.extend(r['id'] for r in rows)
        if key=='deployment_clusters':
            for row in rows:ids.extend(s['id'] for s in row['slots'])
    ids.append(side['extraction']['id']);c.require(len(ids)==len(set(ids)),'duplicate cross-kind ID')
    slots=[s['position_q10'] for row in side['deployment_clusters'] for s in row['slots']]
    c.require(len(slots)==32 and slots[0]==[19072,19072,0] and len({tuple(s) for s in slots})==32,'exact fractional Q10 slots')
    c.require(all(type(v)is int and a[2]==0 for a in slots for v in a),'foot-origin integer convention')
    return dict(canonical_slots=32,integer_technical_starts_are_separate=True,unique_ids=len(ids),
                runtime_grants=False,nav_graph=False)


def validate(root,manifest):
    root=c.regular(root);payload=c.files(root)
    c.require(set(payload)==c.MEMBERS,'exact five-member pack')
    names=[e['path'] for e in manifest['entries']]
    c.require(names==sorted(c.MEMBERS),'manifest order/membership')
    for e in manifest['entries']:
        c.confined(root,e['path'])
        c.require(set(e)=={'path','bytes','sha256','license','notice'},'manifest entry schema')
        c.require(type(e['bytes'])is int and e['bytes']==len(payload[e['path']]) and e['sha256']==c.sha(payload[e['path']]),'manifest bytes/hash')
        c.require(e['license']=='MIT' and e['notice']=='LICENSE.txt','notice/license identity')
    p,materials=c.inputs()
    native=validate_map(payload[c.CGZ],p)
    side=validate_sidecar(payload[c.ANCHORS],p)
    expected=c.payloads()
    for name in c.MEMBERS:c.require(payload[name]==expected[name],'owned config/license/provenance/content mismatch: '+name)
    exact(manifest,c.manifest(payload),'manifest')
    return dict(status='PASS',profile=c.PROFILE,files=5,raw_bytes=sum(map(len,payload.values())),map=native,sidecar=side,
                texture_dependencies=materials,native_decoder=False,runtime=False,overlay=False,
                balance_capsule_navigation_gameplay='NOT RUN; not accepted')


if __name__=='__main__':
    result=validate(c.HERE/'pack-root',json.loads((c.HERE/'manifest.json').read_text()))
    print(c.canonical(result))
