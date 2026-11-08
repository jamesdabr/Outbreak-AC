"""T080 data construction only; stdlib, no old generators or runtime imports."""
import binascii
import hashlib
import json
from pathlib import Path
import struct
import zlib

HERE=Path(__file__).resolve().parent
ROOT=HERE.parents[2]
NAME='blackwood_greybox_v1'
PROFILE='BLACKWOOD_GREYBOX_CANDIDATE_DATA'
COORD='Q10_FOOT_EAST_NORTH_UP'
PLAN='notes/proposals/T076-world-blackwood-plan.md'
REPORT='web/world/reviews/T076/measurements-2.json'
PINS={PLAN:'44f272bfb2f50b44bece0601153627c161c79405dbc44f1131b3477789cd5b51',
      REPORT:'33b29fc02f340a62b7aa6fce6d74574f735dd1a95a51c658c0b870270c3be9e3',
      'MVP/BLACKWOOD_DATA_FOUNDATION.md':'b194cc675978c21df6e88c071bc72c9c99c82fcf50e1e48c08fae05f77d12221',
      'web/assets/network-profile/manifest.json':'c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7',
      'web/assets/network-profile/pack-root/packages/maps/dev_outbreak_browser.cfg':'751937b8c2d1082281643895be6ffbe2c4de22f072012601bbd01361ce0e37de',
      'web/assets/network-profile/pack-root/LICENSE.txt':'93ca3c5ce03804b3e63ea54286b4576269fcb9d943bda87acda9383a8bb8ca4e',
      'source/src/physics.cpp':'bc74c8cfdb39df5e5a5488b69cfaab307e5d064b08d54f581769dfab00d61f5b',
      'source/src/clientgame.cpp':'6f394da0969de59ab1bfc26c3ca6e535b8e7126457e2dc039676aa5abdcbd6b9'}
LIMITS=['CANDIDATE_NOT_BALANCE_ACCEPTED','NO_RUNTIME_CAPSULE_NAV_OR_GAMEPLAY_PROOF',
        'LEGACY_STARTS_ARE_NOT_CANONICAL_SQUAD_SLOTS','NO_RESOURCE_OR_ACTOR_GRANTS']
AIMS=[45,90,135,180,225,270,315,0]
LIGHTS=[(20,40),(64,36),(108,40),(40,64),(64,64),(88,64),(20,88),(64,92),(108,88),
        (56,56),(72,56),(56,72),(72,72)]
CGZ='packages/maps/'+NAME+'.cgz'
CFG='packages/maps/'+NAME+'.cfg'
ANCHORS='packages/outbreak/'+NAME+'.anchors.json'
MEMBERS={CGZ,CFG,ANCHORS,'LICENSE.txt','PROVENANCE.json'}
ENTITY=struct.Struct('<hhhhBBBBhbB')
GZIP=bytes.fromhex('1f8b08000000000002ff')


def require(ok,why):
    if not ok:raise ValueError(why)
def sha(data):return hashlib.sha256(data).hexdigest()
def canonical(value):return json.dumps(value,indent=2,sort_keys=True)+'\n'
def regular(path):
    path=Path(path).absolute()
    require('..' not in path.parts and not any(p.is_symlink() for p in (path,*path.parents)),'symlink/escaping path')
    return path
def confined(root,name):
    p=Path(name)
    require(bool(p.parts) and not p.is_absolute() and str(p)==name and '..' not in p.parts and '\\' not in name and ':' not in name,'unsafe member')
    return regular(regular(root)/p)
def files(root):
    root=regular(root);result={}
    for p in root.rglob('*'):
        regular(p)
        if p.is_file():result[str(p.relative_to(root))]=p.read_bytes()
    return result
def q(value):
    scaled=value*1024
    require(type(value) in (int,float) and scaled==int(scaled),'inexact Q10; rounding forbidden')
    return int(scaled)
def pos(xy):return [q(xy[0]),q(xy[1]),0]


