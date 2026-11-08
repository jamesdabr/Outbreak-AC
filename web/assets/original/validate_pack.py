#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Structural validation only; no native execution."""
import argparse
import binascii
import hashlib
import json
import math
from pathlib import Path, PurePosixPath
import shlex
import struct
import sys
import zlib

HERE=Path(__file__).resolve().parent


class Invalid(ValueError):
    pass


def require(condition, message):
    if not condition:
        raise Invalid(message)


def confined(root, name):
    p=PurePosixPath(name)
    require(bool(p.parts) and not p.is_absolute() and '..' not in p.parts and str(p)==name and '\\' not in name and ':' not in name,'invalid pack path: '+name)
    path=root/name
    require(not any(v.is_symlink() for v in (path,*[root/q for q in p.parents])),'pack symlink: '+name)
    require(path.resolve().is_relative_to(root.resolve()),'escaping pack path: '+name)
    require(not any(token in name.lower() for token in ('private','authkey','password','.git/','saved.cfg','autoexec.cfg')),'excluded pack path: '+name)
    return path


def decode_png(data):
    require(len(data)<=2*1024*1024,'PNG compressed limit')
    require(data[:8]==b'\x89PNG\r\n\x1a\n','PNG signature')
    offset=8
    parts=[]
    compressed=bytearray()
    license_text=None
    width=height=0
    ended=False
    while offset<len(data):
        require(offset+12<=len(data),'truncated PNG chunk')
        size=struct.unpack_from('>I',data,offset)[0]
        kind=data[offset+4:offset+8]
        require(size<=len(data)-offset-12,'truncated PNG payload')
        payload=data[offset+8:offset+8+size]
        crc=struct.unpack_from('>I',data,offset+8+size)[0]
        require(crc==binascii.crc32(kind+payload)&0xffffffff,'PNG CRC')
        if not parts:
            require(kind==b'IHDR' and size==13,'PNG IHDR order/length')
            width,height,depth,color,compression,filtering,interlace=struct.unpack('>IIBBBBB',payload)
            require(0<width<=512 and 0<height<=512,'PNG dimensions')
            require(not width&(width-1) and not height&(height-1),'PNG power-of-two dimensions')
            require((depth,color,compression,filtering,interlace)==(8,6,0,0,0),'PNG RGBA8 format')
        elif kind==b'IHDR':
            raise Invalid('duplicate PNG IHDR')
        if kind==b'IDAT':
            compressed.extend(payload)
        elif kind==b'tEXt' and payload.startswith(b'License\0'):
            license_text=payload[8:].decode('ascii')
        elif kind==b'IEND':
            require(size==0,'PNG IEND length')
            ended=True
            require(offset+12==len(data),'PNG trailing bytes')
        parts.append(kind)
        offset+=12+size
    require(ended and b'IDAT' in parts,'PNG missing image/end')
    require(license_text and 'Permission is hereby granted' in license_text,'PNG per-file permission notice')
    expected=height*(1+width*4)
    try:
        inflater=zlib.decompressobj()
        raw=inflater.decompress(bytes(compressed),expected+1)
        require(inflater.eof and not inflater.unused_data and not inflater.unconsumed_tail,'PNG stream bounds')
    except zlib.error as error:
        raise Invalid('PNG compression: '+str(error)) from error
    require(len(raw)==expected,'PNG scanline length')
    require(all(raw[y*(width*4+1)]==0 for y in range(height)),'PNG unsupported scanline filter')
    pixels=b''.join(raw[y*(width*4+1)+1:(y+1)*(width*4+1)] for y in range(height))
    return width,height,pixels


