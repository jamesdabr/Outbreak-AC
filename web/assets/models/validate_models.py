#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Bounded data decoder, no engine/script execution."""
import binascii
import hashlib
import json
import math
from pathlib import Path
import shlex
import struct
import sys
import zlib

HERE=Path(__file__).resolve().parent
PREFIX='packages/models/outbreak/'
NATIVE_ANIMS={'idle','run','attack','pain','jump','land','flipoff','salute','taunt','wave','point','crouch idle','crouch walk','crouch attack','crouch pain','crouch death','death','lying dead','flag','gun idle','gun shoot','gun reload','gun throw','mapmodel','trigger','decay','all'}


class Invalid(ValueError):
    pass


def require(condition,message):
    if not condition:
        raise Invalid(message)


def text(raw):
    require(b'\0' in raw,'unterminated MD3 name')
    return raw.split(b'\0',1)[0].decode('ascii')


def finite(values):
    require(all(math.isfinite(v) for v in values),'non-finite MD3 float')


def cross(a,b):
    return (a[1]*b[2]-a[2]*b[1],a[2]*b[0]-a[0]*b[2],a[0]*b[1]-a[1]*b[0])


def dot(a,b):
    return sum(x*y for x,y in zip(a,b))


def decode_md3(raw):
    require(108<=len(raw)<=8*1024*1024,'MD3 size bound')
    magic,version,name,flags,nf,nt,ns,skins,fo,to,so,end=struct.unpack_from('<4si64s9i',raw)
    require(magic==b'IDP3' and version==15,'MD3 magic/version')
    text(name)
    require(flags==0 and skins==0 and 1<=nf<=64 and 0<=nt<=8 and 1<=ns<=8,'MD3 counts/flags')
    require(fo==108 and to==fo+nf*56 and so==to+nf*nt*112 and so<=end==len(raw),'MD3 section offsets')
    frames=[]
    for frame in range(nf):
        record=struct.unpack_from('<10f16s',raw,fo+frame*56)
        finite(record[:10]); text(record[10])
        low,high,origin,radius=record[:3],record[3:6],record[6:9],record[9]
        require(all(a<b for a,b in zip(low,high)) and radius>0,'MD3 frame bounds/radius')
        frames.append(dict(min=low,max=high,origin=origin,radius=radius))
    tags=[]
    for frame in range(nf):
        current={}
        for n in range(nt):
            record=struct.unpack_from('<64s12f',raw,to+(frame*nt+n)*112)
            name=text(record[0]);finite(record[1:])
            require(name and name not in current,'MD3 tag names')
            matrix=[record[4:7],record[7:10],record[10:13]]
            require(all(abs(dot(matrix[i],matrix[j])-(1 if i==j else 0))<1e-4 for i in range(3) for j in range(3)) and dot(matrix[0],cross(matrix[1],matrix[2]))>.999,'MD3 tag rotation')
            current[name]=record[1:4]
        if tags:
            require(tuple(current)==tuple(tags[0]),'MD3 frame tag continuity')
        tags.append(current)
    surfaces=[]
    all_vertices=[[] for _ in range(nf)]
    for index in range(ns):
        require(so+108<=end,'truncated MD3 surface')
        magic,name,flags,sf,sh,nv,ntri,ot,osh,ouv,ov,se=struct.unpack_from('<4s64s10i',raw,so)
        name=text(name)
        require(magic==b'IDP3' and flags==0 and sf==nf and 1<=sh<=8 and 1<=nv<=512 and 1<=ntri<=1024,'MD3 surface counts/magic/frames')
        require(ot==108 and osh==ot+ntri*12 and ouv==osh+sh*68 and ov==ouv+nv*8 and se==ov+nf*nv*8 and so+se<=end,'MD3 surface section offsets')
        tris=[struct.unpack_from('<3i',raw,so+ot+t*12) for t in range(ntri)]
        require(all(len(set(t))==3 and all(0<=v<nv for v in t) for t in tris),'MD3 triangle indices')
        shaders=[]
        for n in range(sh):
            shader,num=struct.unpack_from('<64si',raw,so+osh+n*68)
            shader=text(shader)
            require(shader.startswith(PREFIX) and '..' not in Path(shader).parts and num==0,'MD3 shader reference')
            shaders.append(shader)
        uv=[struct.unpack_from('<2f',raw,so+ouv+v*8) for v in range(nv)]
        finite([x for st in uv for x in st])
        require(all(0<=x<=1 for st in uv for x in st),'MD3 UV bounds')
        vertices=[]
        for frame in range(nf):
            positions=[]; normals=[]
            for vertex in range(nv):
                x,y,z,normal=struct.unpack_from('<3hH',raw,so+ov+(frame*nv+vertex)*8)
                pos=(x/64,y/64,z/64)
                polar=(normal>>8)*2*math.pi/255;azimuth=(normal&255)*2*math.pi/255
                n=(math.sin(polar)*math.cos(azimuth),math.sin(polar)*math.sin(azimuth),math.cos(polar))
                require(abs(dot(n,n)-1)<1e-6,'MD3 normal encoding')
                positions.append(pos);normals.append(n)
            for tri in tris:
                a,b,c=[positions[i] for i in tri]
                geometric=cross(tuple(b[i]-a[i] for i in range(3)),tuple(c[i]-a[i] for i in range(3)))
                magnitude=math.sqrt(dot(geometric,geometric))
                require(magnitude>1e-5,'degenerate MD3 triangle/frame')
                require(all(dot(geometric,normals[v])/magnitude>.98 for v in tri),'MD3 normal/winding agreement')
            all_vertices[frame].extend(positions)
            vertices.append(positions)
        surfaces.append(dict(name=name,vertices=nv,triangles=ntri,shaders=shaders,uv=uv,tri_indices=tris,positions=vertices,vertex_offset=so+ov))
        so+=se
    require(so==end,'MD3 trailing surfaces/bytes')
    for frame,positions in enumerate(all_vertices):
        bounds=frames[frame]
        require(all(all(bounds['min'][axis]-.01<=position[axis]<=bounds['max'][axis]+.01 for axis in range(3)) for position in tags[frame].values()),'MD3 tag position bounds')
        for axis in range(3):
            require(abs(min(p[axis] for p in positions)-bounds['min'][axis])<1e-4 and abs(max(p[axis] for p in positions)-bounds['max'][axis])<1e-4,'MD3 frame bounds mismatch')
        require(all(math.sqrt(sum((v-bounds['origin'][i])**2 for i,v in enumerate(p)))<=bounds['radius']+1e-4 for p in positions),'MD3 frame radius mismatch')
    return dict(frames=nf,tag_count=nt,surfaces=surfaces,frame_bounds=frames,tags=tags)