def inputs():
    for name,pin in PINS.items():require(sha(regular(ROOT/name).read_bytes())==pin,'source pin changed: '+name)
    report=json.loads((ROOT/REPORT).read_text())['proposal']
    require(report['iteration']==2 and report['world']==[128,128],'final report identity')
    material_manifest=json.loads((ROOT/'web/assets/network-profile/manifest.json').read_text())
    materials={}
    for name in ('ceiling','ground','wall'):
        key='packages/textures/outbreak/'+name+'.png'
        e=next(e for e in material_manifest['entries'] if e['path']==key)
        path=regular(ROOT/'web/assets/network-profile/pack-root'/key)
        require(sha(path.read_bytes())==e['sha256'] and e['license']=='MIT','original texture pin/license')
        materials[key]=e['sha256']
    return report,materials


def sidecar(p):
    result=dict(schema_version=1,profile=PROFILE,map_name=NAME,map_revision=1,coordinate_system=COORD,
                source_plan_sha256=PINS[PLAN],source_report_sha256=PINS[REPORT])
    bounds=[(8,8,64,64),(64,8,120,64),(8,64,64,120),(64,64,120,120)]
    result['regions']=[dict(id='BW-R%02d'%i,bounds_q10=list(map(q,b))) for i,b in enumerate(bounds)]
    result['deployment_clusters']=[]
    for i,((x,y),aim) in enumerate(zip(p['cluster_centers'],AIMS)):
        ident='BW-D%02d'%i
        result['deployment_clusters'].append(dict(id=ident,center_q10=pos((x,y)),aim_cdeg_from_east=aim*100,
            slots=[dict(id=ident+'-S%d'%n,position_q10=pos((x+dx,y+dy))) for n,(dx,dy) in enumerate(p['slot_offsets'])]))
    kinds=['ammo_pistol','ammo_rifle','medical','wood','ammo_pistol','wood','medical','wood']
    result['loot']=[dict(id='BW-L%02d'%(i+1),position_q10=pos(xy),kind=kinds[i%8]) for i,xy in enumerate(p['loot_xy'])]
    result['barricades']=[dict(id='BW-B%02d'%(i+1),position_q10=pos(a[:2]),axis=a[2]) for i,a in enumerate(p['barricades'])]
    for key,source,prefix in [('walkers','infected_xy','BW-I'),('reinforcements','reinforcement_xy','BW-RI'),('predators','predator_xy','BW-P')]:
        result[key]=[dict(id=prefix+'%02d'%(i+1),position_q10=pos(xy)) for i,xy in enumerate(p[source])]
    result['portals']=[dict(id='BW-V01',position_q10=pos((51,66))),dict(id='BW-V02',position_q10=pos((77,62)))]
    result['extraction']=dict(id='BW-E01',position_q10=pos((64,90)),bounds_q10=list(map(q,(58,86,0,70,94,6))))
    result['reserved_corridors']=[dict(id='BW-X%02d'%(i+1),bounds_q10=list(map(q,b))) for i,b in enumerate(p['reserved_corridors'])]
    result['limitations']=LIMITS
    return result


def cell(p,x,y):
    rects=p['geometry_rectangles']['screens']+p['geometry_rectangles']['building']
    solid=not (8<=x<120 and 8<=y<120) or any(a<=x<c and b<=y<d for a,b,c,d in rects)
    return (0,0,0) if solid else (4,0,12 if 50<=x<78 and 50<=y<78 else 16)


def gzip(raw):
    c=zlib.compressobj(9,zlib.DEFLATED,-15)
    return GZIP+c.compress(raw)+c.flush()+struct.pack('<II',binascii.crc32(raw)&0xffffffff,len(raw))


