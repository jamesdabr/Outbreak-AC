#!/usr/bin/env python3
"""SPDX-License-Identifier: MIT. Generate only independently authored T027 content.
No upstream media/config/map bytes are read, imported, or transformed.
"""
import argparse
import binascii
import hashlib
import json
from pathlib import Path
import struct
import sys
import zlib

from glyphs import glyph

HERE = Path(__file__).resolve().parent
MAP_NAME = 'dev_outbreak_browser'
NOTICE = (HERE / 'LICENSE.txt').read_text(encoding='utf-8')
COMMENT = ''.join('// ' + line + '\n' for line in NOTICE.splitlines()) + '\n'


def canonical(data):
    return json.dumps(data, indent=2, sort_keys=True) + '\n'


def chunk(kind, data):
    return struct.pack('>I',len(data)) + kind + data + struct.pack('>I',binascii.crc32(kind+data)&0xffffffff)


def png(width, height, pixel):
    raw = b''.join(b'\0'+bytes(component for x in range(width) for component in pixel(x,y)) for y in range(height))
    return (b'\x89PNG\r\n\x1a\n' + chunk(b'IHDR',struct.pack('>IIBBBBB',width,height,8,6,0,0,0))
            + chunk(b'tEXt',b'License\0'+NOTICE.encode('ascii'))
            + chunk(b'IDAT',zlib.compress(raw,9)) + chunk(b'IEND',b''))


