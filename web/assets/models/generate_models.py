#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Independent T041 box models, no media inputs."""
import binascii
import hashlib
import json
import math
from pathlib import Path
import struct
import sys
import zlib

HERE=Path(__file__).resolve().parent
PREFIX='packages/models/outbreak/'
NOTICE=(HERE/'LICENSE.txt').read_bytes()
ANIMS=['idle','run','attack','pain','jump','land','flipoff','salute','taunt','wave','point','crouch idle','crouch walk','crouch attack','crouch pain','crouch death','death','lying dead','flag','gun idle','gun shoot','gun reload','gun throw','mapmodel','trigger','decay','all']
FACES=[((0,3,2,1),(0,0,-1)),((4,5,6,7),(0,0,1)),((3,7,6,2),(0,1,0)),((0,1,5,4),(0,-1,0)),((0,4,7,3),(-1,0,0)),((1,2,6,5),(1,0,0))]


def canonical(data):
    return json.dumps(data,indent=2,sort_keys=True)+'\n'


def box(name,bounds,tile=0):
    return (name,bounds,tile)


def survivor(frame):
    crouch=frame in (9,*range(10,18),23,24)
    dead=frame in (22,25)
    if dead:
        # Compact curled lying pose: stays within the approved 2.2 horizontal envelope.
        return [box('torso',(-.55,-.65,.15,.55,.4,.65),0),box('pelvis',(-.55,-1,.1,.55,-.55,.55),0),
          box('head',(-.35,.4,.45,.35,1.05,1.15),1),box('neck',(-.2,.28,.4,.2,.52,.6),1),
          box('upper_arm_-1',(-1,-.4,.1,-.6,.25,.45),0),box('upper_arm_1',(.6,-.4,.1,1,.25,.45),0),
          box('forearm_-1',(-.9,.25,.1,-.5,.7,.4),1),box('forearm_1',(.5,.25,.1,.9,.7,.4),1),
          box('thigh_-1',(-.95,-.85,.05,-.58,-.15,.35),0),box('thigh_1',(.58,-.85,.05,.95,-.15,.35),0),
          box('calf_-1',(-.95,-.15,0,-.58,.5,.28),0),box('calf_1',(.58,-.15,0,.95,.5,.28),0),
          box('foot_-1',(-1,.45,0,-.55,.85,.25),2),box('foot_1',(.55,.45,0,1,.85,.25),2)]
    cycle=frame-1 if 1<=frame<=8 else frame-10 if 10<=frame<=17 else None
    swing=[0,.3,.45,.3,0,-.3,-.45,-.3][cycle] if cycle is not None else 0
    left_lift=[0,.10,.22,.16,.03,0,0,0][cycle] if cycle is not None else 0
    right_lift=[.03,0,0,0,0,.10,.22,.16][cycle] if cycle is not None else 0
    if crouch:
        swing*=.6
    waist=1.55 if crouch else 2.6
    shoulder=2.75 if crouch else 4.2
    top=3.65 if crouch else 5.2
    lean=.16 if frame in (20,24) else .3 if frame==21 else 0
    if frame==21:
        waist=1.5; shoulder=2.7; top=3.6
    result=[box('pelvis',(-.6,-.28,waist-.25,.6,.28,waist+.2)),box('torso',(-.65,-.32+lean,waist+.15,.65,.32+lean,shoulder),0),box('neck',(-.2,-.18+lean,shoulder,.2,.18+lean,top-.75),1),box('head',(-.36,-.32+lean,top-.75,.36,.32+lean,top),1)]
    for side,lift in ((-1,left_lift),(1,right_lift)):
        stride=swing*side
        if frame==18:
            lift=.4; stride=side*.25
        cx=side*.33
        result += [box('thigh_'+str(side),(cx-.23,-.22+stride*.4,waist*.52,cx+.23,.22+stride*.4,waist)),box('calf_'+str(side),(cx-.2,-.2+stride, .25+lift,cx+.2,.2+stride,waist*.55)),box('foot_'+str(side),(cx-.25,-.24+stride,lift,cx+.25,.4+stride,.3+lift),2)]
        arm_y=-stride*.6+.15
        hand_z=shoulder-1.25
        if frame in (19,23):
            arm_y=.55; hand_z=shoulder-.45
        result += [box('upper_arm_'+str(side),(side*.83-.17,arm_y-.2,shoulder-.7,side*.83+.17,arm_y+.2,shoulder),0),box('forearm_'+str(side),(side*.83-.16,arm_y-.18,hand_z,side*.83+.16,arm_y+.18,max(hand_z+.25,shoulder-.55)),1)]
    return result