def map_bytes(p):
    info=b'MIT\0Copyright 2026 Outbreak contributors; T080 candidate only; see LICENSE.txt\0'
    require(len(info)<128,'mapinfo bound')
    extra=bytes((len(info),65))+info
    header=bytearray(980)
    struct.pack_into('<4s4i',header,0,b'ACMP',10,980+len(extra),7,8+len(LIGHTS))
    title=b'Blackwood original greybox candidate DATA'
    header[20:20+len(title)]=title
    header[148:916]=bytes(range(256))*3
    struct.pack_into('<i4B4i',header,916,-10000,40,80,100,255,1,80,0,0)
    ents=[ENTITY.pack(x,y,5,((aim+90)%360)*10,2,100,0,0,0,0,0) for (x,y),aim in zip(p['cluster_centers'],AIMS)]
    ents += [ENTITY.pack(x,y,10,24,1,220,0,0,0,0,0) for x,y in LIGHTS]
    blocks=[]
    for y in range(128):
        for x in range(128):
            kind,floor,ceil=cell(p,x,y)
            blocks.append(bytes((0,2,0)) if kind==0 else struct.pack('<Bbb6B',4,floor,ceil,2,3,4,0,2,0))
    rle=bytearray();previous=None;n=0
    def flush():
        nonlocal n
        while n:r=min(n,255);rle.extend((255,r));n-=r
    for b in blocks:
        if b==previous:n+=1
        else:flush();rle.extend(b);previous=b
    flush()
    return gzip(bytes(header)+extra+b''.join(ents)+rle)


def license_bytes():
    old=(ROOT/'web/assets/network-profile/pack-root/LICENSE.txt').read_text()
    body=old.split('This notice applies only',1)[0]
    return (body+'This notice applies only to the newly authored T080 Blackwood candidate data,\n'
            'generator, validator and tests. It does not replace or relicense upstream\n'
            'engine code, stock assets or separately licensed dependencies.\n').encode()


def payloads():
    p,materials=inputs()
    license=license_bytes()
    template=(ROOT/'web/assets/network-profile/pack-root/packages/maps/dev_outbreak_browser.cfg').read_bytes()
    body=b'mapmodelreset\n'+template.split(b'\nmapmodelreset\n',1)[1]
    config=b''.join(b'// '+line+b'\n' for line in license.splitlines())+b'\n// T080 candidate; original texture dependencies require later assembly.\n'+body
    generators={name:sha(regular(HERE/name).read_bytes()) for name in ('candidate.py','generate.py','validate.py')}
    provenance=dict(schema_version=1,profile=PROFILE,scope='NEW_ORIGINAL_DATA_ONLY_NOT_RUNTIME_OR_STOCK_RELICENSE',
                    source_files=PINS,generator_files=generators,materials=materials,config_body_sha256=sha(body),
                    geometry_origin='exact pinned T076 iteration2 static rectangles; no placed wood',
                    lights=dict(xy=LIGHTS,z=10,radius=24,white_intensity=220,other_attrs=0,
                                origin='new deterministic13-point layout, original proof white220 palette'),
                    legacy_starts=dict(count=8,z=5,kind=2,attr2=100,yaw='((canonical_degrees_from_east+90)%360)*10'),
                    canonical_slots=dict(count=32,origin='exact report offsets, foot0 Q10, not native entities'),limitations=LIMITS)
    return {CGZ:map_bytes(p),CFG:config,ANCHORS:canonical(sidecar(p)).encode(),
            'LICENSE.txt':license,'PROVENANCE.json':canonical(provenance).encode()}


def manifest(payload):
    return dict(schema_version=1,profile=PROFILE,map_name=NAME,map_revision=1,coordinate_system=COORD,
                source_plan_sha256=PINS[PLAN],source_report_sha256=PINS[REPORT],
                entries=[dict(path=n,bytes=len(b),sha256=sha(b),license='MIT',notice='LICENSE.txt') for n,b in sorted(payload.items())],
                native_decoder=False,runtime=False,overlay=False)


def build(root):
    root=regular(root);require(not root.exists(),'new absent candidate output root required')
    data=payloads();require(set(data)==MEMBERS,'five candidate members')
    for n in data:confined(root,n)
    for n,b in data.items():
        p=confined(root,n);p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(b)
    return manifest(data)