def decode_map(data):
    require(len(data)<=1024*1024,'map compressed limit')
    try:
        inflater=zlib.decompressobj(31)
        raw=inflater.decompress(data,1024*1024+1)
        require(inflater.eof and not inflater.unconsumed_tail and not inflater.unused_data and len(raw)<=1024*1024,'map gzip bounds/truncation')
    except zlib.error as error:
        raise Invalid('map gzip: '+str(error)) from error
    require(len(raw)>=980,'map truncated header')
    magic,version,header_size,factor,count=struct.unpack_from('<4s4i',raw)
    require((magic,version,factor)==(b'ACMP',10,6),'map version/magic/factor')
    require(980<=header_size<=980+4096 and 0<count<=32 and header_size+16*count<len(raw),'map header/entity bounds')
    require(struct.unpack_from('<i',raw,932)[0]==0,'map must use external original cfg')
    require(struct.unpack_from('<i',raw,936)[0]==0,'map timestamp must be deterministic')
    for n in range(3):
        require(sorted(raw[148+n*256:404+n*256])==list(range(256)),'map texture list permutation')
    extra=raw[980:header_size]
    # This original pack emits exactly one bounded HX_MAPINFO record, not script.
    offset=0
    def uint():
        nonlocal offset
        value=0
        for shift in (0,7,14,21):
            require(offset<len(extra),'truncated map extra integer')
            byte=extra[offset]; offset+=1
            value|=(byte&127)<<shift
            if not byte&128:
                return value
        raise Invalid('map extra integer overflow')
    size=uint(); flags=uint()
    require(flags==65 and size==len(extra)-offset,'map original notice record')
    notice=extra[offset:]
    require(notice.startswith(b'MIT\0Copyright 2026 Outbreak contributors;') and notice.endswith(b'\0'),'map per-file MIT notice')
    entities=[]
    for n in range(count):
        entity=struct.unpack_from('<4h4Bh bB',raw,header_size+n*16)
        x,y,z,angle,kind,a2,a3,a4,a5,a6,a7=entity
        require(kind in (1,2),'map undeclared entity/model/audio type')
        require(8<=x<56 and 8<=y<56 and 0<z<12,'entity bounds')
        if kind==2:
            require(a2 in (0,1,100) and 0<=angle<3600,'player start encoding')
        else:
            require(0<angle<=32 and 0<a2<=255,'light encoding')
        require((a3,a4,a5,a6,a7)==(0,0,0,0,0),'unexpected entity attributes')
        entities.append(entity)
    offset=header_size+count*16
    cells=[]
    while len(cells)<4096:
        require(offset<len(raw),'truncated RLE')
        code=raw[offset]; offset+=1
        if code==255:
            require(bool(cells) and offset<len(raw),'RLE repeat without predecessor/count')
            count=raw[offset]; offset+=1
            require(count>0 and len(cells)+count<=4096,'RLE repeat overflow/zero')
            cells.extend([cells[-1]]*count)
        elif code==0:
            require(offset+2<=len(raw),'truncated solid')
            wall,delta=raw[offset:offset+2]; offset+=2
            require(wall<5 and delta==0,'solid texture/delta')
            cells.append(dict(type=0,floor=0,ceil=0,wall=wall))
        elif code==4:
            require(offset+8<=len(raw),'truncated space')
            floor,ceil,wall,floor_tex,ceil_tex,delta,upper,tag=struct.unpack_from('<bb6B',raw,offset); offset+=8
            require(floor==0 and ceil in (8,12) and 0<=wall<5 and floor_tex==3 and ceil_tex==4 and delta==0 and upper==2 and tag==0,'space geometry/texture/tag')
            cells.append(dict(type=4,floor=floor,ceil=ceil,wall=wall))
        else:
            raise Invalid('unexpected RLE cube type '+str(code))
    require(offset==len(raw),'trailing RLE data')
    require(any(c['type']==4 for c in cells),'empty solid world')
    for y in range(64):
        for x in range(64):
            if x<2 or y<2 or x>=62 or y>=62:
                require(cells[y*64+x]['type']==0,'native MINBORD violation')
    for x,y,z,angle,kind,*_ in entities:
        if kind==2:
            require(clear(cells,x,y) and z-4.5>=0 and z+0.7<cells[y*64+x]['ceil'],'blocked player start or eye/head bounds')
    require(len([e for e in entities if e[4]==2])==4,'expected four proof start anchors')
    return cells,entities


def clear(cells,x,y,radius=1.1):
    # Circle versus solid unit-square test; source playerent radius=1.1.
    for cy in range(math.floor(y-radius),math.floor(y+radius)+1):
        for cx in range(math.floor(x-radius),math.floor(x+radius)+1):
            if not (0<=cx<64 and 0<=cy<64):
                return False
            if cells[cy*64+cx]['type']==0:
                nx=max(cx,min(x,cx+1)); ny=max(cy,min(y,cy+1))
                if (nx-x)**2+(ny-y)**2<radius**2:
                    return False
    return True


def route(cells,waypoints):
    for (ax,ay),(bx,by) in zip(waypoints,waypoints[1:]):
        steps=max(abs(bx-ax),abs(by-ay))*4
        for step in range(steps+1):
            amount=step/max(1,steps)
            require(clear(cells,ax+(bx-ax)*amount,ay+(by-ay)*amount),'blocked approach route')


def config_lines(data):
    require(len(data)<=64*1024,'config size limit')
    text=data.decode('utf-8')
    require('Permission is hereby granted' in text,'config per-file license')
    return [shlex.split(line) for line in text.splitlines() if line.strip() and not line.lstrip().startswith('//')]