def decode_png(raw,include_pixels=False):
    require(raw[:8]==b'\x89PNG\r\n\x1a\n' and len(raw)<=1024*1024,'PNG signature/limit')
    offset=8; compressed=bytearray();width=height=0;notice=False;ended=False;chunks=0
    while offset<len(raw):
        require(offset+12<=len(raw),'PNG truncated chunk')
        size=struct.unpack_from('>I',raw,offset)[0];kind=raw[offset+4:offset+8]
        require(chunks<4 and kind==(b'IHDR',b'tEXt',b'IDAT',b'IEND')[chunks],'PNG chunk order/type')
        chunks+=1
        require(size<=len(raw)-offset-12,'PNG chunk bounds')
        payload=raw[offset+8:offset+8+size]
        require(struct.unpack_from('>I',raw,offset+8+size)[0]==binascii.crc32(kind+payload)&0xffffffff,'PNG CRC')
        if offset==8:
            require(kind==b'IHDR' and size==13,'PNG IHDR')
            width,height,depth,color,comp,filtering,interlace=struct.unpack('>IIBBBBB',payload)
            require(0<width<=128 and 0<height<=128 and not width&(width-1) and not height&(height-1) and (depth,color,comp,filtering,interlace)==(8,6,0,0,0),'PNG dimensions/format')
        if kind==b'IDAT':compressed.extend(payload)
        if kind==b'tEXt' and payload.startswith(b'License\0') and b'Permission is hereby granted' in payload:notice=True
        if kind==b'IEND':
            require(size==0 and offset+12==len(raw),'PNG ending');ended=True
        offset+=size+12
    require(ended and notice and chunks==4,'PNG end/notice')
    expected=height*(width*4+1)
    try:
        inflater=zlib.decompressobj();pixels=inflater.decompress(compressed,expected+1)
        require(inflater.eof and not inflater.unused_data and not inflater.unconsumed_tail and len(pixels)==expected,'PNG data bounds')
    except zlib.error as error:raise Invalid('PNG compression') from error
    require(all(pixels[y*(width*4+1)]==0 for y in range(height)),'PNG row filtering')
    result=dict(width=width,height=height)
    if include_pixels:
        result['rgba']=b''.join(pixels[y*(width*4+1)+1:(y+1)*(width*4+1)] for y in range(height))
    return result


def decode_config(raw,name,model,declared):
    require(len(raw)<=32768 and b'Permission is hereby granted' in raw,'config size/notice')
    animations={};load=skin=scale=trans=0
    for line in raw.decode().splitlines():
        if not line.strip() or line.lstrip().startswith('//'):continue
        require(not any(c in line for c in '$[]();'),'dynamic config expression')
        words=shlex.split(line);command=words[0]
        if command=='md3load':
            require(words==['md3load','tris.md3'],'MD3 config load reference');load+=1
        elif command=='md3skin':
            require(words==['md3skin','body','skin.png'] and PREFIX+name+'/skin.png' in declared,'MD3 config skin reference');skin+=1
        elif command=='mdlscale':require(words==['mdlscale','100'],'model scale');scale+=1
        elif command=='mdltrans':require(words==['mdltrans','0','0','0'],'model translation');trans+=1
        elif command=='md3anim':
            require(len(words)==5 and words[1] in NATIVE_ANIMS and words[1] not in animations,'native animation name/uniqueness')
            start,count=int(words[2]),int(words[3]);speed=float(words[4]);finite([speed])
            require(start>=0 and count>=1 and start+count<=model['frames'] and 0<speed<=120,'animation range/speed')
            animations[words[1]]=(start,count,speed)
        else:raise Invalid('unapproved config command: '+command)
    require((load,skin,scale,trans)==(1,1,1,1),'config core commands')
    required=NATIVE_ANIMS if name=='survivor' else {'gun idle','gun shoot','gun reload'}
    require(required<=set(animations),'missing native animation mappings')
    return animations


