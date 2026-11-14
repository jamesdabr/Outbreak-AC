"""T164 fixed Blackwood pipeline. Import performs no host observation or effects.
Inspected baseline copying is documented in tests/preparation-1/baseline.json.
No historical project module is imported.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import time
from html.parser import HTMLParser

FIXED_CONFIG={'sdk_root': '/private/tmp/outbreak-web-sdk', 'sdk_version': '7.0.0', 'compiler_revision': '777e6e5db7b4990bcaeb1b9998ed642cc84e6629', 'common_cxx': ['--target=wasm32-unknown-emscripten', '-std=gnu++11', '-fsigned-char', '-O2', '-DOUTBREAK_NETWORK_CLIENT', '-DOUTBREAK_BLACKWOOD_CLIENT'], 'common_c': ['--target=wasm32-unknown-emscripten', '-O2', '-DHAS_SOCKLEN_T=1', '-std=gnu11', '-fsigned-char', '-DOUTBREAK_NETWORK_CLIENT'], 'ports': ['-sUSE_SDL=2', '-sUSE_SDL_IMAGE=2', '-sSDL2_IMAGE_FORMATS=["png"]', '-sUSE_ZLIB=1', '-sUSE_VORBIS=1'], 'link': ['-O2', '-lopenal', '-sLEGACY_GL_EMULATION=1', '-sGL_UNSAFE_OPTS=0', '-sALLOW_MEMORY_GROWTH=1', '-sINITIAL_MEMORY=67108864', '-sSTACK_SIZE=2097152'], 'libpng_sha512': 'e14302d87864432d747896e3944a6416d4b5f3059f538cfe615ddbe1d0084d4a02d4df3ef2761b02c839858625bed57d873198792c3583029c619e1cf8c4561b', 'schema_version': 1, 'recipe': 'blackwood_network_v1', 'profile': 'BLACKWOOD_NETWORK_CLIENT', 'manifest': 'web/assets/blackwood-profile/manifest.json', 'pack_root': 'web/assets/blackwood-profile/pack-root', 'js_library': 'web/transport/enet_websocket.js', 'shell': 'web/build/blackwood/shell.html', 'map': {'name': 'blackwood_greybox_v1', 'revision': 1, 'cgz_bytes': 734, 'cgz_sha256': 'e68314e911130d2822fdfa65d77dfaba302d4f5c3552ff91c698b84768d5ddf1', 'cfg_sha256': '289bcb22b29a17443cdf47a936e82edbc47a7a0e0dd034a8b602ce3ec79b76bd'}}
ACCEPTANCE_PINS={'notes/decisions/D223-T163-source-helper-acceptance.md': '1e1f3f748188190e2524451bfe38aae89d58a4aaa195f9afe3b46e058da69af1', 'notes/handoffs/T163-engine-final-freeze-1.md': '38a6f1ad28400cd7436ba09e48b7a60d37529971d84f0fb0b0b580365a0b44d7', 'notes/reviews/MAIN-T163-final-freeze-review-1.json': 'b26493bb41564a65ef9884f325cc10838ffa02cf124fe34006240882e891a7f9'}
NOTICE_PINS={'notices/assaultcube-source.txt': '8db297aeedc74a8d527a024f6ab4edda72a76686301b39d43142334cad18f153', 'notices/cube-bots.txt': '9850cd946fd360a99146ed268f8e2fd2f7b037df8af3f4b20944358110454cb3', 'notices/cube-source.txt': 'daa94f50008388c7d1b89d745427757cf325b0518a9ddcebcef8e84b6a0c0158', 'notices/emscripten.txt': '620a78084fc7ca97c0b5dea9abf891f3ffcadfdbf305276f099c9c4e12fc1d86', 'notices/enet.txt': 'e603f2f9d22b0c13e50c6568505c81c8466c9ce3b1041f6cebc9b11406d6b165', 'notices/libpng.txt': 'bdb0a645ea18c60507d0368379b1ac5474b92255fcc2d115e07486a7672ba526', 'notices/ogg.txt': 'd2ab5758336489da61c12cc5bb757da5339c4ae9001f9bb0562b4370249af814', 'notices/provenance.json': 'ce91e13c375ca54eb9663a78158cc165db9bed21ca7e54ecc8d4af499b0e06b0', 'notices/sdl2-image.txt': '28aabfed22b3cb0b7e23ef40385e4f66297c960082f029c96d073cc1d4e008d5', 'notices/sdl2.txt': '97f35b302b361680ec1e891e95d2d52097bb95abff361434916d99dc1305f127', 'notices/vorbis.txt': 'ec1815db59fcd302846df949d7424876cb2e2dc5ed1606c5fb0b36787b1cf43a', 'notices/zlib.txt': 'e32ff4e00d9d94930537635291da39e7e612703334bf6fde8c7f1686fe8a45a2'}
PORT_SPECS=[{'name': 'sdl2', 'expected_sha512': '001738b610b42a8f8badfd6af3402f0a1a8601034adef0b8c702dd2b1951dc1b71b733a6779d97499b6f7314d226ec0c8dcffeb753f35a5c51e995ca20bdd459', 'recipe_sha256': 'bc65bfb4e63e10f5b879ad798baf10a2ce683cd7095a7da40d049dfad308462e'}, {'name': 'sdl2_image', 'expected_sha512': '2175d11a90211871f2289c8d57b31fe830e4b46af7361925c2c30cd521c1c677d2ee244feb682b6d3909cf085129255934751848fc81b480ea410952d990ffe0', 'recipe_sha256': 'ee548172c3d5772413e189f008269669c246f831fcfd4a6011269ac30e9239a4'}, {'name': 'zlib', 'expected_sha512': '16fea4df307a68cf0035858abe2fd550250618a97590e202037acd18a666f57afc10f8836cbbd472d54a0e76539d0e558cb26f059d53de52ff90634bbf4f47d4', 'recipe_sha256': '2e744c843aecb320cbc005abb980d0cc264cf87791db25624d17dcd712a9c411'}, {'name': 'vorbis', 'expected_sha512': '10edd193f44f2b2d6085672e257b5be11066f5db27348d4cab53789bf9e8739c2df2cd7f42b83e4edbab53e10b5dc84320d6aab1deac0d8e18196a8a88b19b77', 'recipe_sha256': '1c1f178d3abd296f67ed476b6ac8cd404bccaac4f6574adbb3b823a1e3f85d94'}, {'name': 'ogg', 'expected_sha512': 'e7b5f5d469090b66dbb33634591ae6de41af3a5644c10488e59ba7428ed78912e208a2c0fbb5003ec5b7eb2a0102a2f85cecb21fa9512d790139ecc45b6d03f4', 'recipe_sha256': '4a3c90b5882b07e5bb868ce0e98ed34445002e9d3c0d04ae9fbc6233bb0a2bcf'}, {'name': 'libpng', 'expected_sha512': 'e14302d87864432d747896e3944a6416d4b5f3059f538cfe615ddbe1d0084d4a02d4df3ef2761b02c839858625bed57d873198792c3583029c619e1cf8c4561b', 'recipe_sha256': '3dc04566b3e646400f7b180ff3cc5d539146008e3b416bcb3e2e34fe53189911'}]
ASSEMBLY_PROVENANCE_SHA='48b1bbd659fa0193bce88a8d76a9146fa8e84bc981f20c4203c133e26b64b3c3'

SOURCE_MANIFEST='web/repro/blackwood-source-manifest.json'
SDK='/private/tmp/outbreak-web-sdk'
ADAPTER_DECISION=('notes/decisions/D235-Darwin-nonreaping-wait-adapter.md', '7bc53264af09893e0ec9a8df8a848abae36a89e978acca268e045b712cd5d156')
PROFILE='BLACKWOOD_ASSET_ASSEMBLY_CANDIDATE_DATA'
RECIPE='blackwood_network_v1'
STATUS='LINKED_NOT_BROWSER_VERIFIED'
CLAIMS=dict(runtime=False,audio=False,model=False,multiplayer=False,authority=False,P0=False)
MAX_JSON=32*1024*1024
MAX_LOG=8*1024*1024
UNRESOLVED_HANDLES=[]  # Strong ownership until process exit; never an implicit retry/grace.
SUPERVISOR_RESERVE=16384
SUPERVISOR_FRAME=b'\nBLACKWOOD_COMMAND_SUPERVISOR_V1\n'
CTYPES_INPUTS={'/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/ctypes/__init__.py': '608671c6b49e5e027e3348fcf492718c33f69f919d99f4ff170522c40bd4c550', '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/ctypes/_endian.py': '38dc998ee2d180a64d4fe561b79287b19850df405f48fe72dede7a65d71de844', '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/struct.py': '9c231f9497caf513a22dee8f790b07f969b0e45854a0bdd6dd84b492e08c2856', '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/lib-dynload/_ctypes.cpython-311-darwin.so': 'e5ed138ab1322322bce3dad9d7f9e5bff60ac79cfe09b340a89593ffe3b3add9', '/Library/Frameworks/Python.framework/Versions/3.11/lib/python3.11/lib-dynload/_struct.cpython-311-darwin.so': '9f978a4bc70a3c6ca10c53a1d1d96b52e0dad40f39176e615c0ab5fa58f68f7a'}
DARWIN_WAIT_HEADERS={'/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/wait.h': 'b77f7dd6f592eba8b0d51c15c7b975472fdad50c12ea296f74f062cbf98dcbf7', '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/signal.h': '171af7545ef750627aeba02c1de838c05e2cf396e2f49881ea74dba6990c44a3', '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/_types/_pid_t.h': '052a6dbbec8e30623c2d33dd373992f6c5d0c57c57ed4949d2b48c4ab0976487', '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/_types/_id_t.h': 'fb7255c9872e2a805c206796326e21d47146e22c93c09752126d7166bdaba5e5', '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/_types/_uid_t.h': 'd2140a65a17943a857381757c0b73a920f35ade41dc9809437c168be457c276a', '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/sys/_types.h': '863c4f07045775002b63b7e616742d9f746e4a02da4441442d8fe1138bbd0ff9', '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/machine/_types.h': 'f27264f8fdec9f164b4fc2b556f666ed7c5c0e5b88fd9f23db0b731ffa6cf864', '/Library/Developer/CommandLineTools/SDKs/MacOSX15.5.sdk/usr/include/arm/_types.h': '4f0bde85f9a41cc7d30fff22ebd7e8f4eb206a55a926eda012a2e7481e3524fa'}
MAGIC=b'\0asm\1\0\0\0'
ARTIFACTS=('index.html','index.js','index.wasm','index.data')
OWN_FILES=('recipe.py','build.py','verify.py','config.json','shell.html','SCHEMA.md','README.md','test_recipe.py')
CPP_NAMES='crypto audiomanager autodownload client clientgame clients2c command console docs editing entities http log main menus oggstream openal packetqueue physics protocol rendercubes rendergl renderhud rendermodel renderparticles rendertext rndmap scoreboard serverms server serverbrowser shadow soundlocation soundscheduler stream texture tools water weapon wizard world worldio worldlight worldocull worldrender zip bot/bot bot/botmanager bot/bot_ai bot/bot_util bot/bot_waypoint bot/ac_bot bot/ac_bot_ai'.split()
UNITS=tuple('source/src/'+n+'.cpp' for n in CPP_NAMES)+tuple('source/enet/'+n+'.c' for n in ('callbacks','compress','host','list','packet','peer','protocol'))+('web/transport/enet_websocket.c',)
SOURCE_PINS={'source/src/browser_map_profile.h':'614fe93545ea52a4857d7674aae9b92452ba36cac35d952754ca218488aea414','source/src/main.cpp':'1da216b25233639eaaa1f89fb15a6cdbdd6ad3ab90e19989a44ffc77952a07ac','source/src/client.cpp':'0e3be12c5771eb20f4dfb9dbfe5cd239b49a02998d267a0df6b407280fb31b56','source/src/clients2c.cpp':'5368d23331123aa67de430b7c11460efdb5182944b9508f715491b7c6522a4bd'}
MANIFEST_PINS={'web/assets/blackwood-profile/manifest.json':'8c4f7eef5f0deafb06bec60d62be529a684a30d56bbdc6dc3e5f38dd21c69e60','web/assets/network-profile/manifest.json':'c9ecfa62f7e4ca7111a9d3a23a9c97b906d11399d32f6f312463c6697a3359d7','web/assets/blackwood-candidate/manifest.json':'fa3049408e3ed0dbf2d4bc422b45c166b7fc0e0ac5d2fec4c8c5aadd53ae9711'}
LIMITATIONS=['CANDIDATE_NOT_BALANCE_ACCEPTED','NO_RUNTIME_CAPSULE_NAV_OR_GAMEPLAY_PROOF','LEGACY_STARTS_ARE_NOT_CANONICAL_SQUAD_SLOTS','NO_RESOURCE_OR_ACTOR_GRANTS']
ALIAS_PINS={'notes/decisions/D044-approved-sdk-aliases.json':'7b78d4f0ce74b2e1f24459429409ba9e0350e52902b3b600f07c936b5684154f','notes/decisions/D046-html-minifier-alias.json':'3ff2a582732afcda98ef07a43384146f93dc39b22c84dbe16e91ca7ca702f01c'}
ALIAS_TEXT={SDK+'/upstream/bin/clang':'clang-24',SDK+'/upstream/bin/clang++':'clang',SDK+'/upstream/bin/wasm-ld':'lld',SDK+'/upstream/bin/llvm-ranlib':'llvm-ar',SDK+'/upstream/emscripten/node_modules/.bin/html-minifier-terser':'../html-minifier-terser/cli.js'}
LAUNCHERS=frozenset(('/usr/bin/clang','/usr/bin/clang++','/usr/bin/otool'))
HISTORICAL_ROOT='/Users/jd1/code/apps/outbreak'
HISTORICAL_PREFIX=HISTORICAL_ROOT+'/web/repro/tests/prerequisites/'
HISTORICAL_FIFOS=tuple(HISTORICAL_PREFIX+n+'/repo/web/build/.cache/bad' for n in (
 'FIXTURE_ONLY-1k__01pl','FIXTURE_ONLY-_96_618b','FIXTURE_ONLY-gix5ps6o',
 'FIXTURE_ONLY-ja9bgu83','FIXTURE_ONLY-qdchd7yl','FIXTURE_ONLY-vqodxlzi','T101/FIXTURE_ONLY-yz7bph14'))
HISTORICAL_UNREADABLE=tuple(HISTORICAL_PREFIX+n+'/repo/web/build/.cache/bad-mode' for n in (
 'FIXTURE_ONLY-a6a8xiso','FIXTURE_ONLY-am2d_ogp','FIXTURE_ONLY-gx0ewpha',
 'FIXTURE_ONLY-hghnb9_0','FIXTURE_ONLY-ktpjacgc','FIXTURE_ONLY-wxoxh5ho','T101/FIXTURE_ONLY-_ul9woy_'))
HISTORICAL_SPECIALS=frozenset((*HISTORICAL_FIFOS,*HISTORICAL_UNREADABLE))
OBSERVATION=set('inputs preservation units ports aliases alias_decisions pack tool_errors'.split())
AUTH=set('schema_version kind authority status execution_release recipe ticket candidate_id decision source_revision source_manifest bindings source_acceptance observation'.split())
PLAN=set('schema_version kind status recipe candidate_id source_revision source_manifest source_acceptance observation commands environment claims pending'.split())
COMMAND=set('argv environment exit_code log log_sha256 log_bytes elapsed_ms failure owned_process_reaped'.split())
UNIT=set('source object pre_depfile post_depfile pre_scan compile pre_dependencies post_dependencies object_sha256'.split())
RESULT=set('schema_version kind candidate_id recipe ticket status fixture_only pins source_revision source_manifest source_acceptance observation environment object_reuse claims compiles link syntax wasm_validation error preload_validation notices outputs bundle_id metadata_sha256'.split())

def require(ok,message):
    if not ok:raise ValueError(message[:512])
def canonical(value):return (json.dumps(value,sort_keys=True,indent=2,ensure_ascii=True,allow_nan=False)+'\n').encode()
def digest(data,algorithm='sha256'):return hashlib.new(algorithm,data).hexdigest()
def keys(value,fields,label):require(type(value) is dict and set(value)==set(fields),label+' exact keys')
def equal(a,b):
    if type(a) is not type(b):return False
    if type(a) is dict:return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list:return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b
def integer(v,low=0,high=2**63-1):require(type(v) is int and low<=v<=high,'integer/range');return v
def sha_string(v):require(type(v) is str and re.fullmatch('[0-9a-f]{64}',v),'SHA256');return v
def identifier(v):require(type(v) is str and re.fullmatch('[A-Za-z0-9_-]{1,48}',v),'candidate ID');return v
def revision(v):require(type(v) is str and re.fullmatch('[0-9a-f]{40}',v),'source revision');return v
def relative(v):
    require(type(v) is str and v and not v.startswith('/') and '\\' not in v and all(ord(c)>=32 for c in v),'relative path')
    require(all(p not in ('','.','..') for p in v.split('/')),'relative path components');return v
def absolute(v):
    v=str(v);require(v.startswith('/') and str(PurePosixPath(v))==v and '\\' not in v and all(ord(c)>=32 for c in v),'absolute path')
    require(all(p not in ('.','..') for p in v.split('/')[1:]),'absolute path components');return v
def below(p,root):return p==root or p.startswith(root+'/')
def parse_json(data):
    require(len(data)<=MAX_JSON,'JSON cap')
    def pairs(items):
        d={}
        for k,v in items:require(k not in d,'duplicate JSON key');d[k]=v
        return d
    def bad(_):raise ValueError('noninteger/nonfinite JSON')
    return json.loads(data.decode('utf8'),object_pairs_hook=pairs,parse_float=bad,parse_constant=bad)

def inspect_command_log(data,fixture_only):
    require(len(data)<=MAX_LOG and SUPERVISOR_FRAME in data,'retained command supervisor frame')
    output,encoded=data.rsplit(SUPERVISOR_FRAME,1);state=parse_json(encoded)
    keys(state,'schema_version kind fixture_only pid leader_exit_observed original_handle_reaped exit_code group primary cleanup cleanup_actions child_log_bytes child_log_sha256 hard_deadline_ms work_deadline_ms'.split(),'command supervisor')
    require(encoded==canonical(state) and state['schema_version']==1 and type(state['schema_version']) is int and state['kind']=='BLACKWOOD_COMMAND_SUPERVISOR','canonical supervisor identity')
    require(type(state['fixture_only']) is bool and state['fixture_only']==fixture_only,'supervisor fixture identity')
    integer(state['pid'],2);integer(state['leader_exit_observed'],0,0);integer(state['exit_code'],0,0)
    require(state['original_handle_reaped'] is True and state['primary'] is None and state['cleanup']==[],'successful independent supervisor facts')
    group=state['group'];keys(group,'anchor_acquired anchor_confirmed_before_signal signal_attempted signal_result closure closed permission_observation'.split(),'owned group')
    require(group['anchor_acquired'] is True and group['anchor_confirmed_before_signal'] is True and group['signal_attempted'] is True and group['closed'] is True,'original group anchor/cleanup/closure')
    pair=(group['signal_result'],group['closure']);permission=group['permission_observation']
    deferred=pair==('TERMINAL_EPERM_UNKNOWN','ABSENT_AFTER_TERMINAL_EPERM')
    require(deferred or pair in (('ABSENT_ANCHORED','ABSENT_ANCHORED'),('SENT_ANCHORED','ABSENT_AFTER_ANCHORED_CLEANUP')),'owned group closure evidence')
    if deferred:
        keys(permission,'phase errno pid terminal_exit_code mutating_signal_attempted message resolution'.split(),'terminal permission observation')
        require(permission['phase']=='PRE_REAP_SIGNAL' and integer(permission['errno'],1,1)==1 and integer(permission['pid'],2)==state['pid'] and integer(permission['terminal_exit_code'],0,0)==0 and permission['mutating_signal_attempted'] is True,'terminal permission identity')
        require(type(permission['message']) is str and len(permission['message'])<=240 and permission['resolution']=='POST_REAP_ABSENT','resolved bounded terminal permission observation')
    else:require(permission is None,'normal group permission observation must be null')
    require(state['child_log_bytes']==len(output) and type(state['child_log_bytes']) is int and state['child_log_sha256']==digest(output),'retained child output identity')
    require(len(output)<=MAX_LOG-SUPERVISOR_RESERVE,'child output receipt reserve')
    integer(state['hard_deadline_ms']);integer(state['work_deadline_ms']);require(state['hard_deadline_ms']-state['work_deadline_ms']==5000,'reserved cleanup deadline')
    require(type(state['cleanup_actions']) is list and state['cleanup_actions']==['cached_returncode','confirm_unreaped_anchor','kill_owned_group','wait_original_handle']+(['observe_group_absence'] if group['signal_result'] in ('SENT_ANCHORED','TERMINAL_EPERM_UNKNOWN') else [])+['selector_close','stdin_close','stdout_close','stderr_close'],'exact successful supervisor action ordering')
    return state

def adapter_platform():
    require(sys.platform=='darwin' and sys.byteorder=='little' and os.uname().machine=='arm64','fixed Darwin arm64 LP64 little-endian adapter')

def make_nonreaping_observer():
    # D235: a fixed lazy standard-library bridge, never called at import or
    # through real ctypes in preparation. No general library/PID/flag selector.
    adapter_platform()
    bytecode=sys.dont_write_bytecode;sys.dont_write_bytecode=True
    try:import ctypes  # Future actual backend setup only; fake module in preparation.
    finally:sys.dont_write_bytecode=bytecode
    require(ctypes.sizeof(ctypes.c_int)==4 and ctypes.sizeof(ctypes.c_uint)==4 and ctypes.sizeof(ctypes.c_long)==8 and ctypes.sizeof(ctypes.c_ulong)==8 and ctypes.sizeof(ctypes.c_void_p)==8,'fixed Darwin scalar widths')
    require(ctypes.c_int(-1).value==-1 and ctypes.c_uint(-1).value==0xffffffff and ctypes.c_ulong(-1).value==0xffffffffffffffff,'fixed Darwin scalar signedness')
    class Sigval(ctypes.Union):
        _fields_=[('sival_int',ctypes.c_int),('sival_ptr',ctypes.c_void_p)]
    class Siginfo(ctypes.Structure):
        _fields_=[('si_signo',ctypes.c_int),('si_errno',ctypes.c_int),('si_code',ctypes.c_int),('si_pid',ctypes.c_int),('si_uid',ctypes.c_uint),('si_status',ctypes.c_int),('si_addr',ctypes.c_void_p),('si_value',Sigval),('si_band',ctypes.c_long),('si_pad',ctypes.c_ulong*7)]
    require(ctypes.sizeof(Sigval)==8 and ctypes.alignment(Sigval)==8 and ctypes.sizeof(Siginfo)==104 and ctypes.alignment(Siginfo)==8,'fixed Darwin siginfo size/alignment')
    offsets=dict(si_signo=0,si_errno=4,si_code=8,si_pid=12,si_uid=16,si_status=20,si_addr=24,si_value=32,si_band=40,si_pad=48)
    require(all(getattr(Siginfo,n).offset==offset for n,offset in offsets.items()),'fixed Darwin siginfo field offsets')
    libc=ctypes.CDLL('/usr/lib/libSystem.B.dylib',use_errno=True);waitid=libc.waitid
    waitid.argtypes=[ctypes.c_int,ctypes.c_uint,ctypes.POINTER(Siginfo),ctypes.c_int];waitid.restype=ctypes.c_int
    def observe(pid,deadline):
        integer(pid,2,2**31-1)
        while True:
            require(time.monotonic()<deadline,'nonreaping observation deadline')
            info=Siginfo()  # Zero the complete aligned 104-byte record every call/retry.
            result=waitid(1,pid,ctypes.byref(info),0x25)
            require(time.monotonic()<deadline,'late nonreaping observation')
            require(type(result) is int and result in (-1,0),'unexpected nonreaping return')
            if result==-1:
                error=ctypes.get_errno();integer(error,1,4095)
                if error==4:continue  # EINTR, bounded by the original absolute deadline.
                raise OSError(error,'owned leader nonreaping waitid')
            found=info.si_pid
            if found==0:
                require(all(getattr(info,n)==0 for n in ('si_signo','si_errno','si_code','si_status')),'zero no-event siginfo');return None
            require(found==pid and info.si_signo==signal.SIGCHLD and info.si_errno==0,'owned nonreaping siginfo identity')
            code,status=info.si_code,info.si_status;require(code in (1,2,3),'owned nonreaping terminal code')
            integer(status,0,255)
            return status if code==1 else -integer(status,1,127)
    return observe

class PersistenceRefusal(OSError):
    def __init__(self,receipt):self.receipt=receipt;super().__init__('persistence refused: '+str(receipt))

class FileSystem:
    fixture_only=False
    def __init__(self):self.whole_end=None
    def exists(self,p):return os.path.lexists(absolute(p))
    def stat(self,p):
        s=Path(absolute(p)).lstat()
        return dict(kind='directory' if stat.S_ISDIR(s.st_mode) else ('link' if stat.S_ISLNK(s.st_mode) else ('file' if stat.S_ISREG(s.st_mode) else ('fifo' if stat.S_ISFIFO(s.st_mode) else 'special'))),mode=stat.S_IMODE(s.st_mode),nlink=s.st_nlink,bytes=s.st_size,device=s.st_dev,inode=s.st_ino,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns,identity=(s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns,s.st_nlink))
    def ordinary(self,p,directory=False,launcher=False):
        p=absolute(p)
        for parent in reversed(PurePosixPath(p).parents):require(self.stat(str(parent))['kind']=='directory','ordinary ancestor')
        s=self.stat(p);require(s['kind']==('directory' if directory else 'file'),'ordinary kind')
        if not directory:
            require(p not in HISTORICAL_SPECIALS and s['mode']&0o444,'historical special/unreadable is never consumed')
            require(s['nlink']==1 or (launcher and p in LAUNCHERS and s['nlink']>=1 and s['mode']==0o755),'single-link consumption')
        return s
    def read(self,p,maximum=MAX_JSON):
        s=self.ordinary(p);require(s['bytes']<=maximum,'read cap')
        with open(p,'rb') as f:data=f.read(maximum+1)
        require(len(data)==s['bytes'] and s['identity']==self.ordinary(p)['identity'],'read changed');return data
    def record(self,p,launcher=False):
        s=self.ordinary(p,launcher=launcher);h=hashlib.sha256()
        with open(p,'rb') as f:
            for b in iter(lambda:f.read(1048576),b''):h.update(b)
        require(s['identity']==self.ordinary(p,launcher=launcher)['identity'],'record changed')
        return dict(bytes=s['bytes'],sha256=h.hexdigest(),mode=s['mode'])
    def hash(self,p,algorithm='sha256'):
        self.ordinary(p);h=hashlib.new(algorithm)
        with open(p,'rb') as f:
            for b in iter(lambda:f.read(1048576),b''):h.update(b)
        return h.hexdigest()
    def list(self,root):
        self.ordinary(root,True);return sorted(str(p) for p in Path(root).iterdir())
    def link(self,p):require(self.stat(p)['kind']=='link','link kind');return os.readlink(p)
    def cutoff(self,explicit=None):
        whole=self.whole_end
        return whole if explicit is None else explicit if whole is None else min(explicit,whole)
    def step(self,cutoff):require(cutoff is None or time.monotonic()<cutoff,'original filesystem cutoff')
    def release_fd(self,fd,path,cutoff,phase,written):
        event=None;error=None
        if cutoff is not None and time.monotonic()>=cutoff:
            event=dict(fd=fd,path=path,phase=phase,bytes=written,status='SKIPPED_EXPIRED_UNRESOLVED')
        else:
            try:
                os.close(fd)
                if cutoff is not None and time.monotonic()>=cutoff:event=dict(fd=fd,path=path,phase=phase,bytes=written,status='RELEASED_LATE')
            except BaseException as e:
                event=dict(fd=fd,path=path,phase=phase,bytes=written,status='CLOSE_ERROR_AMBIGUOUS_UNRESOLVED');error=error_text(e)
        if event is not None:UNRESOLVED_HANDLES.append(event)
        return event,error
    def mkdir(self,p):
        cutoff=self.cutoff();self.step(cutoff);p=absolute(p);self.ordinary(str(PurePosixPath(p).parent),True);self.step(cutoff);os.mkdir(p,0o755);self.step(cutoff)
    def write_new(self,p,data,cutoff=None):
        # Unbuffered ownership: releases cannot flush a buffered pending write.
        cutoff=self.cutoff(cutoff)
        start=time.monotonic();fd=None;raw=None;error=None;release_errors=[];written=0
        facts=dict(kind='BOUNDED_EXCLUSIVE_PERSISTENCE',cutoff_ms=None if cutoff is None else int(cutoff*1000),actions=[],releases=[],opened=False,written_bytes=0,write_return_unresolved=False,flushed=False,fsynced=False,raw_released=False,fd_released=False)
        def check(stage):require(cutoff is None or time.monotonic()<cutoff,stage+' persistence cutoff')
        def begin(stage):check(stage);facts['actions'].append(stage)
        try:
            check('entry');p=absolute(p);self.ordinary(str(PurePosixPath(p).parent),True)
            begin('open');fd=os.open(p,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,0o644);facts['opened']=True;check('open return')
            begin('chmod');os.fchmod(fd,0o644);check('chmod return')
            begin('fdopen');raw=os.fdopen(fd,'wb',buffering=0,closefd=False);check('fdopen return')
            while written<len(data):
                begin('write');facts['write_return_unresolved']=True;count=raw.write(memoryview(data)[written:])
                require(type(count) is int and 0<count<=len(data)-written,'unbuffered write count')
                written+=count;facts['written_bytes']=written;facts['write_return_unresolved']=False;check('write return')
            begin('flush');raw.flush();facts['flushed']=True;check('flush return')
            begin('fsync');os.fsync(fd);facts['fsynced']=True;check('fsync return')
        except BaseException as e:error=error_text(e)
        finally:
            # Only eligible releases begin before the original cutoff. Retain
            # unresolved ownership rather than starting an expired close.
            for label,handle,close in (('raw_close',raw,lambda:raw.close()),('fd_close',fd,lambda:os.close(fd))):
                if handle is not None:
                    if cutoff is not None and time.monotonic()>=cutoff:
                        facts['releases'].append(dict(action=label,status='SKIPPED_EXPIRED_UNRESOLVED'));continue
                    facts['releases'].append(dict(action=label,status='STARTED_BEFORE_CUTOFF'))
                    try:
                        close();facts['raw_released' if label=='raw_close' else 'fd_released']=True
                        if cutoff is not None and time.monotonic()>=cutoff:facts['releases'][-1]['status']='RELEASED_LATE'
                    except BaseException as e:release_errors.append(dict(action=label,error=error_text(e)))
            if (raw is not None and not facts['raw_released']) or (fd is not None and not facts['fd_released']):
                UNRESOLVED_HANDLES.append(dict(phase='PERSISTENCE',cutoff=cutoff,raw=raw,fd=fd))
        facts.update(error=error,release_errors=release_errors,known_prefix_sha256=digest(data[:written]),elapsed_ms=int((time.monotonic()-start)*1000),late=cutoff is not None and time.monotonic()>=cutoff)
        if error is not None or release_errors or facts['late']:raise PersistenceRefusal(facts)
        return facts
    def sync(self,p):
        cutoff=self.cutoff();self.step(cutoff);p=absolute(p);self.ordinary(p,True);self.step(cutoff)
        fd=None;error=None;event=None;phase='open_directory'
        try:
            fd=os.open(p,os.O_RDONLY|os.O_DIRECTORY|os.O_NOFOLLOW);self.step(cutoff)
            phase='directory_fsync';self.step(cutoff);os.fsync(fd);self.step(cutoff)
        except BaseException as e:error=error_text(e)
        finally:
            if fd is not None:
                event,release_error=self.release_fd(fd,p,cutoff,phase,0)
                if error is None:error=release_error
        if error is not None or event is not None:raise PersistenceRefusal(dict(kind='BOUNDED_DIRECTORY_SYNC',path=p,error=error,release=event))
    def remove_marker(self,p):
        cutoff=self.cutoff();self.step(cutoff);self.ordinary(p);self.step(cutoff);os.unlink(p);self.step(cutoff)
        # Last mutator. A late return refuses without another publication.
    def protected_hash(self,p):
        # Historical protection is opaque and never grants input permission.
        s=self.stat(p);require(p not in HISTORICAL_SPECIALS and s['kind']=='file' and s['mode']&0o444,'protected ordinary readable file');h=hashlib.sha256()
        with open(p,'rb') as f:
            for b in iter(lambda:f.read(1048576),b''):h.update(b)
        require(s['identity']==self.stat(p)['identity'],'protected file changed');return h.hexdigest()
    def copy_file(self,source,target):
        cutoff=self.cutoff();self.step(cutoff);before=self.record(source);self.ordinary(str(PurePosixPath(absolute(target)).parent),True);self.step(cutoff)
        handles=[];error=None;releases=[];written=0;phase='open_source'
        try:
            src=os.open(source,os.O_RDONLY|os.O_NOFOLLOW);handles.append((src,source));self.step(cutoff)
            phase='open_target';self.step(cutoff);dst=os.open(target,os.O_WRONLY|os.O_CREAT|os.O_EXCL|os.O_NOFOLLOW,before['mode']);handles.append((dst,target));self.step(cutoff)
            phase='chmod';self.step(cutoff);os.fchmod(dst,before['mode']);self.step(cutoff)
            while True:
                phase='read_source';self.step(cutoff);block=os.read(src,1048576);self.step(cutoff)
                if not block:break
                view=memoryview(block);offset=0
                while offset<len(view):
                    phase='write_target';self.step(cutoff);count=os.write(dst,view[offset:]);require(type(count) is int and 0<count<=len(view)-offset,'raw copy write count');offset+=count;written+=count;self.step(cutoff)
            phase='copy_fsync';self.step(cutoff);os.fsync(dst);self.step(cutoff)
        except BaseException as e:error=error_text(e)
        finally:
            for fd,path in reversed(handles):
                event,release_error=self.release_fd(fd,path,cutoff,phase,written)
                if event is not None:releases.append(event)
                if error is None:error=release_error
        if error is not None or releases:raise PersistenceRefusal(dict(kind='BOUNDED_PHYSICAL_COPY',source=source,target=target,bytes=written,phase=phase,error=error,releases=releases))
        self.step(cutoff);require(self.record(source)==before==self.record(target),'copy source/target identity');self.step(cutoff)

class Gate:
    def __init__(self,fs):self.fs=fs;self.checked={};self.dependency_files=set();self.armed={}
    def record(self,p):
        p=absolute(p);row=self.fs.record(p,launcher=p in self.armed and p not in self.dependency_files)
        if p in self.checked:require(equal(row,self.checked[p]),'late consumed identity/mode change')
        self.checked[p]=row;return row
    def dependency_record(self,p):self.dependency_files.add(absolute(p));return self.record(p)
    def arm_launcher(self,p,expected):
        require(p in LAUNCHERS,'fixed installed launcher role');sha_string(expected)
        self.armed[p]=expected;row=self.record(p);require(row['sha256']==expected and row['mode']==0o755,'launcher identity')
        return row
    def read(self,p,maximum=MAX_JSON):
        # Read context is ALWAYS strict, even after named launcher arming.
        self.dependency_files.add(absolute(p));data=self.fs.read(p,maximum);require(digest(data)==self.record(p)['sha256'],'read identity');return data
    def json(self,p):return parse_json(self.read(p))
    def recheck(self):
        for p in tuple(self.checked):self.record(p)

def check_specials(rows,complete=True):
    require(type(rows) is dict and list(rows)==sorted(rows),'sorted historical-special map')
    require(set(rows)<=HISTORICAL_SPECIALS and (not complete or set(rows)==HISTORICAL_SPECIALS),'exact fourteen original historical roles')
    for path,row in rows.items():
        fifo=path in HISTORICAL_FIFOS
        keys(row,('kind','mode','nlink','device','inode') if fifo else ('kind','bytes','mode','nlink','device','inode','mtime_ns','ctime_ns'),'historical lstat row')
        require(row['kind']==('fifo' if fifo else 'unreadable_regular'),'historical type')
        integer(row['mode'],420 if fifo else 0,420 if fifo else 0);integer(row['nlink'],1,1);integer(row['device'],0,9007199254740991);integer(row['inode'],1,9007199254740991)
        if not fifo:
            integer(row['bytes'],12,12)
            for key in ('mtime_ns','ctime_ns'):require(type(row[key]) is str and re.fullmatch(r'0|[1-9][0-9]{0,19}',row[key]),'canonical historical ns string')
def special_record(fs,path,before):
    fifo=path in HISTORICAL_FIFOS
    require(before['kind']==('fifo' if fifo else 'file'),'no retyped historical role')
    row=dict(kind='fifo' if fifo else 'unreadable_regular',mode=before['mode'],nlink=before['nlink'],device=before['device'],inode=before['inode'])
    if not fifo:
        row['bytes']=before['bytes']
        for key in ('mtime_ns','ctime_ns'):row[key]=str(integer(before[key],0,10**20-1))
    check_specials({path:row},False)
    after=fs.stat(path)
    require(all(after[key]==before[key] for key in ('kind','mode','nlink','bytes','device','inode','mtime_ns','ctime_ns')),'historical lstat identity changed')
    return row
def tree(fs,root,opaque=False):
    files={};dirs=[];links={};specials={}
    def walk(p):
        s=fs.stat(p)
        if p in HISTORICAL_SPECIALS:
            require(opaque,'historical role cannot be owned or consumed');specials[p]=special_record(fs,p,s);return
        if s['kind']=='link':
            require(opaque,'unapproved tree link');links[p]=dict(target=fs.link(p),mode=s['mode']);return
        if s['kind']=='directory':
            dirs.append(p)
            for child in fs.list(p):walk(child)
        else:require(s['kind']=='file' and s['mode']&0o444 and (opaque or s['nlink']==1),'ordinary readable tree member');files[p]=fs.protected_hash(p) if opaque else fs.record(p)['sha256']
    if not fs.exists(root):return dict(files={},directories=[],links={},specials={},absent_roots=[root])
    walk(root);return dict(files=files,directories=sorted(dirs),links=links,specials=dict(sorted(specials.items())),absent_roots=[])

def inventory(fs,root,excluded=()):
    found=tree(fs,root);return dict(files={p[len(root)+1:]:fs.record(p) for p in sorted(found['files']) if p[len(root)+1:] not in excluded},directories=sorted(p[len(root)+1:] for p in found['directories'] if p!=root))

class Shell(HTMLParser):
    def __init__(self):super().__init__();self.canvas=[];self.scripts=[]
    def handle_starttag(self,tag,attrs):
        values=dict(attrs)
        if tag=='canvas':self.canvas.append(values.get('id'))
        if tag=='script' and 'src' in values:self.scripts.append(values['src'])

class Recipe:
    fixture_only=False
    def __init__(self):
        self.ROOT=str(Path(__file__).absolute().parents[3]);self.HERE=self.ROOT+'/web/build/blackwood'
        self.fs=FileSystem();self.gate=Gate(self.fs);self.started=None;self.reserved=[];self.control_paths=set()
        self.effects=Effects()
    def repo(self,name):return self.ROOT+'/'+relative(name)
    def paths(self,id_):identifier(id_);return self.HERE+'/attempts/'+id_,self.HERE+'/candidates/'+id_
    def context(self):require(type(self.fixture_only) is bool and self.fs.fixture_only==self.fixture_only,'FIXTURE_ONLY filesystem cannot be production')
    def config(self):
        self.context();cfg=self.gate.json(self.HERE+'/config.json');require(equal(cfg,FIXED_CONFIG),'exact fixed Blackwood config/sole define')
        require(digest(self.gate.read(self.HERE+'/shell.html'))=='6fccbeb1094a4f09998db25b123d2b9287b75da013f80d6e72a0444efa751399','exact accepted shell')
        return cfg
    def units(self):
        text=self.gate.read(self.repo('source/src/Makefile')).decode()
        match=re.search(r'CLIENT_OBJS=\s*\\\n(.*?)\n\nCLIENT_PCH=',text,re.S);require(match is not None,'Makefile CLIENT_OBJS')
        cpp=['source/src/'+n+'.cpp' for n in re.findall(r'([A-Za-z0-9_/]+)\.o',match[1])]
        require(cpp==list(UNITS[:53]) and len(set(UNITS))==61,'fixed genuine ordered53+8')
        for n in UNITS:self.gate.record(self.repo(n))
        return list(UNITS)
    def source_acceptance(self):
        refs=[]
        for path,pin in ACCEPTANCE_PINS.items():require(self.gate.record(self.repo(path))['sha256']==pin,'T163 accepted reference');refs.append(dict(path=path,sha256=pin))
        files=[]
        for path,pin in sorted(SOURCE_PINS.items()):
            row=self.gate.record(self.repo(path));require(row['sha256']==pin and row['mode']==420,'accepted T163 source identity');files.append(dict(path=path,**row))
        return dict(ticket='T163',decision=refs[0],handoff=refs[1],evidence=refs[2],files=files)
    def pack(self,cfg):
        manifests={}
        for n,pin in MANIFEST_PINS.items():require(self.gate.record(self.repo(n))['sha256']==pin,'accepted manifest pin');manifests[n]=self.gate.json(self.repo(n))
        m=manifests[cfg['manifest']]
        keys(m,'schema_version profile map_name map_revision mount inputs entries raw_bytes transfer_measurement assembly_performed existing_profiles_modified runtime_verified gameplay_verified candidate_balance_accepted'.split(),'T148 manifest')
        expected=dict(schema_version=1,profile=PROFILE,map_name='blackwood_greybox_v1',map_revision=1,mount='/outbreak',raw_bytes=411990,transfer_measurement='NOT_OBSERVED',assembly_performed=True,existing_profiles_modified=False,runtime_verified=False,gameplay_verified=False,candidate_balance_accepted=False)
        for n,v in expected.items():require(equal(m[n],v),'T148 identity/type '+n)
        require(type(m['entries']) is list and len(m['entries'])==84,'84 mapped entries')
        sources=[dict(path=n,sha256=MANIFEST_PINS[n]) for n in ('web/assets/network-profile/manifest.json','web/assets/blackwood-candidate/manifest.json')]
        require(equal(m['inputs'],sources),'two original manifest bindings')
        originals={n:{e['path']:e for e in doc['entries']} for n,doc in manifests.items() if n!=cfg['manifest']}
        require(len(originals[sources[0]['path']])==79 and len(originals[sources[1]['path']])==5,'79+5 source split')
        mapping=[];paths=[];count={n:0 for n in originals};total=0
        for e in m['entries']:
            keys(e,'path virtual_path bytes sha256 license notice source_manifest source_path source_sha256'.split(),'source-mapped entry')
            path=relative(e['path']);source=relative(e['source_path']);sha_string(e['sha256']);integer(e['bytes'],1)
            require(e['virtual_path']=='/outbreak/'+path and e['source_manifest'] in originals,'virtual/source context')
            origin=originals[e['source_manifest']].get(source);require(origin is not None,'original source missing')
            require(e['bytes']==origin['bytes'] and e['sha256']==e['source_sha256']==origin['sha256'] and e['license']==origin['license'],'source bytes/license mapping')
            black=e['source_manifest']==sources[1]['path']
            expected_path=('notices/blackwood-candidate/'+source if source in ('LICENSE.txt','PROVENANCE.json') else source) if black else source
            require(path==expected_path and e['notice']==('notices/blackwood-candidate/LICENSE.txt' if black else origin['notice']),'notice/source namespace')
            original=e['source_manifest'].removesuffix('manifest.json')+'pack-root/'+source
            for n in (cfg['pack_root']+'/'+path,original):
                row=self.gate.record(self.repo(n));require(row==dict(bytes=e['bytes'],sha256=e['sha256'],mode=420),'actual original/assembled identity')
            require(self.gate.read(self.repo(cfg['pack_root']+'/'+e['notice']))==self.gate.read(self.repo(e['source_manifest'].removesuffix('manifest.json')+'pack-root/'+origin['notice'])),'notice exact source association')
            paths.append(path);mapping.append({k:e[k] for k in ('path','source_manifest','source_path','source_sha256')});count[e['source_manifest']]+=1;total+=e['bytes']
        require(paths==sorted(set(paths)) and list(count.values())==[79,5] and total==411990,'sorted exact84 bytes')
        actual=inventory(self.fs,self.repo(cfg['pack_root']));require(set(actual['files'])==set(paths),'exact pack membership')
        for d in actual['directories']:require(any(p.startswith(d+'/') for p in paths),'unknown empty pack directory')
        provpath='web/assets/blackwood-profile/PROVENANCE.json';require(self.gate.record(self.repo(provpath))['sha256']==ASSEMBLY_PROVENANCE_SHA,'accepted assembly provenance')
        blackprov=self.gate.json(self.repo(cfg['pack_root']+'/notices/blackwood-candidate/PROVENANCE.json'));require(blackprov['limitations']==LIMITATIONS and blackprov['canonical_slots']['count']==32 and blackprov['legacy_starts']['count']==8,'opaque original limitations/slots/technical starts')
        self.cfg_closure(cfg)
        return m,dict(manifest=dict(path=cfg['manifest'],sha256=MANIFEST_PINS[cfg['manifest']]),profile=PROFILE,files=84,raw_bytes=411990,map=cfg['map'],source_manifests=sources,source_mapping_sha256=digest(canonical(mapping)),entries_sha256=digest(canonical(m['entries'])),limitations=LIMITATIONS[:])
    def cfg_closure(self,cfg):
        base=cfg['pack_root'];cgz=self.repo(base+'/packages/maps/blackwood_greybox_v1.cgz');config=self.repo(base+'/packages/maps/blackwood_greybox_v1.cfg')
        require(self.gate.record(cgz)['bytes']==734 and self.gate.record(cgz)['sha256']==cfg['map']['cgz_sha256'] and self.gate.record(config)['sha256']==cfg['map']['cfg_sha256'],'fixed CGZ/CFG')
        lines=[x.split('//',1)[0].strip() for x in self.gate.read(config).decode().splitlines()];lines=[x for x in lines if x]
        require(lines==['mapmodelreset','mapsoundreset','texturereset','texture 0 "outbreak/ceiling.png"','texture 0 "outbreak/ground.png"','texture 0 "outbreak/wall.png"','texture 0 "outbreak/ground.png"','texture 0 "outbreak/ceiling.png"','fog 256','fogcolour 0x18232B'],'sealed exact CFG order')
        common=self.gate.read(self.repo(base+'/config/browser.cfg')).decode()
        allow=re.findall(r'^scriptcontext MAPCFG (\w+)$',common,re.M)
        require(allow==['texture','texturereset','mapmodelreset','mapsoundreset','fog','fogcolour'] and '\nisolatecontext MAPCFG\n' in common,'sealed MAPCFG allowlist')
        for n in ('ceiling','ground','wall'):self.gate.record(self.repo(base+'/packages/textures/outbreak/'+n+'.png'))
    def notices(self):
        root=self.repo('web/build/notices');actual=inventory(self.fs,root)
        expected={n.removeprefix('notices/') for n in NOTICE_PINS};require(set(actual['files'])==expected and not actual['directories'],'exact12 source notices')
        for n,h in NOTICE_PINS.items():require(self.gate.record(root+'/'+n.removeprefix('notices/'))['sha256']==h,'scoped source notice pin')
        return dict(NOTICE_PINS)
    def alias_policy(self):
        rows=[];decisions={}
        for name,pin in ALIAS_PINS.items():
            require(self.gate.record(self.repo(name))['sha256']==pin,'alias decision identity');doc=self.gate.json(self.repo(name))
            allowed={'schema_version','root','aliases'}|({'inspected_supporting_files'} if 'D046' in name else set());keys(doc,allowed,'alias decision')
            integer(doc['schema_version'],1,1);root=doc['root'];absolute(root)
            require(root==(SDK+'/upstream/bin' if 'D044' in name else SDK+'/upstream/emscripten/node_modules'),'fixed alias root')
            for row in doc['aliases']:
                keys(row,('path','link_text','resolved_path','resolved_sha256'),'alias');p=row['path']
                require(p in ALIAS_TEXT and row['link_text']==ALIAS_TEXT[p] and below(p,root),'fixed alias names')
                require(self.fs.link(p)==row['link_text'],'alias raw text')
                current=p;seen=set();declared={r['path']:r for r in doc['aliases']}
                while self.fs.stat(current)['kind']=='link':
                    require(current in declared and current not in seen,'unapproved/cyclic alias');seen.add(current)
                    link=self.fs.link(current);require(link==declared[current]['link_text'] and not link.startswith('/'),'alias text/absolute escape')
                    current=os.path.normpath(str(PurePosixPath(current).parent)+'/'+link);require(below(current,root),'alias escape')
                require(current==row['resolved_path'] and self.gate.record(current)['sha256']==row['resolved_sha256'],'alias resolved bytes');rows.append(row)
            supporting=doc.get('inspected_supporting_files',{})
            for p,h in supporting.items():require(self.gate.record(absolute(p))['sha256']==h,'alias supporting source')
            decisions[name]=dict(sha256=pin,root=root,aliases=doc['aliases'],supporting_files=supporting)
        require({r['path'] for r in rows}==set(ALIAS_TEXT) and len(rows)==5,'exact five alias roles')
        return rows,decisions
    def ports(self,cfg):
        root=self.repo('web/build/.cache/ports');rows=[]
        for spec in PORT_SPECS:
            recipe=SDK+'/upstream/emscripten/tools/ports/'+spec['name']+'.py'
            require(self.gate.record(recipe)['sha256']==spec['recipe_sha256'],'port recipe')
            candidates=[p for p in self.fs.list(root) if str(PurePosixPath(p).name).startswith(spec['name']+'.') and p.endswith(('.zip','.tar.gz'))]
            require(len(candidates)==1,'exact retained port archive');archive=candidates[0]
            row=self.gate.record(archive);require(self.fs.hash(archive,'sha512')==spec['expected_sha512'],'accepted archive SHA512')
            rows.append(dict(name=spec['name'],recipe=recipe,recipe_sha256=spec['recipe_sha256'],archive=archive,archive_sha256=row['sha256'],archive_sha512=spec['expected_sha512']))
        return rows
    def tools(self,cfg,aliases):
        require(self.gate.record(self.repo(ADAPTER_DECISION[0]))['sha256']==ADAPTER_DECISION[1],'D235 adapter decision bytes')
        for p,h in CTYPES_INPUTS.items():require(self.gate.record(p)['sha256']==h,'declared ctypes input bytes without import')
        for p,h in DARWIN_WAIT_HEADERS.items():require(self.gate.record(p)['sha256']==h,'fixed nonreaping ABI header bytes')
        require(self.gate.read(SDK+'/upstream/emscripten/emscripten-version.txt').decode().strip().strip('"')==cfg['sdk_version'],'SDK version bytes')
        require(self.gate.read(SDK+'/upstream/emscripten/emscripten-revision.txt').decode().strip()==cfg['compiler_revision'],'SDK revision bytes')
        python='/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11';node=SDK+'/node/24.19.0_64bit/bin/node'
        require(self.gate.record(python)['sha256']=='4e28e811a89aeac6eed668ae641c7f85f5831e42e8dc6cd9a85a3bcc032ec46a','Python role bytes')
        require(self.gate.record(node)['sha256']=='27db838bb204ef7c21df2931f5656e4c8fb32e6e947f363a402b49714d32b5b1','Node role bytes')
        if not self.fixture_only:require(os.path.realpath(sys.executable)==python and sys.version_info[:3]==(3,11,9),'actual driver interpreter')
        self.gate.record(SDK+'/.emscripten')
        def walk(p):
            for child in self.fs.list(p):
                s=self.fs.stat(child)
                if s['kind']=='directory':
                    if PurePosixPath(child).name not in ('.git','__pycache__','.bin'):walk(child)
                elif s['kind']=='link':require(child in ALIAS_TEXT,'undeclared SDK link')
                elif not child.endswith('.pyc'):self.gate.record(child)
        for name in ('bin','lib','include','share','emscripten'):walk(SDK+'/upstream/'+name)
        for p in tree(self.fs,self.repo('web/build/.cache'))['files']:self.gate.record(p)
        # Authoring stdlib/extension inputs are bytes, never executed probes.
        if not self.fixture_only:
            adapter_platform()
            prefix=str(Path(sys.base_prefix).resolve())
            for module in tuple(sys.modules.values()):
                filename=getattr(module,'__file__',None)
                if filename and filename.endswith(('.py','.so')) and below(filename,prefix) and '/site-packages/' not in filename:self.gate.record(absolute(filename))
    def repository_inputs(self):
        names=[ADAPTER_DECISION[0]]+['web/build/blackwood/'+n for n in OWN_FILES]+list(UNITS)+[n for n in ACCEPTANCE_PINS if self.fs.exists(self.repo(n))]+['source/src/Makefile','source/src/ge25519_base.data','web/transport/enet_websocket.js']+list(ALIAS_PINS)
        for root in ('source/src','source/enet','web/transport'):
            for p in tree(self.fs,self.repo(root))['files']:
                if p.endswith(('.h','.hpp','.inc','.inl')):names.append(p[len(self.ROOT)+1:])
        # Exact accepted asset originals and manifests are all consumed/provenance inputs.
        for root in ('web/assets/blackwood-profile','web/assets/network-profile','web/assets/blackwood-candidate'):
            names.append(root+'/manifest.json')
            if root.endswith('blackwood-profile'):names.append(root+'/PROVENANCE.json')
            for p in tree(self.fs,self.repo(root+'/pack-root'))['files']:names.append(p[len(self.ROOT)+1:])
        names+=['web/build/'+n for n in NOTICE_PINS]
        pins={'web/transport/enet_websocket.c':'5d386d859e7178e9777de130ac399da26a015f51b78f78d4bcaee86ecfbac053','web/transport/enet_websocket.js':'ce706fd7b8e2ce583d15483ef122b35f91bc48d14f58af6495994c69c6180d34','web/transport/enet_ws_bridge.h':'c1905aef1a57b0f599d2e176d90c1e8786fbfea5caf9ec12a8c36f3f7840b832','source/src/browsernet.h':'0a7f522f26d6a29c1956e15a69d601e481790d69091071622f9db73c759e6b44'}
        for n,h in pins.items():require(self.gate.record(self.repo(n))['sha256']==h,'accepted transport bytes')
        return {self.repo(n):self.gate.record(self.repo(n))['sha256'] for n in sorted(set(names))}
    def read_head(self):
        directory=self.ROOT+'/.git'
        if self.fs.stat(directory)['kind']=='file':
            value=self.gate.read(directory).decode().strip();require(value.startswith('gitdir: '),'gitdir metadata')
            directory=os.path.normpath(self.ROOT+'/'+value[8:]) if not value[8:].startswith('/') else absolute(value[8:])
        common=directory
        if self.fs.exists(directory+'/commondir'):common=os.path.normpath(directory+'/'+self.gate.read(directory+'/commondir').decode().strip())
        value=self.gate.read(directory+'/HEAD').decode().strip();seen=set()
        while value.startswith('ref: '):
            ref=relative(value[5:]);require(ref.startswith('refs/') and ref not in seen,'cyclic git metadata');seen.add(ref)
            candidates=[p+'/'+ref for p in (directory,common) if self.fs.exists(p+'/'+ref)]
            if candidates:value=self.gate.read(candidates[0]).decode().strip()
            else:
                rows=[s.split()[0] for s in self.gate.read(common+'/packed-refs').decode().splitlines() if s and not s.startswith(('#','^')) and len(s.split())==2 and s.split()[1]==ref]
                require(len(rows)==1,'HEAD packed ref');value=rows[0]
        return revision(value)
    def source_manifest(self,rev,consumed):
        path=self.repo(SOURCE_MANIFEST);doc=self.gate.json(path);keys(doc,('schema_version','kind','source_revision','entries'),'source manifest')
        integer(doc['schema_version'],1,1);require(doc['kind']=='SOURCE_INPUT_MANIFEST' and doc['source_revision']==rev and type(doc['entries']) is list,'source manifest identity')
        names=[]
        for row in doc['entries']:
            keys(row,('path','bytes','sha256','mode'),'source entry');name=relative(row['path']);integer(row['bytes']);sha_string(row['sha256']);integer(row['mode'],420,493)
            require(row['mode'] in (420,493) and name!=SOURCE_MANIFEST,'source mode/self exclusion')
            require(self.gate.record(self.repo(name))=={k:row[k] for k in ('bytes','sha256','mode')},'source manifest current overlay identity');names.append(name)
        require(names==sorted(set(names)) and {p[len(self.ROOT)+1:] for p in consumed}<=set(names),'source manifest exact sorted consumed closure')
        return dict(path=SOURCE_MANIFEST,sha256=self.gate.record(path)['sha256'])
    def preservation(self,owned=()):
        combined=dict(files={},directories=[],links={},specials={},absent_roots=[])
        for root in (self.repo('source'),self.repo('web'),self.repo('tests'),SDK):
            found=tree(self.fs,root,opaque=True)
            for field in ('files','links','specials'):combined[field].update({p:v for p,v in found[field].items() if not any(below(p,o) for o in owned)})
            for field in ('directories','absent_roots'):combined[field].extend(p for p in found[field] if not any(below(p,o) for o in owned))
        for field in ('directories','absent_roots'):combined[field]=sorted(set(combined[field]))
        combined['specials']=dict(sorted(combined['specials'].items()));check_specials(combined['specials'])
        return combined
    def protection_equal(self,before,current,owned):
        for row in (before,current):
            keys(row,('files','directories','links','specials','absent_roots'),'preservation');check_specials(row['specials'])
            require(not set(row['specials']).intersection(set(row['files'])|set(row['links'])|set(row['directories'])|set(row['absent_roots'])),'cross-table historical role')
        require(equal(before['files'],current['files']) and equal(before['links'],current['links']),'protected byte/link/file membership change')
        require(equal(before['specials'],current['specials']),'original historical-special identity change')
        parents={str(PurePosixPath(p).parent) for p in owned}
        require(set(current['directories'])-set(before['directories'])<=parents and set(before['directories'])<=set(current['directories']),'phase directory union')
        require(set(before['absent_roots'])-set(current['absent_roots'])<=parents and set(current['absent_roots'])<=set(before['absent_roots']),'phase absent-root union')
    def observe(self,strict=True,owned=()):
        cfg=self.config();units=self.units();manifest,pack=self.pack(cfg);self.notices();consumed=self.repository_inputs();aliases,decisions=self.alias_policy();ports=self.ports(cfg);errors=[]
        try:self.tools(cfg,aliases)
        except (ValueError,OSError) as e:
            if strict:raise
            errors.append(str(e)[:512])
        rev=self.read_head();source=self.source_manifest(rev,consumed) if self.fs.exists(self.repo(SOURCE_MANIFEST)) else None
        acceptance=self.source_acceptance() if all(self.fs.exists(self.repo(n)) for n in ACCEPTANCE_PINS) else None
        inputs={p:r['sha256'] for p,r in self.gate.checked.items() if p not in self.control_paths and not below(p,self.HERE+'/attempts') and not below(p,self.HERE+'/candidates') and not below(p,self.ROOT+'/.git')}
        observed=dict(inputs=inputs,preservation=self.preservation(owned),units=units,ports=ports,aliases=aliases,alias_decisions=decisions,pack=pack,tool_errors=errors)
        keys(observed,OBSERVATION,'observation');return cfg,manifest,observed,rev,source,acceptance
    def environment(self,attempt):
        return dict(PATH='/usr/bin:/bin:/usr/sbin:/sbin',EMSDK=SDK,EMSDK_PYTHON='/Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11',EM_CONFIG=SDK+'/.emscripten',EM_CACHE=attempt+'/cache',EM_PORTS=attempt+'/cache/ports',EM_FROZEN_CACHE='1',NODE_COMPILE_CACHE=attempt+'/node-cache',EMCC_TEMP_DIR=attempt+'/tmp',TMPDIR=attempt+'/tmp',PYTHONDONTWRITEBYTECODE='1')
    def commands(self,cfg,units,attempt):
        require(equal(cfg,FIXED_CONFIG) and units==list(UNITS),'fixed command context');rows=[]
        for i,source in enumerate(units):
            cpp=source.endswith('.cpp');obj=attempt+'/objects/%02d.o'%i;pre=attempt+'/deps/%02d.pre.d'%i;post=attempt+'/deps/%02d.post.d'%i
            argv=[SDK+'/upstream/emscripten/'+('em++' if cpp else 'emcc')]+(cfg['common_cxx']+cfg['ports'] if cpp else cfg['common_c'])+['-I'+self.repo(p) for p in ('source/src','source/src/bot','source/enet/include','web/transport')]
            rows.append(dict(source=source,object=obj,pre_depfile=pre,post_depfile=post,pre_command=argv+['-M','-MF',pre,'-MT',obj,self.repo(source)],command=argv+['-c',self.repo(source),'-o',obj,'-MD','-MF',post]))
        link=[SDK+'/upstream/emscripten/em++']+[r['object'] for r in rows]+cfg['ports']+cfg['link']+['--js-library',self.repo(cfg['js_library']),'--shell-file',self.repo(cfg['shell']),'--preload-file',self.repo(cfg['pack_root'])+'@/outbreak','-o',attempt+'/bundle/index.html']
        node=SDK+'/node/24.19.0_64bit/bin/node'
        return dict(compiles=rows,link=link,syntax=[node,'--check',attempt+'/bundle/index.js'],wasm_validation=[node,'-e',"if(!WebAssembly.validate(require('fs').readFileSync(process.argv[1])))process.exit(1)",attempt+'/bundle/index.wasm'])
    def plan(self,id_):
        attempt,publication=self.paths(id_);require(not self.fs.exists(attempt) and not self.fs.exists(publication),'occupied candidate')
        cfg,manifest,observation,rev,source,acceptance=self.observe(strict=False);pending=['EXECUTION_PINS_NOT_SUPPLIED']
        if source is None:pending.append('MAIN_SOURCE_MANIFEST_MISSING')
        if acceptance is None:pending.append('T163_NOT_ACCEPTED')
        return dict(schema_version=1,kind='BLACKWOOD_BUILD_PLAN',status='NOT_EXECUTED',recipe=RECIPE,candidate_id=id_,source_revision=rev,source_manifest=source,source_acceptance=acceptance,observation=observation,commands=self.commands(cfg,observation['units'],attempt),environment=self.environment(attempt),claims=CLAIMS.copy(),pending=pending)
    def authorization(self,id_,path,pin,observation,completed=False):
        path=absolute(path);sha_string(pin);require(str(PurePosixPath(path).parent)==self.repo('notes/decisions') and path.endswith('.json'),'fixed MAIN pins path')
        self.control_paths.add(path)
        require(self.gate.record(path)['sha256']==pin,'pins digest');doc=self.gate.json(path);keys(doc,AUTH,'authorization');integer(doc['schema_version'],1,1)
        require(doc['kind']=='CANDIDATE_BLACKWOOD_BUILD_AUTHORIZATION' and doc['authority']=='MAIN' and doc['status']=='ACCEPTED' and doc['execution_release']=='EXPLICIT_BLACKWOOD_NETWORK_BUILD_EXECUTION' and doc['recipe']==RECIPE and doc['candidate_id']==id_,'explicit fixed build authority')
        require(type(doc['ticket']) is str and 0<len(doc['ticket'])<=64 and doc['ticket'].isascii() and doc['ticket'].strip()==doc['ticket'],'ticket provenance')
        decision=relative(doc['decision']);require(decision.startswith('notes/decisions/') and decision.endswith('.md') and '/' not in decision.removeprefix('notes/decisions/'),'authority decision path')
        require(observation['inputs'].get(self.repo(decision))==self.gate.record(self.repo(decision))['sha256'],'decision consumed/source-bound')
        require(equal(doc['bindings'],dict(repository=self.ROOT,sdk=SDK,ports_cache=self.repo('web/build/.cache'))),'fixed root bindings')
        rev=self.read_head();require(doc['source_revision']==rev,'HEAD source revision');consumed=self.repository_inputs();source=self.source_manifest(rev,consumed)
        require(equal(doc['source_manifest'],source) and equal(doc['source_acceptance'],self.source_acceptance()),'MAIN successor source/accepted overlay binding')
        require(decision in [r['path'] for r in self.gate.json(self.repo(SOURCE_MANIFEST))['entries']],'decision in MAIN source manifest')
        keys(doc['observation'],OBSERVATION,'authorization observation');require(equal(doc['observation'],observation) and observation['tool_errors']==[],'full observation mismatch')
        if not completed:
            a,p=self.paths(id_);require(not self.fs.exists(a) and not self.fs.exists(p),'occupied authority')
        return doc
    def boundary(self,observed,owned,pins_path,pins_sha,pins):
        self.gate.recheck();cfg,m,current,rev,s,a=self.observe(owned=owned)
        for key in OBSERVATION-{'preservation'}:require(equal(observed[key],current[key]),'late observation '+key)
        self.protection_equal(observed['preservation'],current['preservation'],owned)
        require(equal(self.authorization(pins['candidate_id'],pins_path,pins_sha,observed,True),pins),'late authority')
        require(self.started is not None and time.monotonic()-self.started<3600,'whole build deadline')
    def dependencies(self,path,attempt,observed):
        text=self.fs.read(path).decode().replace('\\\n',' ');require(': ' in text,'dependency target')
        # Compiler Make rules escape spaces/backslashes/dollars, not shell commands.
        body=text.split(': ',1)[1];tokens=[];token='';escaped=False
        for c in body:
            if escaped:token+=c;escaped=False
            elif c=='\\':escaped=True
            elif c.isspace():
                if token:tokens.append(token.replace('$$','$'));token=''
            else:token+=c
        if token:tokens.append(token.replace('$$','$'))
        require(tokens and not escaped and len(tokens)==len(set(tokens)),'dependency syntax/duplicate')
        rows={}
        for token in tokens:
            actual=absolute(token if token.startswith('/') else self.repo(relative(token)))
            original=self.repo('web/build/.cache')+actual[len(attempt+'/cache'):] if below(actual,attempt+'/cache') else actual
            require(original in observed['inputs'],'undeclared dependency before read')
            row=self.gate.dependency_record(actual);require(row['sha256']==observed['inputs'][original],'changed dependency/context')
            rows[original]=row['sha256']
        return dict(sorted(rows.items()))
    def validate_payload(self,root,manifest):
        html=self.fs.read(root+'/index.html').decode();parser=Shell();parser.feed(html)
        require(parser.canvas==['canvas'] and parser.scripts==['index.js'] and '{{{ SCRIPT }}}' not in html,'actual HTML canvas/script')
        require(self.fs.read(root+'/index.wasm')[:8]==MAGIC,'actual Wasm magic')
        data=self.fs.read(root+'/index.data');require(len(data)==411990,'actual data length')
        js=self.fs.read(root+'/index.js').decode();slices=re.findall(r'\{filename:"([^"]+)",start:(\d+),end:(\d+)\}',js)
        expected={e['virtual_path']:e for e in manifest['entries']}
        require(len(slices)==len(expected)==len({r[0] for r in slices})==84 and {r[0] for r in slices}==set(expected),'exact84 actual slices')
        cursor=0;rows=[]
        for name,begin,end in sorted(slices,key=lambda r:int(r[1])):
            start,finish=int(begin),int(end);require(start==cursor and finish>start and finish<=len(data),'slice gap/overlap/bounds')
            e=expected[name];value=data[start:finish];require(len(value)==e['bytes'] and digest(value)==e['sha256'],'actual slice identity')
            rows.append(dict(path=name,start=start,end=finish,sha256=e['sha256']));cursor=finish
        require(cursor==len(data),'unindexed suffix')
        return dict(status='PASS',files=84,raw_bytes=411990,actual_preload_slices=rows,canvas='canvas',runtime_decoding='NOT RUN')
    def bundle_identity(self,result):
        commands=[r[k]['argv'] for r in result['compiles'] for k in ('pre_scan','compile')]+[result[k]['argv'] for k in ('link','syntax','wasm_validation')]
        return digest(canonical(dict(inputs=result['observation']['inputs'],outputs=result['outputs'],pins_sha256=result['pins']['sha256'],environment=result['environment'],commands=commands)))
    def verify_bundle(self,root,manifest,result,publication=False):
        require(equal(self.validate_payload(root,manifest),result['preload_validation']),'independent actual preload evidence')
        outputs={n:self.fs.record(root+'/'+n)['sha256'] for n in ARTIFACTS};require(equal(outputs,result['outputs']),'actual four output identities')
        notices={n:self.fs.record(root+'/'+n)['sha256'] for n in NOTICE_PINS};require(notices==result['notices']==NOTICE_PINS,'exact12 notices')
        actual=inventory(self.fs,root,('verification/receipt.json',));require(set(actual['files'])==set(ARTIFACTS)|{'build-metadata.json'}|set(NOTICE_PINS),'exact17 outer files')
        require(set(actual['directories'])==({'notices','verification'} if publication else {'notices'}),'exact outer directories')
        metadata=dict(result);metadata.pop('metadata_sha256');require(self.fs.read(root+'/build-metadata.json')==canonical(metadata) and self.fs.record(root+'/build-metadata.json')['sha256']==result['metadata_sha256'],'metadata exact nonrecursive result')
        return actual
    def reserve(self,attempt,publication):
        require(not self.fs.exists(attempt) and not self.fs.exists(publication),'preflight both absent')
        for parent in (str(PurePosixPath(attempt).parent),str(PurePosixPath(publication).parent)):
            if not self.fs.exists(parent):self.fs.mkdir(parent)
        self.fs.mkdir(attempt);self.reserved.append(attempt)
        self.fs.write_new(attempt+'/failure.json',canonical(dict(status='REFUSE',recipe=RECIPE,candidate_id=PurePosixPath(attempt).name,error='NOT_COMPLETED')));self.fs.sync(attempt)
        self.fs.mkdir(publication);self.reserved.append(publication)
    def owned_layout(self,attempt,commands,marker_allowed=False):
        actual=inventory(self.fs,attempt,('freeze.json','failure.json') if marker_allowed else ('freeze.json',));roots={p.split('/')[0] for p in actual['directories']}
        require(roots=={'objects','deps','logs','bundle','cache','tmp','node-cache'},'exact owned top directories')
        require({p for p in actual['files'] if '/' not in p}=={'plan.json','result.json'},'exact top file roles')
        expected_objects={'objects/%02d.o'%i for i in range(61)};expected_deps={'deps/%02d.%s.d'%(i,s) for i in range(61) for s in ('pre','post')}
        expected_logs={'logs/%02d-%s.log'%(i,s) for i in range(61) for s in ('pre','compile')}|{'logs/'+n+'.log' for n in ('link','syntax','wasm_validation')}
        for base,expected in (('objects',expected_objects),('deps',expected_deps),('logs',expected_logs)):
            require({p for p in actual['files'] if p.startswith(base+'/')}==expected and not any(d.startswith(base+'/') for d in actual['directories']),'owned '+base+' exact membership')
        return actual
    def command(self,argv,env,path,record):
        record.update(argv=argv,environment=env,exit_code=None,log=path,log_sha256=None,log_bytes=0,elapsed_ms=0,failure='NOT_COMPLETED',owned_process_reaped=False)
        try:outcome=self.effects.run(self,argv,env,path)
        except ProcessRefusal as e:record.update(e.record);raise
        keys(outcome,COMMAND,'actual command');record.update(outcome)
        require(record['argv']==argv and record['environment']==env and record['log']==path,'command effect identity')
        require(record['exit_code']==0 and type(record['exit_code']) is int and record['failure'] is None and record['owned_process_reaped'] is True,'command refused')
        integer(record['elapsed_ms'],0,120000);integer(record['log_bytes'],0,MAX_LOG)
        require(self.fs.record(path)['bytes']==record['log_bytes'] and self.fs.record(path)['sha256']==record['log_sha256'],'retained actual log identity')
        inspect_command_log(self.fs.read(path),self.fixture_only)
        return record
    def execute_candidate(self,id_,pins_path,pins_sha):
        self.started=time.monotonic()
        self.fs.whole_end=self.started+3600
        self.effects.whole_end=self.fs.whole_end
        self.context();attempt,publication=self.paths(id_);require(not self.fs.exists(attempt) and not self.fs.exists(publication),'fresh destinations')
        cfg,manifest,observed,rev,source,acceptance=self.observe();require(source is not None and acceptance is not None,'accepted complete source required')
        pins=self.authorization(id_,pins_path,pins_sha,observed);commands=self.commands(cfg,observed['units'],attempt);env=self.environment(attempt)
        require(time.monotonic()-self.started<3600,'whole build deadline before reservation')
        report=dict(schema_version=1,kind='CANDIDATE_BLACKWOOD_BUILD_RESULT',candidate_id=id_,recipe=RECIPE,ticket=pins['ticket'],status='INCOMPLETE',fixture_only=self.fixture_only,pins=dict(path=pins_path,sha256=pins_sha),source_revision=rev,source_manifest=source,source_acceptance=acceptance,observation=observed,environment=env,object_reuse=False,claims=CLAIMS.copy(),compiles=[],link={},syntax={},wasm_validation={},error=None,preload_validation=None,notices={},outputs={},bundle_id=None,metadata_sha256=None)
        self.reserved=[];owned=(attempt,publication)
        try:
            self.reserve(attempt,publication)
            for name in ('objects','deps','bundle','logs','tmp','node-cache'):self.fs.mkdir(attempt+'/'+name)
            # Immutable pre-execution plan; never updated to pretend authorization.
            plan=dict(schema_version=1,kind='BLACKWOOD_BUILD_PLAN',status='NOT_EXECUTED',recipe=RECIPE,candidate_id=id_,source_revision=rev,source_manifest=source,source_acceptance=acceptance,observation=observed,commands=commands,environment=env,claims=CLAIMS.copy(),pending=[])
            self.fs.write_new(attempt+'/plan.json',canonical(plan))
            require(time.monotonic()-self.started<3600,'whole build deadline before cache copy')
            self.effects.copy_cache(self,self.repo('web/build/.cache'),attempt+'/cache')
            require(inventory(self.fs,self.repo('web/build/.cache'))==inventory(self.fs,attempt+'/cache'),'physical own cache copy')
            def boundary():self.boundary(observed,owned,pins_path,pins_sha,pins)
            boundary()
            for i,unit in enumerate(commands['compiles']):
                row=dict(source=unit['source'],object=unit['object'],pre_depfile=unit['pre_depfile'],post_depfile=unit['post_depfile'],pre_scan={},compile={},pre_dependencies={},post_dependencies={},object_sha256=None);report['compiles'].append(row)
                self.command(unit['pre_command'],env,attempt+'/logs/%02d-pre.log'%i,row['pre_scan'])
                row['pre_dependencies']=self.dependencies(unit['pre_depfile'],attempt,observed)
                require(self.repo(unit['source']) in row['pre_dependencies'],'real source closure omitted')
                if unit['source'] in SOURCE_PINS and unit['source']!='source/src/browser_map_profile.h':require(self.repo('source/src/browser_map_profile.h') in row['pre_dependencies'],'T163 header missing actual consumer prescan')
                boundary();require(not self.fs.exists(unit['object']),'stale/reused object')
                self.command(unit['command'],env,attempt+'/logs/%02d-compile.log'%i,row['compile'])
                row['post_dependencies']=self.dependencies(unit['post_depfile'],attempt,observed)
                require(row['pre_dependencies']==row['post_dependencies'],'pre/post actual closure')
                require(self.fs.read(unit['object'])[:8]==MAGIC,'fresh Wasm object');row['object_sha256']=self.fs.record(unit['object'])['sha256'];boundary()
            for row in report['compiles']:
                require(self.fs.record(row['object'])['sha256']==row['object_sha256'] and self.dependencies(row['pre_depfile'],attempt,observed)==row['pre_dependencies'] and self.dependencies(row['post_depfile'],attempt,observed)==row['post_dependencies'],'late object/closure change before link')
            for name in ('link','syntax','wasm_validation'):
                boundary();self.command(commands[name],env,attempt+'/logs/'+name+'.log',report[name])
            report['preload_validation']=self.validate_payload(attempt+'/bundle',manifest);report['notices']=self.notices()
            self.fs.mkdir(attempt+'/bundle/notices')
            for n in NOTICE_PINS:self.fs.write_new(attempt+'/bundle/'+n,self.gate.read(self.repo('web/build/'+n)))
            report['outputs']={n:self.fs.record(attempt+'/bundle/'+n)['sha256'] for n in ARTIFACTS};report['status']=STATUS;report['bundle_id']=self.bundle_identity(report)
            metadata=dict(report);metadata.pop('metadata_sha256');self.fs.write_new(attempt+'/bundle/build-metadata.json',canonical(metadata));report['metadata_sha256']=digest(canonical(metadata))
            self.verify_bundle(attempt+'/bundle',manifest,report);boundary()
            self.fs.mkdir(publication+'/notices');self.fs.mkdir(publication+'/verification')
            for n in (*ARTIFACTS,'build-metadata.json',*NOTICE_PINS):self.fs.write_new(publication+'/'+n,self.fs.read(attempt+'/bundle/'+n))
            self.verify_bundle(publication,manifest,report,True);boundary()
            self.effects.report(report)  # includes flush, BEFORE final result/freeze/marker.
            self.fs.write_new(attempt+'/result.json',canonical(report));self.owned_layout(attempt,commands,True)
            elapsed=int((time.monotonic()-self.started)*1000);integer(elapsed,0,3600000)
            # Only path membership (not parent timestamps) is in this schema;
            # the direct freeze file and transient marker are literal exclusions.
            freeze=dict(schema_version=1,kind='BLACKWOOD_CANDIDATE_TERMINAL_FREEZE',candidate_id=id_,status=STATUS,attempt=inventory(self.fs,attempt,('freeze.json','failure.json')),publication=inventory(self.fs,publication,('verification/receipt.json',)),receipt_path='verification/receipt.json',elapsed_ms=elapsed)
            self.fs.write_new(attempt+'/freeze.json',canonical(freeze));self.fs.sync(publication);self.fs.sync(attempt)
            boundary()  # Reporting/terminal writes cannot hide a late protected change.
            require(time.monotonic()-self.started<3600,'whole deadline before final commit')
            self.fs.remove_marker(attempt+'/failure.json')  # FINAL REQUIRED EFFECT.
            return report
        except BaseException as e:
            report['status']='FAIL';report['error']=str(e)[:2048]
            if attempt in self.reserved:
                ledger=self.preserve_failure(attempt,report)
                if isinstance(e,ProcessRefusal):e.outer_ledger=ledger
            raise
    def preserve_failure(self,attempt,report):
        # A separate outer FAIL ledger uses only the remaining ORIGINAL whole
        # cutoff while refusal still dominates; never resume the child phase.
        cutoff=self.started+3600
        facts=dict(phase='OUTER_FAIL_LEDGER',cutoff_ms=int(cutoff*1000),status='SKIPPED')
        if time.monotonic()>=cutoff:facts['reason']='WHOLE_CUTOFF';return facts
        if not self.fs.exists(attempt+'/failure.json') or self.fs.exists(attempt+'/result.json'):
            facts['reason']='MARKER_MISSING_OR_RESULT_OCCUPIED';return facts
        try:
            facts['persistence']=self.fs.write_new(attempt+'/result.json',canonical(report),cutoff=cutoff);facts['status']='WRITTEN'
        except PersistenceRefusal as e:facts['status']='REFUSED';facts['persistence']=e.receipt
        except BaseException as e:facts['status']='REFUSED';facts['error']=error_text(e)
        return facts
    def verify_candidate(self,id_,pins_path,pins_sha,receipt=None):
        verification_end=time.monotonic()+3600;self.fs.whole_end=verification_end
        self.context();attempt,publication=self.paths(id_)
        require(not self.fs.exists(attempt+'/failure.json'),'refusal marker dominates')
        self.control_paths.add(absolute(pins_path));cfg,manifest,current,rev,source,acceptance=self.observe(owned=(attempt,publication))
        result=self.gate.json(attempt+'/result.json');keys(result,RESULT,'result');integer(result['schema_version'],1,1)
        require(result['kind']=='CANDIDATE_BLACKWOOD_BUILD_RESULT' and result['recipe']==RECIPE and result['candidate_id']==id_ and result['status']==STATUS and result['error'] is None,'successful fixed candidate result')
        require(type(result['fixture_only']) is bool and result['fixture_only']==self.fixture_only,'fixture cannot be real verification')
        require(equal(result['claims'],CLAIMS) and result['object_reuse'] is False,'no claims/reuse')
        observed=result['observation'];keys(observed,OBSERVATION,'result observation')
        for key in OBSERVATION-{'preservation'}:require(equal(observed[key],current[key]),'independent current '+key)
        self.protection_equal(observed['preservation'],current['preservation'],(attempt,publication))
        pins=self.authorization(id_,pins_path,pins_sha,observed,True)
        require(result['pins']==dict(path=pins_path,sha256=pins_sha) and result['ticket']==pins['ticket'] and result['source_revision']==rev and equal(result['source_manifest'],source) and equal(result['source_acceptance'],acceptance),'result independent authority/source')
        env=self.environment(attempt);commands=self.commands(cfg,list(UNITS),attempt);require(equal(result['environment'],env),'independent environment')
        plan=self.gate.json(attempt+'/plan.json');keys(plan,PLAN,'immutable plan')
        expected_plan=dict(schema_version=1,kind='BLACKWOOD_BUILD_PLAN',status='NOT_EXECUTED',recipe=RECIPE,candidate_id=id_,source_revision=rev,source_manifest=source,source_acceptance=acceptance,observation=observed,commands=commands,environment=env,claims=CLAIMS.copy(),pending=[])
        require(equal(plan,expected_plan),'immutable plan reconstructed')
        require(inventory(self.fs,self.repo('web/build/.cache'))==inventory(self.fs,attempt+'/cache'),'independent physical cache copy equality')
        self.owned_layout(attempt,commands)
        require(type(result['compiles']) is list and len(result['compiles'])==61,'61 actual unit results')
        def command(record,argv,path):
            keys(record,COMMAND,'COMMAND');integer(record['exit_code'],0,0);integer(record['elapsed_ms'],0,120000);integer(record['log_bytes'],0,MAX_LOG);sha_string(record['log_sha256'])
            require(record['argv']==argv and equal(record['environment'],env) and record['log']==path and record['failure'] is None and record['owned_process_reaped'] is True,'independent command/env/status/owned reap')
            row=self.fs.record(path);require(row['sha256']==record['log_sha256'] and row['bytes']==record['log_bytes'],'actual log identity')
            inspect_command_log(self.fs.read(path),self.fixture_only)
        for i,(row,unit) in enumerate(zip(result['compiles'],commands['compiles'])):
            keys(row,UNIT,'UNIT')
            for n in ('source','object','pre_depfile','post_depfile'):require(row[n]==unit[n],'regenerated unit '+n)
            command(row['pre_scan'],unit['pre_command'],attempt+'/logs/%02d-pre.log'%i);command(row['compile'],unit['command'],attempt+'/logs/%02d-compile.log'%i)
            before=self.dependencies(unit['pre_depfile'],attempt,observed);after=self.dependencies(unit['post_depfile'],attempt,observed)
            require(equal(before,after) and equal(before,row['pre_dependencies']) and equal(after,row['post_dependencies']) and self.repo(unit['source']) in before,'independent pre/post/source closure')
            if unit['source'] in SOURCE_PINS:require(self.repo('source/src/browser_map_profile.h') in before,'actual three consumer header closure')
            require(self.fs.record(unit['object'])['sha256']==row['object_sha256'] and self.fs.read(unit['object'])[:8]==MAGIC,'actual object bytes')
        for name in ('link','syntax','wasm_validation'):command(result[name],commands[name],attempt+'/logs/'+name+'.log')
        require(result['bundle_id']==self.bundle_identity(result),'independent bundle ID')
        self.verify_bundle(attempt+'/bundle',manifest,result);self.verify_bundle(publication,manifest,result,True)
        freeze=self.gate.json(attempt+'/freeze.json');keys(freeze,('schema_version','kind','candidate_id','status','attempt','publication','receipt_path','elapsed_ms'),'freeze')
        integer(freeze['schema_version'],1,1);integer(freeze['elapsed_ms'],0,3600000)
        require(freeze['kind']=='BLACKWOOD_CANDIDATE_TERMINAL_FREEZE' and freeze['candidate_id']==id_ and freeze['status']==STATUS and freeze['receipt_path']=='verification/receipt.json','terminal freeze identity')
        require(equal(freeze['attempt'],inventory(self.fs,attempt,('freeze.json','failure.json'))) and equal(freeze['publication'],inventory(self.fs,publication,('verification/receipt.json',))),'complete owned terminal inventories')
        def check_receipt(required=False):
            if self.fs.exists(target):
                require(self.gate.read(target)==canonical(doc),'fixed receipt canonical bytes')
                require(self.gate.record(target)==dict(bytes=len(canonical(doc)),sha256=digest(canonical(doc)),mode=420),'fixed receipt ordinary identity')
            else:require(not required and target not in self.gate.checked,'required or previously observed receipt missing')
        def final_gate(receipt_required=False):
            self.gate.recheck()
            _,_,latest,latest_rev,latest_source,latest_acceptance=self.observe(owned=(attempt,publication))
            for key in OBSERVATION-{'preservation'}:require(equal(observed[key],latest[key]),'verifier final observation '+key)
            self.protection_equal(observed['preservation'],latest['preservation'],(attempt,publication))
            require(latest_rev==rev and equal(latest_source,source) and equal(latest_acceptance,acceptance),'verifier final accepted source')
            require(equal(self.authorization(id_,pins_path,pins_sha,observed,True),pins),'verifier final authority')
            self.owned_layout(attempt,commands)
            require(equal(freeze['attempt'],inventory(self.fs,attempt,('freeze.json','failure.json'))) and equal(freeze['publication'],inventory(self.fs,publication,('verification/receipt.json',))),'verifier final complete owned inventories')
            check_receipt(receipt_required)  # Excluded inventory slot is still consumed evidence.
            self.gate.recheck()
            check_receipt(receipt_required)  # Also detect an absent slot appearing during rechecks.
            require(not self.fs.exists(attempt+'/failure.json'),'verifier final refusal marker dominates')
        doc=dict(schema_version=1,kind='BLACKWOOD_CANDIDATE_VERIFICATION_RECEIPT',candidate_id=id_,status='FIXTURE_ONLY' if self.fixture_only else 'VERIFIED_LINKED_NOT_BROWSER_VERIFIED',fixture_only=self.fixture_only,bundle_id=result['bundle_id'],pins_sha256=pins_sha,result_sha256=self.fs.record(attempt+'/result.json')['sha256'],freeze_sha256=self.fs.record(attempt+'/freeze.json')['sha256'],claims=CLAIMS.copy(),verifier_inputs={n:self.gate.record(self.HERE+'/'+n)['sha256'] for n in ('recipe.py','verify.py')})
        target=publication+'/verification/receipt.json'
        check_receipt()
        if receipt is not None:
            require(absolute(receipt)==target,'only fixed exclusive receipt path')
            final_gate()  # Do not publish a receipt from an already stale graph.
            if not self.fs.exists(target):self.fs.write_new(target,canonical(doc))
            check_receipt(True)
        final_gate(receipt is not None)  # Last observations include required receipt and marker absence.
        require(time.monotonic()<verification_end,'original independent verifier cutoff')
        return doc


class ProcessRefusal(RuntimeError):
    def __init__(self,record):self.record=record;super().__init__(str(record['failure']))

def reap_original_child(process,pid,deadline,publish):
    """D269/D271: strict consuming wait; no Popen ECHILD-to-zero fallback."""
    integer(pid,2,2**31-1)
    for observation in range(6000):
        require(time.monotonic()<deadline,'original consuming wait cutoff')
        require(type(process.pid) is int and process.pid==pid and process.returncode is None,'original unconsumed handle/PID')
        try:
            answer=os.waitpid(pid,os.WNOHANG)
        except OSError as error:
            if not (type(error.errno) is int and error.errno==4):raise
        else:
            require(type(answer) is tuple and len(answer)==2,'consuming wait tuple')
            found,status=answer
            require(type(found) is int and found in (0,pid) and type(status) is int and 0<=status<=65535,'consuming wait exact PID/status')
            if found==pid:
                if os.WIFEXITED(status):
                    code=os.WEXITSTATUS(status);require(status==code<<8,'canonical consumed exit status')
                elif os.WIFSIGNALED(status):
                    signal_number=os.WTERMSIG(status)
                    require(1<=signal_number<=127 and status in (signal_number,signal_number|128),'canonical consumed signal status');code=-signal_number
                else:raise ValueError('consuming wait nonterminal status')
                # Publish the actual consumption BEFORE checking post-call time.
                # Late consumption is still reaped, but never a successful run.
                process.returncode=code;publish(code)
                require(time.monotonic()<deadline,'late original consuming wait')
                require(type(process.pid) is int and process.pid==pid and type(process.returncode) is int and process.returncode==code,'consumed original handle changed')
                return code
            require(status==0,'nonterminal no-event status must be zero')
        remaining=deadline-time.monotonic();require(remaining>0,'original consuming wait cutoff after no-event/EINTR')
        if observation+1<6000:time.sleep(min(.01,remaining))
    raise TimeoutError('original consuming wait observation ceiling')

def error_text(e):
    try:return (type(e).__name__+': '+str(e))[:512]
    except BaseException:return 'error text unavailable'

class Effects:
    """Physical effects are future separately authorized execution only."""
    def copy_cache(self,recipe,source,target):
        require(recipe.started is not None and time.monotonic()-recipe.started<3600,'whole deadline before cache effects')
        recipe.fs.mkdir(target);found=inventory(recipe.fs,source)
        for d in sorted(found['directories'],key=lambda n:(n.count('/'),n)):
            require(time.monotonic()-recipe.started<3600,'whole deadline during cache directories');recipe.fs.mkdir(target+'/'+d)
        for p in found['files']:
            require(time.monotonic()-recipe.started<3600,'whole deadline during cache files');recipe.fs.copy_file(source+'/'+p,target+'/'+p)
    def report(self,result):
        require(time.monotonic()<self.whole_end,'original report cutoff')
        sys.stdout.write(canonical(dict(status=STATUS,candidate_id=result['candidate_id'],terminal_commit='PENDING')).decode())
        require(time.monotonic()<self.whole_end,'late report write; no expired flush')
        sys.stdout.flush();require(time.monotonic()<self.whole_end,'late report flush')
    def run(self,recipe,argv,env,log):
        # Retain the unreaped session leader as the group identity anchor.
        # No Popen poll/wait is permitted before anchored group cleanup.
        start=time.monotonic();hard=min(start+120,recipe.started+3600);work=hard-5
        p=None;selector=None;pid=None;primary=None;secondary=[];actions=[];output=bytearray();code=None;reaped=False;leader_exit=None;observer=None
        group=dict(anchor_acquired=False,anchor_confirmed_before_signal=False,signal_attempted=False,signal_result='NOT_ATTEMPTED',closure='NOT_ACQUIRED',closed=False,permission_observation=None)
        def budget():
            n=work-time.monotonic();require(n>0,'command work deadline');return n
        def attempt(label,call):
            actions.append(label)
            try:return call()
            except BaseException as e:secondary.append(dict(action=label,error=error_text(e)));return None
        def observe_leader(deadline=work):
            return observer(pid,deadline)
        try:
            budget()
            require(signal.getsignal(signal.SIGCHLD)==signal.SIG_DFL,'default SIGCHLD ownership required before launch')
            observer=make_nonreaping_observer();budget()
            p=subprocess.Popen(argv,cwd=recipe.ROOT,env=env,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
            pid=p.pid;require(type(pid) is int and pid>1,'owned leader PID');group['anchor_acquired']=True;group['closure']='ANCHORED_UNREAPED'
            budget();selector=selectors.DefaultSelector();os.set_blocking(p.stdout.fileno(),False);selector.register(p.stdout,selectors.EVENT_READ)
            while selector.get_map():
                for key,_ in selector.select(min(.05,budget())):
                    budget();block=os.read(key.fileobj.fileno(),65536)
                    if not block:selector.unregister(key.fileobj);continue
                    require(len(output)+len(block)<=MAX_LOG-SUPERVISOR_RESERVE,'command merged-log overflow');output.extend(block)
            while leader_exit is None:
                budget();leader_exit=observe_leader()
                if leader_exit is None:time.sleep(min(.01,budget()))
            budget();require(leader_exit==0,'command nonzero')
        except BaseException as e:primary=error_text(e)
        finally:
            if p is not None:
                cached_errors=len(secondary)
                cached=attempt('cached_returncode',lambda:p.returncode)
                if cached is not None:
                    group['closure']='UNRESOLVED_UNANCHORED_REAP';secondary.append(dict(action='cached_returncode',error='cached returncode is not verified original consumption'))
                anchored=False;anchor_exit=None
                if group['anchor_acquired'] and cached is None and len(secondary)==cached_errors and not reaped and time.monotonic()<hard:
                    try:
                        actions.append('confirm_unreaped_anchor');anchor_exit=observe_leader(hard);anchored=True;group['anchor_confirmed_before_signal']=True
                    except BaseException as e:
                        secondary.append(dict(action='confirm_unreaped_anchor',error=error_text(e)));group['closure']='UNRESOLVED_ANCHOR'
                if anchored:
                    def kill():
                        require(time.monotonic()<hard,'no remaining signal time');require(type(p.pid) is int and p.pid==pid,'original group handle before signal');group['signal_attempted']=True
                        try:os.killpg(pid,signal.SIGKILL);group['signal_result']='SENT_ANCHORED'
                        except ProcessLookupError:group['signal_result']='ABSENT_ANCHORED';group['closed']=True;group['closure']='ABSENT_ANCHORED'
                        except PermissionError as e:
                            # D263: this observation is UNKNOWN, never absence or
                            # permission to retry a signal. Only a fresh native
                            # terminal0 on this still-waitable original qualifies.
                            if not (type(e.errno) is int and e.errno==1 and type(anchor_exit) is int and anchor_exit==0 and type(p.pid) is int and p.pid==pid and p.returncode is None and time.monotonic()<hard):raise
                            group['permission_observation']=dict(phase='PRE_REAP_SIGNAL',errno=1,pid=pid,terminal_exit_code=0,mutating_signal_attempted=True,message=error_text(e)[:240],resolution='UNRESOLVED')
                            group['signal_result']='TERMINAL_EPERM_UNKNOWN';group['closure']='UNRESOLVED_TERMINAL_EPERM'
                    attempt('kill_owned_group',kill)
                elif group['anchor_acquired'] and not reaped:
                    secondary.append(dict(action='kill_owned_group',error='no confirmed live ownership anchor or remaining deadline; not signaled'))
                if not reaped:
                    def wait():
                        nonlocal code,reaped
                        def consumed(value):
                            nonlocal code,reaped
                            code=value;reaped=True
                        reap_original_child(p,pid,hard,consumed)
                        require(code==0,'consumed original command nonzero/signal exit')
                    if time.monotonic()<hard:attempt('wait_original_handle',wait)
                    else:secondary.append(dict(action='wait_original_handle',error='deadline exhausted, unresolved'))
                if group['anchor_confirmed_before_signal'] and group['signal_attempted'] and reaped and not group['closed']:
                    # Read-only absence probes only. A surviving/reused PGID is
                    # ambiguous after reap: it is NEVER sent another kill signal.
                    def closure():
                        if group['permission_observation'] is not None:
                            require(time.monotonic()<hard and type(p.pid) is int and p.pid==pid and type(code) is int and code==0,'timely original terminal permission reap')
                            # The FIRST distinct post-reap observation must be
                            # ESRCH. PRESENT/EPERM/unknown are final refusals,
                            # not a retry loop and never post-reap mutation.
                            try:os.killpg(pid,0)
                            except ProcessLookupError:
                                require(time.monotonic()<hard,'late terminal permission closure')
                                group['closed']=True;group['closure']='ABSENT_AFTER_TERMINAL_EPERM';group['permission_observation']['resolution']='POST_REAP_ABSENT';return
                            raise ValueError('first terminal permission post-reap observation PRESENT')
                        while time.monotonic()<hard:
                            try:os.killpg(pid,0)
                            except ProcessLookupError:group['closed']=True;group['closure']='ABSENT_AFTER_ANCHORED_CLEANUP';return
                            group['closure']='UNRESOLVED_POST_REAP_GROUP'
                            time.sleep(min(.01,max(0,hard-time.monotonic())))
                        raise TimeoutError('owned group closure unresolved before absolute deadline')
                    attempt('observe_group_absence',closure)
            unresolved_release=False
            def release(label,call):
                nonlocal unresolved_release
                if time.monotonic()>=hard:
                    actions.append(label+'_SKIPPED_EXPIRED');secondary.append(dict(action=label,error='SKIPPED_EXPIRED_UNRESOLVED'));unresolved_release=True
                else:
                    prior=len(secondary);attempt(label,call)
                    if len(secondary)!=prior:unresolved_release=True
            if selector is not None:release('selector_close',selector.close)
            if p is not None:
                for name in ('stdin','stdout','stderr'):
                    def close(name=name):
                        pipe=getattr(p,name)
                        if pipe is not None and not pipe.closed:pipe.close()
                    release(name+'_close',close)
            if p is not None and (unresolved_release or not reaped):UNRESOLVED_HANDLES.append(dict(phase='COMMAND_CLEANUP',cutoff=hard,process=p,selector=selector))
        if time.monotonic()>=hard and primary is None:primary='operation deadline including cleanup'
        if (not reaped or not group['closed']) and primary is None:primary='original handle or owned group unresolved'
        state=dict(schema_version=1,kind='BLACKWOOD_COMMAND_SUPERVISOR',fixture_only=recipe.fixture_only,pid=pid,leader_exit_observed=leader_exit,original_handle_reaped=reaped,exit_code=code,group=group,primary=primary,cleanup=secondary,cleanup_actions=actions,child_log_bytes=len(output),child_log_sha256=digest(output),hard_deadline_ms=int(hard*1000),work_deadline_ms=int(work*1000))
        encoded=bytes(output)+SUPERVISOR_FRAME+canonical(state)
        require(len(encoded)<=MAX_LOG,'bounded supervisor log frame')
        record=dict(argv=argv,environment=env,exit_code=code,log=log,log_sha256=digest(encoded),log_bytes=len(encoded),elapsed_ms=0,failure=canonical(state).decode() if primary or secondary or not reaped or not group['closed'] else None,owned_process_reaped=reaped)
        # Snapshot and raw child-prefix facts exist before fallible retention.
        # No normal command persistence starts after its original hard cutoff.
        if time.monotonic()>=hard:
            state['retention']=dict(status='SKIPPED_COMMAND_CUTOFF',opened=False,written_bytes=0,planned_bytes=len(encoded));record['log_bytes']=0;record['log_sha256']=None
            if state['primary'] is None:state['primary']='command cutoff before persistence'
            record['failure']=canonical(state).decode()
        else:
            try:recipe.fs.write_new(log,encoded,cutoff=hard)
            except PersistenceRefusal as e:
                state['retention']=e.receipt;record['log_bytes']=e.receipt['written_bytes'];record['log_sha256']=None if e.receipt['write_return_unresolved'] else e.receipt['known_prefix_sha256'];record['failure']=canonical(state).decode()
            except BaseException as e:state['retention']=dict(error=error_text(e),retained_identity='UNRESOLVED');record['log_bytes']=0;record['log_sha256']=None;record['failure']=canonical(state).decode()
        ended=time.monotonic()
        if ended>=hard:state['late_retention']=True;record['failure']=canonical(state).decode()
        record['elapsed_ms']=int((ended-start)*1000)  # Inclusive through retention/eligible releases.
        if record['failure'] is not None:raise ProcessRefusal(record)
        return record

def build_parser():
    p=argparse.ArgumentParser(description='Fixed Blackwood planning or separately MAIN-released execution')
    mode=p.add_mutually_exclusive_group(required=True);mode.add_argument('--plan-only',action='store_true');mode.add_argument('--execute',action='store_true')
    p.add_argument('--candidate-id',required=True);p.add_argument('--pins');p.add_argument('--pins-sha256');return p

def build_main(argv=None):
    args=build_parser().parse_args(argv);recipe=Recipe();identifier(args.candidate_id)
    if args.execute:
        require(args.pins is not None and args.pins_sha256 is not None,'pins AND digest required')
        recipe.execute_candidate(args.candidate_id,args.pins,args.pins_sha256)
    else:
        require(args.pins is None and args.pins_sha256 is None,'plan refuses execution controls');require(args.candidate_id!='1','reserved preparation-1 evidence')
        doc=recipe.plan(args.candidate_id);target=recipe.HERE+'/tests/preparation-'+args.candidate_id
        require(not recipe.fs.exists(target),'exclusive plan output');recipe.fs.mkdir(target);recipe.fs.write_new(target+'/plan.json',canonical(doc))
        sys.stdout.write(canonical(dict(status='NOT_EXECUTED',plan=target+'/plan.json')).decode());sys.stdout.flush()
    return 0

def verify_main(argv=None):
    p=argparse.ArgumentParser(description='Read-only Blackwood linked-candidate reconstruction; no child processes')
    p.add_argument('--candidate-id',required=True);p.add_argument('--pins',required=True);p.add_argument('--pins-sha256',required=True);p.add_argument('--receipt')
    args=p.parse_args(argv);doc=Recipe().verify_candidate(args.candidate_id,args.pins,args.pins_sha256,args.receipt)
    sys.stdout.write(canonical(dict(status=doc['status'],candidate_id=args.candidate_id)).decode());sys.stdout.flush();return 0