def validate(root,manifest):
    root=Path(root)
    require(not root.is_symlink(),'root symlink')
    entries=manifest['entries']
    names=[e['path'] for e in entries]
    require(names==sorted(set(names)),'manifest source order/uniqueness')
    actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
    require(actual==set(names),'undeclared or missing pack files')
    for entry in entries:
        path=confined(root,entry['path'])
        raw=path.read_bytes()
        require(len(raw)==entry['bytes'] and hashlib.sha256(raw).hexdigest()==entry['sha256'],'entry content/hash mismatch: '+entry['path'])
        require(entry['original'] is True and entry['license']=='MIT' and entry['notice']=='LICENSE.txt','original permission record')
        require(entry['virtual_path']=='/outbreak/'+entry['path'],'virtual path mismatch')
        if path.suffix in ('.png','.jpg'):
            require(entry.get('encoded_format')=='PNG','encoded image format record')
            decode_png(raw)
    require(sum(e['bytes'] for e in entries)==manifest['raw_bytes'],'aggregate size mismatch')
    font_width,font_height,pixels=decode_png((root/'packages/outbreak/font.png').read_bytes())
    fonts={}
    current=None
    for words in config_lines((root/'config/font.cfg').read_bytes()):
        command=words[0]
        if command=='font':
            require(len(words)==5 and words[2]=='packages/outbreak/font.png' and words[3:]==['14','20'],'font texture/metrics')
            current=words[1]; require(current not in fonts,'duplicate font')
            fonts[current]=[]
        elif command=='fontskip':
            require(words==['fontskip','33'] and current,'font ASCII offset')
        elif command=='fontchar':
            require(len(words)==5 and current,'fontchar arguments')
            x,y,w,h=map(int,words[1:])
            require(0<=x<x+w<=font_width and 0<=y<y+h<=font_height,'font atlas bounds')
            require(any(pixels[(row*font_width+col)*4+3] for row in range(y,y+h) for col in range(x,x+w)),'blank ASCII glyph')
            fonts[current].append((x,y,w,h))
        else:
            require(words==['setfont','default'],'unexpected font command/reference')
    require(set(fonts)==set(manifest['provided_fonts']) and all(len(v)==94 for v in fonts.values()),'font coverage/names')
    map_cfgs=['config/default_map_settings.cfg','packages/maps/dev_outbreak_browser.cfg']
    for config in map_cfgs:
        texture_count=0
        for words in config_lines((root/config).read_bytes()):
            command=words[0]
            require(command in ('mapmodelreset','mapsoundreset','texturereset','texture','fog','fogcolour'),'inherited/unexpected map config command')
            if command=='texture':
                require(len(words)==3 and words[1]=='0','texture command format')
                texture='packages/textures/'+words[2]
                require(texture in names,'missing/non-original texture reference')
                confined(root,texture)
                texture_count+=1
        require(texture_count==5,'reserved native texture slot count')
    actions={}
    for words in config_lines((root/'config/browser.cfg').read_bytes()):
        command=words[0]
        if command=='keymap':
            require(len(words)==3,'keymap args'); int(words[1])
        elif command=='bind':
            require(len(words)==3 and words[2] in ('[forward]','[backward]','[left]','[right]','[jump]','[crouch]','[reload]','[attack]'),'unsafe/unknown bind')
            actions[words[1]]=words[2]
        elif command=='scriptcontext':
            require(len(words)==3 and words[1]=='MAPCFG' and words[2] in ('texture','texturereset','mapmodelreset','mapsoundreset','fog','fogcolour'),'map command context')
        elif command=='isolatecontext':
            require(words[1:] in (['MAPCFG'],['MDLCFG']),'context isolation')
        elif command=='sealcontexts':
            require(len(words)==1,'seal args')
        else:
            require(command in ('fov','sensitivity','hudgun','audio','soundvol','musicvol','dynshadow','stencilshadow','waterreflect','hideradar','hideigraphs','hidecompass','hideteam','autodownload') and len(words)==2,'unexpected browser config command/reference')
            float(words[1])
    require({k:actions.get(k) for k in ('W','S','A','D')}==dict(W='[forward]',S='[backward]',A='[left]',D='[right]'),'movement binds')
    cells,entities=decode_map((root/'packages/maps/dev_outbreak_browser.cgz').read_bytes())
    routes=dict(through=[(16,32),(48,32)],north=[(16,32),(16,18),(48,18),(48,32)],south=[(16,32),(16,46),(48,46),(48,32)])
    for path in routes.values():
        route(cells,path)
    require(not clear(cells,26,25) and not clear(cells,32,24),'structure walls absent')
    return dict(structural_validation='PASS',png_files=sum(n.endswith(('.png','.jpg')) for n in names),font_names=sorted(fonts),ascii_characters_per_font=94,map_cubes=len(cells),open_cells=sum(c['type']==4 for c in cells),entities=len(entities),player_starts=[dict(x=e[0],y=e[1],eye_z=e[2],yaw_degrees=e[3]/10,team=e[5]) for e in entities if e[4]==2],routes=routes,collision_probe=dict(wall=[26,25],clear_before=[22,25],expected_stop_x_upper_bound=24.9,player_radius=1.1),runtime_validation='NOT RUN',pack_raw_bytes=manifest['raw_bytes'])


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    try:
        result=validate(HERE/'pack-root',json.loads((HERE/'manifest.json').read_text()))
    except (Invalid,ValueError,OSError,KeyError) as error:
        print('validation error: '+str(error),file=sys.stderr)
        return 1
    (HERE/'validation.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,sort_keys=True))
    return 0


if __name__=='__main__':
    sys.exit(main())