def validate(root,manifest):
    from generate_models import safe
    root=Path(root)
    expected={PREFIX+'LICENSE.txt'}|{PREFIX+n+'/'+f+s for n in ('survivor','pistol','rifle') for f in ('tris.md3','skin.png','md3.cfg') for s in ('','.LICENSE.txt')}
    names=[e['path'] for e in manifest['entries']]
    require(names==sorted(expected),'model manifest membership/order')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual==expected,'undeclared/missing model files')
    for entry in manifest['entries']:
        raw=safe(root,entry['path']).read_bytes()
        require(len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256'],'model hash/size mismatch')
        require(entry['license']=='MIT' and entry['original'] is True,'model license/provenance')
        notice=entry['path']+'.LICENSE.txt' if not entry['path'].endswith('LICENSE.txt') else PREFIX+'LICENSE.txt'
        require(entry['notice']==notice and (root/notice).is_file(),'model notice reference')
        if entry['path'].endswith('LICENSE.txt'):
            require(b'Permission is hereby granted' in raw and b'T041' in raw,'model scoped notice')
    require(sum(e['bytes'] for e in manifest['entries'])==manifest['raw_bytes'],'model aggregate bytes')
    results={};decoded={}
    for name in ('survivor','pistol','rifle'):
        prefix=PREFIX+name+'/'
        model=decode_md3((root/(prefix+'tris.md3')).read_bytes())
        require(len(model['surfaces'])==1 and model['surfaces'][0]['name']=='body','original surface identity')
        require(model['surfaces'][0]['shaders']==[prefix+'skin.png'],'exact original shader reference')
        image=decode_png((root/(prefix+'skin.png')).read_bytes())
        animations=decode_config((root/(prefix+'md3.cfg')).read_bytes(),name,model,expected)
        info=manifest['models'][name]
        measured_bounds=[dict(min_engine=[b['min'][1]/16,b['min'][0]/16,b['min'][2]/16],max_engine=[b['max'][1]/16,b['max'][0]/16,b['max'][2]/16]) for b in model['frame_bounds']]
        require(info['frame_bounds']==measured_bounds,'model bounds metadata')
        measured_tags=[{tag:[pos[1]/16,pos[0]/16,pos[2]/16] for tag,pos in tags.items()} for tags in model['tags']]
        require(info['frame_tags_engine']==measured_tags,'model tag metadata')
        require(info['frames']==model['frames'] and info['vertices_per_surface']==model['surfaces'][0]['vertices'] and info['triangles_per_surface']==model['surfaces'][0]['triangles'],'model count metadata')
        require({k:list(v) for k,v in animations.items()}=={k:list(v) for k,v in info['animations'].items()},'animation metadata')
        if name=='survivor':
            require(model['frames']==26 and all(set(t)=={'tag_weapon','tag_head'} for t in model['tags']),'survivor frames/tags')
            coords=model['surfaces'][0]['positions']
            for start in (1,10):
                fingerprints={hashlib.sha256(str(frame).encode()).hexdigest() for frame in coords[start:start+8]}
                require(len(fingerprints)==8,'non-genuine run/crouch cycle')
                # Relative limb geometry must change; rigid translations do not suffice.
                anchors=[tuple(frame[24][i]-frame[0][i] for i in range(3)) for frame in coords[start:start+8]]
                require(len(set(anchors))>1,'rigid-only walk cycle')
            standing=model['frame_bounds'][0]
            require(abs(standing['min'][2]/16)<.001 and abs(standing['max'][2]/16-5.2)<.001,'standing visual feet/height')
            require(model['frame_bounds'][9]['max'][2]<standing['max'][2] and model['frame_bounds'][22]['max'][2]/16<1.3,'crouch/lying pose distinction')
            for bounds in model['frame_bounds']:
                require(all((bounds['max'][i]-bounds['min'][i])/16<=2.2 for i in (0,1)),'survivor horizontal visual extent')
        else:require(model['frames']==3,'weapon frame count')
        results[name]=dict(frames=model['frames'],vertices=model['surfaces'][0]['vertices'],triangles=model['surfaces'][0]['triangles'],tags=list(model['tags'][0]),texture=image,standing_or_idle_bounds_file_units=model['frame_bounds'][0],animation_ranges=animations)
        decoded[name]=model
    return dict(status='PASS',declared_files=19,raw_bytes=manifest['raw_bytes'],models=results,actual_engine_load='NOT RUN',actual_browser_render_animation_attachment='NOT RUN'),decoded


if __name__=='__main__':
    result,_=validate(HERE/'pack-root',json.loads((HERE/'manifest.json').read_text()))
    (HERE/'validation.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