def weapon(name,frame):
    recoil=-.07 if frame==1 else 0
    if name=='pistol':
        return [box('slide',(-.18,-.12+recoil,.05,.18,.9+recoil,.33),2),box('barrel',(-.09,.85+recoil,.1,.09,1.15+recoil,.26),2),box('grip',(-.14,-.08,-.55,.14,.28,.12),0),box('magazine',(-.12,-.04,-.7 if frame==2 else -.5,.12,.24,-.12),3)]
    return [box('receiver',(-.19,-.25+recoil,-.03,.19,1.1+recoil,.3),2),box('barrel',(-.08,1.05+recoil,.07,.08,2.2+recoil,.23),2),box('stock',(-.18,-.95,0,.18,-.2,.26),0),box('grip',(-.12,-.13,-.48,.12,.17,.08),0),box('magazine',(-.13,.34,-.75 if frame==2 else -.55,.13,.65,-.04),3),box('sight',(-.07,.7,.3,.07,.87,.47),3)]


def topology(parts):
    vertices=[]; normals=[]; uv=[]; triangles=[]
    for name,b,tile in parts:
        x0,y0,z0,x1,y1,z1=b
        corners=[(x0,y0,z0),(x1,y0,z0),(x1,y1,z0),(x0,y1,z0),(x0,y0,z1),(x1,y0,z1),(x1,y1,z1),(x0,y1,z1)]
        for face,normal in FACES:
            selected=3 if normal==(0,1,0) and name=='head' else 2 if normal==(0,1,0) and name=='torso' else tile
            ox,oy=(selected%2)*32,(selected//2)*32
            coords=[((ox+2)/64,(oy+2)/64),((ox+30)/64,(oy+2)/64),((ox+30)/64,(oy+30)/64),((ox+2)/64,(oy+30)/64)]
            # Native GL culls GL_FRONT. Engine-facing triangles must be clockwise;
            # MD3's x/y swap makes these CCW in file coordinates.
            ordered=[face[0],face[3],face[2],face[1]]
            base=len(vertices)
            for index,st in zip(ordered,coords):
                vertices.append(corners[index]); normals.append(normal); uv.append(st)
            triangles += [(base,base+1,base+2),(base,base+2,base+3)]
    return vertices,normals,uv,triangles


def encoded_normal(engine_normal):
    # Construction front +Y -> native front +X via -90deg Z, then file x/y swap.
    x,y,z=-engine_normal[0],engine_normal[1],engine_normal[2]
    polar=round(math.acos(z)*255/(2*math.pi))&255
    azimuth=round(math.atan2(y,x)*255/(2*math.pi))&255
    return (polar<<8)|azimuth


def animations(name):
    if name!='survivor':
        return {a:(0,1,8) for a in ANIMS}|{'attack':(1,1,12),'crouch attack':(1,1,12),'gun shoot':(1,1,12),'gun reload':(2,1,6),'all':(0,3,8)}
    result={a:(0,1,8) for a in ANIMS}
    result.update({'run':(1,8,10),'attack':(19,1,8),'pain':(20,1,8),'jump':(18,1,8),'point':(19,1,8),'crouch idle':(9,1,8),'crouch walk':(10,8,8),'crouch attack':(23,1,8),'crouch pain':(24,1,8),'crouch death':(25,1,8),'death':(21,2,6),'lying dead':(22,1,8),'decay':(22,1,8),'all':(0,26,8)})
    return result


def model(name):
    frame_count=26 if name=='survivor' else 3
    tags=('tag_weapon','tag_head') if name=='survivor' else ()
    frames=[]; tag_data=[]; vertex_data=[]; bounds=[]; tag_frames=[]
    first=None
    for frame in range(frame_count):
        parts=sorted(survivor(frame) if name=='survivor' else weapon(name,frame),key=lambda part:part[0])
        vertices,normals,uv,tris=topology(parts)
        if first is None:
            first=(uv,tris,len(vertices))
        quantized=[(round(-x*1024),round(y*1024),round(z*1024)) for x,y,z in vertices]
        actual=[tuple(v/64 for v in xyz) for xyz in quantized]
        low=[min(v[axis] for v in actual) for axis in range(3)]
        high=[max(v[axis] for v in actual) for axis in range(3)]
        radius=max(math.sqrt(sum(n*n for n in v)) for v in actual)+.01
        frames.append(struct.pack('<10f16s',*low,*high,0,0,0,radius,('pose_'+str(frame)).encode()))
        bounds.append(dict(min_engine=[low[1]/16,low[0]/16,low[2]/16],max_engine=[high[1]/16,high[0]/16,high[2]/16]))
        for xyz,normal in zip(quantized,normals):
            vertex_data.append(struct.pack('<3hH',*xyz,encoded_normal(normal)))
        frame_tags={}
        if tags:
            head=next(b for part,b,tile in parts if part=='head')
            forearm=next(b for part,b,tile in parts if part=='forearm_1')
            positions=[tuple((forearm[i]+forearm[i+3])/2 for i in range(3)),tuple((head[i]+head[i+3])/2 for i in range(3))]
            for tag,pos in zip(tags,positions):
                x,y,z=pos
                packed=struct.pack('<64s12f',tag.encode(),-x*16,y*16,z*16,1,0,0,0,1,0,0,0,1)
                tag_data.append(packed)
                stored=struct.unpack('<64s12f',packed)
                frame_tags[tag]=[stored[2]/16,stored[1]/16,stored[3]/16]
        tag_frames.append(frame_tags)
    uv,tris,vertex_count=first
    triangle_bytes=b''.join(struct.pack('<3i',*t) for t in tris)
    shader=struct.pack('<64si',(PREFIX+name+'/skin.png').encode(),0)
    texcoords=b''.join(struct.pack('<2f',*v) for v in uv)
    vertices=b''.join(vertex_data)
    tri_offset=108; shader_offset=tri_offset+len(triangle_bytes); uv_offset=shader_offset+len(shader); vertex_offset=uv_offset+len(texcoords); end=vertex_offset+len(vertices)
    surface=struct.pack('<4s64s10i',b'IDP3',b'body',0,frame_count,1,vertex_count,len(tris),tri_offset,shader_offset,uv_offset,vertex_offset,end)+triangle_bytes+shader+texcoords+vertices
    frame_offset=108; tags_offset=frame_offset+frame_count*56; mesh_offset=tags_offset+frame_count*len(tags)*112
    header=struct.pack('<4si64s9i',b'IDP3',15,('outbreak_'+name).encode(),0,frame_count,len(tags),1,0,frame_offset,tags_offset,mesh_offset,mesh_offset+len(surface))
    return header+b''.join(frames)+b''.join(tag_data)+surface,dict(frames=frame_count,surfaces=1,vertices_per_surface=vertex_count,triangles_per_surface=len(tris),uv_range=[0,1],tags=list(tags),frame_tags_engine=tag_frames,tag_basis='identity right-handed; origins follow right forearm and head centers',frame_bounds=bounds,animations=animations(name),native_scale=100,file_to_engine='swap x/y then divide by16; packed coordinates engine*1024',surface='body',native_forward='+X',construction_to_native='rotate -90 degrees around Z before file x/y swap')


def png(name):
    palettes={'survivor':[(45,76,100),(191,151,113),(230,160,55),(204,170,131)],'pistol':[(49,55,65),(125,135,146),(92,103,120),(225,149,54)],'rifle':[(65,84,63),(136,144,131),(76,83,91),(201,159,70)]}
    colors=palettes[name]
    def pixel(x,y):
        tile=(y//32)*2+x//32
        color=colors[tile]
        if name=='survivor' and tile==3 and 10<=x%32<=22 and 9<=y%32<=13:
            color=(30,37,42)  # original front visor strip
        return bytes((*color,255))
    raw=b''.join(b'\0'+b''.join(pixel(x,y) for x in range(64)) for y in range(64))
    def chunk(kind,data):
        return struct.pack('>I',len(data))+kind+data+struct.pack('>I',binascii.crc32(kind+data)&0xffffffff)
    return b'\x89PNG\r\n\x1a\n'+chunk(b'IHDR',struct.pack('>IIBBBBB',64,64,8,6,0,0,0))+chunk(b'tEXt',b'License\0'+NOTICE)+chunk(b'IDAT',zlib.compress(raw,9))+chunk(b'IEND',b'')


def config(name):
    lines=['// '+line for line in NOTICE.decode().splitlines()]+['md3load tris.md3','md3skin body skin.png','mdlscale 100','mdltrans 0 0 0']
    for animation,(start,count,fps) in animations(name).items():
        lines.append(f'md3anim "{animation}" {start} {count} {fps}')
    return ('\n'.join(lines)+'\n').encode()


def safe(root,name):
    from pathlib import PurePosixPath
    p=PurePosixPath(name)
    if not name.startswith(PREFIX) or p.is_absolute() or '..' in p.parts or str(p)!=name or '\\' in name:
        raise ValueError('invalid model path: '+name)
    path=root/name
    if any(item.is_symlink() for item in (root,path,*[root/parent for parent in p.parents])):
        raise ValueError('model symlink: '+name)
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError('model path escape: '+name)
    return path


def generate(root):
    root=Path(root)
    files={PREFIX+'LICENSE.txt':(NOTICE,'original scoped MIT notice')}
    metadata={}
    for name in ('survivor','pistol','rifle'):
        data,info=model(name); metadata[name]=info
        for filename,raw in (('tris.md3',data),('skin.png',png(name)),('md3.cfg',config(name))):
            path=PREFIX+name+'/'+filename
            files[path]=(raw,'original box geometry, per-face palette UVs, pose transforms and native command references; no stock inputs')
            files[path+'.LICENSE.txt']=(NOTICE,'per-original-file MIT notice')
    if root.is_symlink():
        raise ValueError('model root symlink')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()} if root.exists() else set()
    if actual-set(files):
        raise ValueError('undeclared model files: '+','.join(sorted(actual-set(files))))
    for name in files:
        safe(root,name)
    entries=[]
    for name,(raw,reason) in sorted(files.items()):
        path=safe(root,name);path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw)
        entry=dict(path=name,bytes=len(raw),sha256=hashlib.sha256(raw).hexdigest(),license='MIT',notice=name+'.LICENSE.txt' if not name.endswith('LICENSE.txt') else PREFIX+'LICENSE.txt',original=True,provenance=reason)
        if name.endswith('.md3'):
            entry['format']='MD3 version15';entry['model']=metadata[Path(name).parent.name]
        elif name.endswith('.png'):
            entry.update(format='PNG RGBA8',dimensions=[64,64],palette_layout='four 32x32 quadrants; survivor front head visor and chest panel differ from back')
        entries.append(entry)
    return dict(schema_version=1,ticket='T041 revision1.5',models=metadata,entries=entries,raw_bytes=sum(e['bytes'] for e in entries),staged_only=True,runtime_verified=False,gameplay_mapping_implemented=False)


if __name__=='__main__':
    result=generate(HERE/'pack-root')
    (HERE/'manifest.json').write_text(canonical(result))
    print(f'Generated {len(result["entries"])} original files, {result["raw_bytes"]} raw bytes; runtime NOT RUN')