def atlas():
    def pixel(x,y):
        index=(y//20)*16+x//16
        code=index+33
        gx,gy=(x%16-2)//2,(y%20-2)//2
        on=code<=126 and 0<=gx<5 and 0<=gy<7 and glyph(chr(code))[gy][gx]=='1'
        return (255,255,255,255 if on else 0)
    return png(256,128,pixel)


def font_config():
    lines=[COMMENT]
    # API names are source interfaces; metrics/pixel data are original.
    for name in ('default','mono','huddigits','serverquality','bargraphs','radaricons'):
        lines += [f'font {name} "packages/outbreak/font.png" 14 20','fontskip 33']
        for index in range(94):
            lines.append(f'fontchar {(index%16)*16+1} {(index//16)*20} 14 20')
    lines += ['setfont default','']
    return '\n'.join(lines).encode('utf-8')


def browser_config():
    lines=[COMMENT,'// Minimal original offline-map bindings; browser pointer lifecycle belongs to T028.']
    for code,name,action in ((119,'W','forward'),(115,'S','backward'),(97,'A','left'),(100,'D','right'),(32,'SPACE','jump'),(99,'C','crouch'),(114,'R','reload'),(-1,'MOUSE1','attack')):
        lines += [f'keymap {code} {name}',f'bind {name} [{action}]']
    lines += ['fov 90','sensitivity 3','hudgun 0','audio 0','soundvol 0','musicvol 0','dynshadow 0','stencilshadow 0','waterreflect 0','hideradar 1','hideigraphs 1','hidecompass 1','hideteam 1','autodownload 0']
    # command.cpp::scriptcontext/isolatecontext/sealcontexts; no generic exec in MAPCFG.
    for command in ('texture','texturereset','mapmodelreset','mapsoundreset','fog','fogcolour'):
        lines.append('scriptcontext MAPCFG '+command)
    lines += ['isolatecontext MAPCFG','isolatecontext MDLCFG','sealcontexts','']
    return '\n'.join(lines).encode('utf-8')


def map_config():
    return (COMMENT + '\n'.join(['mapmodelreset','mapsoundreset','texturereset',
        'texture 0 "outbreak/ceiling.png"',  # reserved slot 0; geometry never uses sky slot
        'texture 0 "outbreak/ground.png"',   # reserved liquid slot; water is below floor
        'texture 0 "outbreak/wall.png"',
        'texture 0 "outbreak/ground.png"',
        'texture 0 "outbreak/ceiling.png"',
        'fog 256','fogcolour 0x18232B',''])).encode('utf-8')


def uint(value):
    output=bytearray()
    while value>=128:
        output.append((value&127)|128)
        value >>=7
    output.append(value)
    return bytes(output)


def cells():
    result=[]
    for y in range(64):
        for x in range(64):
            solid=not (8<=x<56 and 8<=y<56)
            building=26<=x<38 and 24<=y<40
            inner=28<=x<36 and 26<=y<38
            doorway=30<=y<34 and (26<=x<28 or 36<=x<38)
            if building and not inner and not doorway:
                solid=True
            if solid:
                result.append(bytes((0,2,0)))
            else:
                result.append(bytes((4,0,8 if building else 12,2,3,4,0,2,0)))
    return result


def rle(blocks):
    output=bytearray()
    previous=None
    repeats=0
    def flush():
        nonlocal repeats
        while repeats:
            count=min(255,repeats)
            output.extend((255,count))
            repeats-=count
    for block in blocks:
        if block==previous:
            repeats+=1
        else:
            flush()
            output.extend(block)
        previous=block
    flush()
    return bytes(output)


def map_bytes():
    # world.h::header, worldio.cpp::save_world/rlencodecubes; no stock bytes.
    starts=[(16,32,5,900,100),(48,32,5,2700,100),(16,16,5,900,0),(48,48,5,2700,1)]
    entities=[struct.pack('<4h4Bh bB',x,y,z,yaw,2,team,0,0,0,0,0) for x,y,z,yaw,team in starts]
    # Native persistent_entity is exactly 16 bytes. Lights follow starts, like save_world's sort.
    for x,y in ((16,16),(48,16),(16,48),(48,48),(32,32)):
        entities.append(struct.pack('<4h4Bh bB',x,y,6 if (x,y)==(32,32) else 10,24,1,220,0,0,0,0,0))
    mapinfo=b'MIT\0Copyright 2026 Outbreak contributors; see LICENSE.txt\0'
    extra=uint(len(mapinfo))+uint(65)+mapinfo  # HX_MAPINFO | HX_FLAG_PERSIST
    header=bytearray(980)
    struct.pack_into('<4s4i',header,0,b'ACMP',10,980+len(extra),6,len(entities))
    title=b'Outbreak original browser courtyard proof'
    header[20:20+len(title)]=title
    header[148:916]=bytes(range(256))*3
    struct.pack_into('<i4B4i',header,916,-10000,40,80,100,255,1,80,0,0)
    raw=bytes(header)+extra+b''.join(entities)+rle(cells())
    compressor=zlib.compressobj(9,zlib.DEFLATED,-15)
    body=compressor.compress(raw)+compressor.flush()
    # Explicit deterministic gzip header (mtime=0, OS=255), footer validates CRC/length.
    return b'\x1f\x8b\x08\x00\0\0\0\0\x02\xff'+body+struct.pack('<II',binascii.crc32(raw)&0xffffffff,len(raw))


def file_set():
    files={}
    def add(name,data,reason):
        files[name]=(data,reason)
    add('LICENSE.txt',NOTICE.encode('utf-8'),'Per-original-file MIT notice, scope limited to this declared pack')
    add('config/LICENSE.txt',NOTICE.encode('utf-8'),'Notice pointer compatible with existing config/packages inventory confinement')
    add('config/font.cfg',font_config(),'rendertext.cpp::newfont/fontchar/fontskip; independent hand-drawn stroke atlas')
    add('config/browser.cfg',browser_config(),'D005 canonical minimal offline-map settings, bindings and explicit map command context')
    cfg=map_config()
    add('config/default_map_settings.cfg',cfg,'worldio.cpp::load_world external/default config branch; authored minimal texture slots')
    add(f'packages/maps/{MAP_NAME}.cfg',cfg,'D005 canonical original external map config')
    add(f'packages/maps/{MAP_NAME}.cgz',map_bytes(),'Native v10 header, original persistent entities and SOLID/SPACE RLE')
    add(f'packages/maps/{MAP_NAME}.cgz.LICENSE.txt',NOTICE.encode('utf-8'),'Explicit per-original-map notice; HX_MAPINFO also identifies MIT')
    add('packages/outbreak/font.png',atlas(),'Original glyphs.py stroke grids, 2x nearest-neighbor rasterization')
    fallback=png(64,64,lambda x,y:(240,55,170,255) if (x//8+y//8)%2 else (24,30,38,255))
    add('packages/outbreak/fallback.png',fallback,'D005 canonical generated diagnostic checker fallback')
    for name,color in (('ground',(67,99,87)),('wall',(147,115,80)),('ceiling',(73,89,112))):
        def tile(x,y,color=color):
            change=-22 if x%16==0 or y%16==0 else ((x*7+y*3)%7)-3
            return tuple(max(0,min(255,c+change)) for c in color)+(255,)
        add(f'packages/textures/outbreak/{name}.png',png(64,64,tile),'Original procedural grid tile referenced by authored map texture commands')
    sky=png(64,64,lambda x,y:(56,78,104,255))
    for side in ('lf','rt','ft','bk','dn','up'):
        add(f'packages/textures/skymaps/_{side}.jpg',sky,'texture.cpp::loadskymap with empty loadsky; required by T028 reload path; original solid-color PNG, legacy .jpg filename, no JPEG pixels/decoder needed by inspected IMG detection')
    add('packages/misc/startscreen.png',png(128,128,lambda x,y:(22+(x//16)%2*8,40+(y//16)%2*8,56,255)),'renderhud.cpp::loadingscreen literal; original abstract grid, no inherited logo')
    add('packages/misc/icon.png',fallback,'main.cpp non-Apple SDL window icon literal; original fallback pixels')
    add('packages/misc/com.png',png(64,64,lambda x,y:(100,220,240,255 if 600<((2*x-63)**2+(2*y-63)**2)<1200 else 0)),'rendergl.cpp::renderaboveheadicon literal; original ring placeholder')
    # Proven fixed core aliases; these are independently rendered pixels, not copied media.
    for name in ('base.png','smoke.png','explosion.png','bullethole.png','blood.png','scorch.png','muzzleflash.jpg'):
        def radial(x,y,name=name):
            d=(2*x-63)**2+(2*y-63)**2
            alpha=max(0,255-d//12)
            color=(250,180,60) if name in ('explosion.png','muzzleflash.jpg') else (235,235,235)
            return color+(alpha,)
        add('packages/misc/'+name,png(64,64,radial),'renderparticles.cpp::particleinit literal; original radial neutral placeholder; PNG signature even for legacy .jpg name')
    for name,source in (('items.png','drawequipicon'),('radaricons.png','drawradaricon'),('ctficons.png','drawctficon'),('htficons.png','drawctficon'),('ktficons.png','drawctficon'),('voteicons.png','drawvoteicon'),('teamicons.png','drawteamicons'),('damage.png','drawdamagescreen'),('compass-base.png','drawradar_showmap'),('compass-rose.png','drawradar_showmap'),('scope.png','drawscope')):
        def icon(x,y):
            cellx,celly=x%16,y%16
            mark=cellx in (6,7,8,9) or celly in (6,7,8,9)
            return (80+(x//16)*40,100+(y//16)*30,210,230 if mark else 0)
        add('packages/misc/'+name,png(64,64,icon),'renderhud.cpp::'+source+' literal; original neutral cross/grid placeholder, not final iconography')
    add('packages/crosshairs/default.png',png(64,64,lambda x,y:(240,250,255,255 if (30<=x<=33 and 21<=y<=42 or 30<=y<=33 and 21<=x<=42) else 0)),'renderhud.cpp::loadcrosshair default literal, original procedural cross')
    return files


def generate(root):
    root=Path(root)
    if root.is_symlink():
        raise ValueError('pack root must not be a symlink')
    root=root.resolve()
    files=file_set()
    if root.exists():
        actual={p.relative_to(root).as_posix() for p in root.rglob('*') if p.is_file() or p.is_symlink()}
        if actual-set(files):
            raise ValueError('undeclared existing files in pack root: '+','.join(sorted(actual-set(files))))
    for name in sorted(files):
        destination=root/name
        if any(parent.is_symlink() for parent in (destination,*destination.parents)):
            raise ValueError('symlink in pack output: '+name)
    entries=[]
    for name,(data,reason) in sorted(files.items()):
        path=root/name
        path.parent.mkdir(parents=True,exist_ok=True)
        path.write_bytes(data)
        entry=dict(path=name,virtual_path='/outbreak/'+name,bytes=len(data),sha256=hashlib.sha256(data).hexdigest(),provenance=reason,license='MIT',notice='LICENSE.txt',original=True)
        if name.endswith(('.png','.jpg')):
            entry['encoded_format']='PNG'
        entries.append(entry)
    return dict(schema_version=1,profile='offline-map-original',map_name=MAP_NAME,entries=entries,raw_bytes=sum(e['bytes'] for e in entries),runtime_verified=False,shared_build_ready=False,omitted_optional_features=['weapon and character models','audio/music','bots','native menus/docs/autostarts','public networking/auth/download services','inline igraph directory/icons (hideigraphs=1)' ],dimensions=dict(world=[64,64],courtyard_bounds=[8,8,56,56],courtyard_size=[48,48],building_bounds=[26,24,38,40],building_size=[12,16],interior_bounds=[28,26,36,38],interior_size=[8,12],floor_z=0,exterior_ceiling_z=12,interior_ceiling_z=8,door_width=4,wall_thickness=2,player_radius=1.1,spawn_eye_z=5),provided_fonts=['default','mono','huddigits','serverquality','bargraphs','radaricons'])


def font_preview():
    lines=['OUTBREAK BROWSER PROOF','WASD MOVE  SPACE JUMP','0123456789  Aa Zz !?']
    def pixel(x,y):
        row=(y-20)//28
        column=(x-20)//14
        gx=((x-20)%14-2)//2
        gy=((y-20)%28-2)//2
        on=False
        if 0<=row<len(lines) and 0<=column<len(lines[row]):
            char=lines[row][column]
            on=char!=' ' and 0<=gx<5 and 0<=gy<7 and glyph(char)[gy][gx]=='1'
        return (240,250,255,255) if on else (18,30,42,255)
    return png(512,128,pixel)


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.parse_args()
    manifest=generate(HERE/'pack-root')
    (HERE/'manifest.json').write_text(canonical(manifest),encoding='utf-8')
    (HERE/'font-preview.png').write_bytes(font_preview())
    print(f'Generated {len(manifest["entries"])} original files; {manifest["raw_bytes"]} raw bytes; runtime_verified=false')
    return 0


if __name__=='__main__':
    sys.exit(main())
