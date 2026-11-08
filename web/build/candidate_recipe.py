"""T088 fixed network_v1 candidate gates. No effects occur on import/discovery.

Private result/freeze schema: tests/candidate/SCHEMA.md. Historical Recipe is
composed read-only; its config, flags, backend, payload and alias gates remain.
"""
import argparse
import hashlib
import importlib.util
import json
import os
from pathlib import Path
import re
import selectors
import shutil
import signal
import stat
import subprocess
import sys
import time

from profile_client import Recipe

ID = re.compile(r'[A-Za-z0-9_-]{1,48}\Z')
SHA = re.compile(r'[0-9a-f]{64}\Z')
REV = re.compile(r'[0-9a-f]{40}\Z')
OBSERVATION = {'inputs','preservation','units','ports','aliases','alias_decisions','pack','tool_errors'}
AUTHORIZATION = {'schema_version','kind','authority','status','execution_release','recipe','ticket',
                 'candidate_id','decision','source_revision','source_manifest','bindings','observation'}
CLAIMS = dict(runtime=False, audio=False, model=False, multiplayer=False, authority=False, P0=False)
STATUS = 'LINKED_NOT_BROWSER_VERIFIED'
MAX_JSON = 32 * 1024 * 1024
MAX_LOG = 8 * 1024 * 1024


def require(value, message):
    if not value:
        raise ValueError(message)


def canonical(value):
    return json.dumps(value, sort_keys=True, indent=2, ensure_ascii=True, allow_nan=False) + '\n'


def digest_bytes(value):
    return hashlib.sha256(value).hexdigest()


def load_json(path):
    path = absolute(path)
    require(stat.S_ISREG(path.stat().st_mode), 'ordinary JSON file required')
    require(Path(path).stat().st_size <= MAX_JSON, 'JSON size limit')
    def pairs(items):
        result = {}
        for key, value in items:
            require(key not in result, 'duplicate JSON key: ' + key)
            result[key] = value
        return result
    return json.loads(Path(path).read_text(encoding='utf8'), object_pairs_hook=pairs,
        parse_constant=lambda _: (_ for _ in ()).throw(ValueError('nonfinite JSON')))


def keys(value, expected, label):
    require(type(value) is dict and set(value) == set(expected), label + ' exact fields')


def exact(a, b):
    if type(a) is not type(b):
        return False
    if type(a) is dict:
        return set(a)==set(b) and all(exact(a[k],b[k]) for k in a)
    if type(a) is list:
        return len(a)==len(b) and all(exact(x,y) for x,y in zip(a,b))
    return a==b


def integer(value, minimum, maximum, label):
    require(type(value) is int and minimum <= value <= maximum, label + ' integer/range')


def relative(name):
    require(type(name) is str and bool(name) and '\\' not in name and '\x00' not in name,
            'canonical relative member required')
    p = Path(name)
    require(not p.is_absolute() and str(p) == name and not any(x in ('.','..') for x in p.parts),
            'canonical relative member required')
    return p


def absolute(path):
    p = Path(path)
    require(p.is_absolute() and str(p) == str(path) and '..' not in p.parts,
            'canonical absolute path required')
    require(not any(x.is_symlink() for x in (p, *p.parents)), 'undeclared symlink: ' + str(p))
    return p


def write_new(path, value):
    path = absolute(path)
    with path.open('x', encoding='utf8') as stream:
        stream.write(canonical(value))


def file_record(path):
    path = absolute(path)
    require(path.is_file() and stat.S_ISREG(path.stat().st_mode), 'ordinary file required: ' + str(path))
    h = hashlib.sha256()
    with path.open('rb') as stream:
        for chunk in iter(lambda: stream.read(1024*1024), b''):
            h.update(chunk)
    return dict(bytes=path.stat().st_size, sha256=h.hexdigest(), mode=stat.S_IMODE(path.stat().st_mode))


def inventory(root, excluded=()):
    """Exact ordinary file AND directory membership; exclusions are literal files."""
    root = absolute(root)
    require(root.is_dir(), 'inventory directory missing: ' + str(root))
    excluded = set(excluded)
    files, directories = {}, []
    for parent, dirs, names in os.walk(root, followlinks=False):
        for name in dirs:
            p = absolute(Path(parent) / name)
            require(p.is_dir(), 'ordinary directory required')
            directories.append(str(p.relative_to(root)))
        for name in names:
            p = absolute(Path(parent) / name)
            member = str(p.relative_to(root))
            if member not in excluded:
                files[member] = file_record(p)
    return dict(files=dict(sorted(files.items())), directories=sorted(directories))


def protected_tree(root):
    """D091: preserve historical links opaquely; NEVER traverse/approve them."""
    root=Path(root)
    absolute(root.parent)
    files,dirs,links={},{},{}
    def inspect(path):
        mode=path.lstat().st_mode
        if stat.S_ISLNK(mode):
            links[str(path)]=dict(target=os.readlink(path),mode=stat.S_IMODE(mode))
            return 'link'
        absolute(path)
        if stat.S_ISDIR(mode):
            dirs[str(path)]=True; return 'directory'
        require(stat.S_ISREG(mode),'nonordinary protected object: '+str(path))
        files[str(path)]=file_record(path)['sha256']; return 'file'
    try:
        kind=inspect(root)
    except FileNotFoundError:
        return dict(files={},directories=[],links={},absent_roots=[str(root)])
    if kind=='directory':
        for parent,names,leafs in os.walk(root,followlinks=False):
            keep=[]
            for name in names:
                path=Path(parent) / name
                if inspect(path)=='directory': keep.append(name)
            names[:]=keep
            for name in leafs: inspect(Path(parent) / name)
    return dict(files=files,directories=sorted(dirs),links=links,absent_roots=[])


def read_head(root):
    # Read Git metadata, never run git/subprocess from observation.
    directory = root / '.git'
    if directory.is_file():
        text = directory.read_text().strip()
        require(text.startswith('gitdir: '), 'invalid git directory reference')
        directory = (root / text[8:]).resolve()
    directory = absolute(directory)
    common = directory
    if (directory / 'commondir').is_file():
        common = absolute((directory / (directory / 'commondir').read_text().strip()).resolve())
    value = (directory / 'HEAD').read_text().strip()
    visited = set()
    while value.startswith('ref: '):
        ref = value[5:]
        relative(ref)
        require(ref.startswith('refs/') and ref not in visited, 'invalid/cyclic HEAD reference')
        visited.add(ref)
        target = next((base / ref for base in (directory, common) if (base / ref).is_file()), None)
        if target:
            value = absolute(target).read_text().strip()
        else:
            packed = absolute(common / 'packed-refs').read_text().splitlines()
            found = [line.split()[0] for line in packed if line and not line.startswith(('#','^'))
                     and len(line.split()) == 2 and line.split()[1] == ref]
            require(len(found) == 1, 'HEAD reference missing')
            value = found[0]
    require(REV.fullmatch(value) is not None, 'HEAD revision format')
    return value


def parse_dependencies(path, cwd):
    """Parse one compiler Make dependency rule, retaining system headers (-M/-MD)."""
    text = Path(path).read_text().replace('\\\n', '')
    escaped, colon = False, None
    for index,char in enumerate(text):
        if escaped:
            escaped=False
        elif char=='\\':
            escaped=True
        elif char==':':
            colon=index; break
    require(colon is not None and bool(text[:colon].strip()), 'dependency target missing')
    token, tokens, escaped = '', [], False
    for char in text[colon+1:]:
        if escaped:
            token += char; escaped = False
        elif char == '\\':
            escaped = True
        elif char.isspace():
            if token:
                tokens.append(token.replace('$$', '$')); token = ''
        else:
            token += char
    if token:
        tokens.append(token.replace('$$', '$'))
    require(not escaped and bool(tokens), 'malformed dependency rule')
    result = []
    for token in tokens:
        p = Path(token)
        if not p.is_absolute():
            p = cwd / p
        require('..' not in p.parts, 'noncanonical compiler dependency')
        result.append(p)
    require(len(set(result)) == len(result), 'duplicate compiler dependency')
    return sorted(result)


class CandidateRecipe(Recipe):
    """Only network_v1; CLI roots/flags/commands cannot be supplied by a document."""
    fixture_only = False

    def __init__(self):
        super().__init__('network')
        self.ROOT = absolute(Path(__file__).absolute().parents[2])
        self.HERE = self.ROOT / 'web/build'
        self.CONFIG = self.HERE / 'network-config.json'
        self.started = None

    def paths(self, candidate_id):
        require(type(candidate_id) is str and ID.fullmatch(candidate_id), 'invalid candidate ID')
        return (absolute(self.HERE / 'candidate-attempts' / candidate_id),
                absolute(self.HERE / 'candidates' / candidate_id))

    def config(self):
        load_json(self.CONFIG); load_json(self.HERE / 'client-config.json')
        cfg = Recipe.config(self)
        keys(cfg,{'ticket','sdk_root','sdk_version','compiler_revision','common_cxx','common_c','ports','link',
                  'libpng_sha512','profile','manifest','pack_root','output','attempt_root','js_library'},'fixed network config')
        fixed = dict(sdk_root='/private/tmp/outbreak-web-sdk', sdk_version='7.0.0',
            compiler_revision='777e6e5db7b4990bcaeb1b9998ed642cc84e6629',
            libpng_sha512='e14302d87864432d747896e3944a6416d4b5f3059f538cfe615ddbe1d0084d4a02d4df3ef2761b02c839858625bed57d873198792c3583029c619e1cf8c4561b',
            common_cxx=['--target=wasm32-unknown-emscripten','-std=gnu++11','-fsigned-char','-O2','-DOUTBREAK_NETWORK_CLIENT'],
            common_c=['--target=wasm32-unknown-emscripten','-O2','-DHAS_SOCKLEN_T=1','-std=gnu11','-fsigned-char','-DOUTBREAK_NETWORK_CLIENT'],
            ports=['-sUSE_SDL=2','-sUSE_SDL_IMAGE=2','-sSDL2_IMAGE_FORMATS=["png"]','-sUSE_ZLIB=1','-sUSE_VORBIS=1'],
            link=['-O2','-lopenal','-sLEGACY_GL_EMULATION=1','-sGL_UNSAFE_OPTS=0','-sALLOW_MEMORY_GROWTH=1',
                  '-sINITIAL_MEMORY=67108864','-sSTACK_SIZE=2097152'])
        for key,value in fixed.items():
            require(cfg.get(key) == value, 'fixed network_v1 flag/tool changed: ' + key)
        return cfg

    def repository_inputs(self, cfg):
        # Deliberately no web/runtime/tests or worker diagnostics: no compiler
        # includes them. Actual -M/-MD closure must still pass for every unit.
        names = ['profile_client.py','verify_audio_bundle.py','client-config.json','build_client.py',
                 'verify_client_bundle.py','compile_probe.py','preflight.py','shell.html',
                 'sdk-inspection/sources-and-artifacts.json','build_audio_client.py',
                 'build_network_client.py','verify_network_bundle.py','network-shell.html','audio-config.json',
                 'network-config.json','candidate_recipe.py','build_candidate.py','verify_candidate.py']
        paths = [self.HERE / name for name in names] + [self.repo('source/src/Makefile'),self.repo('source/src/ge25519_base.data')]
        paths += [self.repo(name) for name in self.network_backend()]
        paths += [self.repo(name) for name in self.units()]
        for base in ('source/src','source/enet'):
            paths += [p for p in self.files(self.repo(base)) if p.suffix in ('.h','.hpp','.inc','.inl')]
        paths += [self.clean(p) for p in sorted(self.repo('web/transport').iterdir())
                  if p.suffix in ('.h','.hpp','.inc','.inl')]
        paths += [self.HERE / ('tests/candidate/'+name) for name in ('test_candidate.py','SCHEMA.md','README.md')]
        helper = self.ROOT / 'web/assets/network-profile'
        paths += [helper / n for n in ('manifest.json','anchors.json','map_format.py',
                                      'build_network_profile.py','validate_network_profile.py')]
        paths += self.files(helper / 'pack-root') + [self.ROOT / 'web/assets/original/validate_pack.py']
        paths += self.files(self.HERE / 'notices')
        for name in ('original','audio','models','media-profile','audio-profile'):
            base = self.ROOT / 'web/assets' / name
            paths += [base / 'manifest.json'] + self.files(base / 'pack-root')
        paths += [self.ROOT / 'web/assets/audio-profile/check_profile.py',
                  self.ROOT / 'web/assets/audio-profile/build_profile.py',
                  self.ROOT / 'web/assets/media-profile/assemble.py']
        return self.snapshot(paths)

    def protection_roots(self):
        return [self.HERE / name for name in ('out','audio-out','network-out','.cache','generated',
                  'tests','candidate-attempts','candidates')] + [self.ROOT / name for name in
                  ('web/server/out','web/server/out-lifecycle','web/server/out-signed','web/server/deps-signed',
                   'web/server/run','web/runtime/tests','web/player/tests','web/transport/results','tests/outbreak')]

    def preservation(self, owned=()):
        # Original Recipe file protection remains a subset; add historical build
        # attempts/candidates, directories and originally absent roots explicitly.
        files,links={},{}
        directories, absent = [], []
        for root in self.protection_roots():
            tree=protected_tree(root)
            files.update(tree['files']); links.update(tree['links'])
            directories+=tree['directories']; absent+=tree['absent_roots']
        # Same original source-object/binary selection as Recipe.preservation,
        # but lstat preserves qualifying historical links instead of following.
        source=self.ROOT / 'source'
        if source.exists():
            absolute(source)
            for parent,names,leafs in os.walk(source,followlinks=False):
                for name in names+leafs:
                    path=Path(parent) / name
                    if path.suffix in ('.o','.lo','.a','.gch','.pch') or name in ('ac_client','ac_server','ac_master'):
                        tree=protected_tree(path)
                        files.update(tree['files']); links.update(tree['links'])
        for path in owned:
            files = {p: h for p,h in files.items() if not Path(p).is_relative_to(path)}
            links = {p: h for p,h in links.items() if not Path(p).is_relative_to(path)}
            directories = [p for p in directories if not Path(p).is_relative_to(path)]
        return dict(files=dict(sorted(files.items())),directories=sorted(set(directories)),
                    links=dict(sorted(links.items())),absent_roots=sorted(set(absent)))

    def manifest_document(self, revision):
        path = self.repo('web/repro/source-manifest.json')
        doc = load_json(path)
        keys(doc, {'schema_version','kind','source_revision','entries'}, 'source manifest')
        integer(doc['schema_version'],1,1,'manifest schema')
        require(doc['kind'] == 'SOURCE_INPUT_MANIFEST' and doc['source_revision'] == revision, 'manifest kind/revision')
        require(type(doc['entries']) is list, 'source entries array')
        names = []
        for row in doc['entries']:
            keys(row, {'path','bytes','sha256','mode'}, 'source entry')
            name = row['path']; relative(name)
            require(name != 'web/repro/source-manifest.json', 'recursive source manifest')
            integer(row['bytes'],0,2**63-1,'source bytes')
            integer(row['mode'],420,493,'source mode')
            require(row['mode'] in (420,493) and type(row['sha256']) is str and SHA.fullmatch(row['sha256']), 'source identity/mode')
            require(file_record(self.repo(name)) == {k: row[k] for k in ('bytes','sha256','mode')}, 'source bytes/hash/mode changed')
            names.append(name)
        require(names == sorted(set(names)), 'source entries unique sorted')
        return doc

    def source_manifest(self, observed, revision):
        path=self.repo('web/repro/source-manifest.json')
        doc=self.manifest_document(revision)
        names={row['path'] for row in doc['entries']}
        consumed = {str(Path(p).relative_to(self.ROOT)) for p in self.repository_inputs(self.config())}
        # Authority decisions and SDK alias provenance are explicit source files.
        consumed |= set(observed['alias_decisions'])
        require(consumed <= names, 'source manifest missing consumed members')
        return dict(path='web/repro/source-manifest.json', sha256=self.sha(path))

    def configuration_json_paths(self,cfg,decisions):
        # Parse documents the recipe actually interprets, not opaque SDK/cache
        # JSON test resources that are merely hash-bound tool bytes.
        paths=[self.CONFIG,self.HERE / 'client-config.json',self.HERE / 'audio-config.json',
               self.HERE / 'sdk-inspection/sources-and-artifacts.json',
               self.repo(cfg['manifest']),self.repo('web/assets/network-profile/anchors.json')]
        paths += [self.repo('web/assets/'+name+'/manifest.json') for name in
                  ('original','audio','models','media-profile','audio-profile')]
        paths += [self.repo(name) for name in decisions]
        return sorted(set(paths))

    def observe(self, strict=True, owned=()):
        cfg, manifest, observed = super().observe(strict=strict)
        observed['preservation'] = self.preservation(owned)
        # Authoring tools are bytes too, not only the Python executable. Imported
        # framework stdlib/extension modules are deterministic for these entrypoints.
        python_root = Path(sys.base_prefix).resolve()
        authoring = []
        for module in tuple(sys.modules.values()):
            filename = getattr(module,'__file__',None)
            if not filename:
                continue
            p = Path(filename).resolve()
            if p.suffix == '.pyc':
                p = Path(importlib.util.source_from_cache(str(p)))
            if p.is_relative_to(python_root) and p.is_file() and 'site-packages' not in p.parts:
                authoring.append(p)
        observed['inputs'].update(self.snapshot(authoring))
        # Full frozen cache is a compiler prerequisite closure, not reused game objects.
        observed['inputs'].update(self.snapshot(self.files(self.HERE / '.cache')))
        for path in self.configuration_json_paths(cfg,observed['alias_decisions']):
            load_json(path)
        source_path = self.repo('web/repro/source-manifest.json')
        if source_path.exists():
            source = self.manifest_document(read_head(self.ROOT))
            for row in source['entries']:
                observed['inputs'][str(self.repo(row['path']))] = row['sha256']
            observed['inputs'][str(source_path)] = self.sha(source_path)
        require(set(observed) == OBSERVATION, 'observation exact fields')
        return cfg, manifest, observed

    def plan(self, candidate_id):
        attempt, publication = self.paths(candidate_id)
        require(not attempt.exists() and not publication.exists(), 'candidate destination exists')
        cfg, manifest, observed = self.observe(strict=False)
        revision = read_head(self.ROOT)
        source_path=self.repo('web/repro/source-manifest.json')
        binding = self.source_manifest(observed, revision) if source_path.exists() else None
        proposal=self.repository_inputs(cfg)
        proposal.update({str(self.repo(name)):self.sha(self.repo(name)) for name in observed['alias_decisions']})
        if binding:
            for row in load_json(source_path)['entries']:
                proposal[str(self.repo(row['path']))]=row['sha256']
        entries=[dict(path=str(Path(p).relative_to(self.ROOT)),**file_record(Path(p))) for p in sorted(proposal)]
        commands = self.candidate_commands(cfg, observed['units'], attempt)
        return dict(schema_version=1,kind='CANDIDATE_PREPARATION',status='NOT_EXECUTED',
            accepted_source_pins=False,execution_ready=False,candidate_id=candidate_id,recipe='network_v1',
            source_revision=revision,source_manifest=binding,observation=observed,
            source_manifest_error=None if binding else 'PENDING_MAIN_SOURCE_MANIFEST',proposed_source_entries=entries,
            attempt=str(attempt),publication=str(publication),commands=commands,
            environment=self.environment(cfg,attempt),claims=CLAIMS.copy(),fixture_only=self.fixture_only)

    def authorization(self, candidate_id, path, expected_sha, observed, completed=False):
        attempt, publication = self.paths(candidate_id)
        require(path is not None and type(expected_sha) is str and SHA.fullmatch(expected_sha), 'pins path AND digest required')
        path = absolute(path)
        require(path.parent == self.ROOT / 'notes/decisions' and path.suffix == '.json', 'MAIN decision pins path required')
        require(stat.S_ISREG(path.stat().st_mode) and path.stat().st_size<=MAX_JSON,'ordinary bounded pins required')
        require(self.sha(path) == expected_sha, 'pins digest mismatch')
        doc = load_json(path); keys(doc,AUTHORIZATION,'authorization')
        integer(doc['schema_version'],1,1,'authorization schema')
        require(doc['kind'] == 'CANDIDATE_NETWORK_BUILD_AUTHORIZATION' and doc['authority'] == 'MAIN'
                and doc['status'] == 'ACCEPTED' and doc['execution_release'] == 'EXPLICIT_CANDIDATE_NETWORK_BUILD_EXECUTION'
                and doc['recipe'] == 'network_v1' and doc['candidate_id'] == candidate_id, 'explicit MAIN execution identity')
        ticket = doc['ticket']
        require(type(ticket) is str and 0 < len(ticket) <= 64 and ticket.isascii() and ticket.strip() == ticket,
                'execution ticket ASCII provenance')
        decision = self.repo(doc['decision'])
        require(decision.parent == self.ROOT / 'notes/decisions' and decision.suffix == '.md', 'decision path')
        require(observed['inputs'].get(str(decision)) == self.sha(decision), 'decision not bound in observation inputs')
        revision = read_head(self.ROOT)
        require(doc['source_revision'] == revision and REV.fullmatch(revision), 'HEAD/source revision differs')
        keys(doc['source_manifest'],{'path','sha256'},'source manifest binding')
        require(doc['source_manifest'] == self.source_manifest(observed,revision), 'source manifest binding differs')
        manifest=load_json(self.repo('web/repro/source-manifest.json'))
        require(doc['decision'] in {r['path'] for r in manifest['entries']},'source manifest missing authorization decision')
        keys(doc['bindings'],{'repository','sdk','ports_cache'},'root bindings')
        require(doc['bindings'] == dict(repository=str(self.ROOT),sdk='/private/tmp/outbreak-web-sdk',
                ports_cache=str(self.HERE / '.cache')), 'fixed canonical root bindings')
        keys(doc['observation'],OBSERVATION,'observation')
        require(exact(doc['observation'],observed) and observed['tool_errors'] == [], 'complete current observation differs')
        if not completed:
            require(not attempt.exists() and not publication.exists(), 'candidate already reserved')
        return doc

    def candidate_commands(self, cfg, units, attempt):
        compiles, link, syntax = Recipe.commands(self,cfg,units,attempt)
        for index, row in enumerate(compiles):
            # -MD includes system headers; pre-scan -M uses the identical frozen
            # flags/includes/ports, without compiling an object or changing recipe.
            dep = attempt / 'deps' / f'{index:02}.post.d'
            pre = attempt / 'deps' / f'{index:02}.pre.d'
            command = row['command']
            require(command[-4:] == ['-c',str(self.ROOT / row['source']),'-o',row['object']], 'fixed compile suffix')
            row['pre_command'] = command[:-4] + ['-M','-MF',str(pre),'-MT',row['object'],str(self.ROOT / row['source'])]
            row['command'] = command + ['-MD','-MF',str(dep)]
            row['pre_depfile'],row['post_depfile'] = str(pre),str(dep)
        return dict(compiles=compiles,link=link,syntax=syntax,wasm_validation=self.wasm_command(cfg,attempt))

    def stable(self, observed, owned, baseline):
        _, _, current = self.observe(owned=owned)
        for key in OBSERVATION - {'preservation'}:
            require(current[key] == observed[key], 'late changed observation: ' + key)
        self.protection_equal(baseline,current['preservation'],owned)

    def protection_equal(self, baseline, current, owned):
        keys(baseline,{'files','directories','links','absent_roots'},'baseline protection')
        keys(current,{'files','directories','links','absent_roots'},'current protection')
        require(exact(current['files'],baseline['files']), 'original protected byte/membership differs')
        require(exact(current['links'],baseline['links']), 'opaque historical link membership/text/mode differs')
        # Container directories can be created solely to reserve the two new
        # direct children. Everything else, including empty directories, is exact.
        allowed_parents = {str(p.parent) for p in owned}
        require(set(current['directories']) - set(baseline['directories']) <= allowed_parents,
                'extra original protected directory')
        require(set(baseline['directories']) <= set(current['directories']), 'missing protected directory')
        require(set(baseline['absent_roots']) - set(current['absent_roots']) <= allowed_parents,
                'unexpected formerly absent protected root')
        require(set(current['absent_roots']) <= set(baseline['absent_roots']), 'protected root removed')

    def dependencies(self, path, attempt, observed):
        result = {}
        for actual in parse_dependencies(path,self.ROOT):
            if actual.is_relative_to(attempt / 'cache'):
                original = self.HERE / '.cache' / actual.relative_to(attempt / 'cache')
            else:
                original = actual
            # Only decision-declared aliases can be compiler input aliases.
            try:
                actual = absolute(actual)
            except ValueError:
                declared = next((r for r in observed['aliases'] if r['path'] == str(actual)),None)
                require(declared is not None, 'undeclared compiler dependency alias')
                actual = absolute(declared['resolved_path']); original = actual
            expected = observed['inputs'].get(str(original))
            require(expected is not None and self.sha(actual) == expected, 'new/changed/undeclared compiler dependency: ' + str(original))
            result[str(original)] = expected
        return result

    def reserve(self, attempt, publication):
        # Preflight BOTH before any reservation. mkdir itself is exclusive; a
        # race loses safely and retains any first reserved failed attempt.
        require(not attempt.exists() and not publication.exists(), 'destination exists before effects')
        for parent in (attempt.parent,publication.parent):
            absolute(parent); parent.mkdir(parents=True,exist_ok=True)
        attempt.mkdir(exist_ok=False)
        self.reserved.append(attempt)
        publication.mkdir(exist_ok=False)
        self.reserved.append(publication)

    def run_bounded(self, argv, env, log):
        """No shell. Process-group ownership, bounded output, kill/reap on faults."""
        require(self.started is not None, 'attempt timer missing')
        remaining = 3600 - (time.monotonic() - self.started)
        require(remaining > 0, 'complete attempt deadline')
        timeout = min(120,remaining)
        start = time.monotonic()
        process = subprocess.Popen(argv,cwd=self.ROOT,env=env,stdin=subprocess.DEVNULL,
            stdout=subprocess.PIPE,stderr=subprocess.STDOUT,start_new_session=True)
        def terminate():
            try:
                os.killpg(process.pid,signal.SIGKILL)
            except ProcessLookupError:
                pass
        selector = selectors.DefaultSelector(); selector.register(process.stdout,selectors.EVENT_READ)
        output = bytearray(); failure = None
        try:
            while selector.get_map():
                if time.monotonic()-start > timeout:
                    failure = 'COMMAND_TIMEOUT'; break
                for key,_ in selector.select(timeout=min(.1,timeout)):
                    chunk = os.read(key.fileobj.fileno(),65536)
                    if not chunk:
                        selector.unregister(key.fileobj); continue
                    if len(output)+len(chunk) > MAX_LOG:
                        output.extend(chunk[:MAX_LOG-len(output)]); failure='LOG_OVERFLOW'; break
                    output.extend(chunk)
                if failure:
                    break
            if failure:
                terminate()
            try:
                code = process.wait(timeout=max(.01,timeout-(time.monotonic()-start)))
            except subprocess.TimeoutExpired:
                failure='COMMAND_TIMEOUT'; terminate(); code=process.wait()
        finally:
            selector.close(); process.stdout.close()
            if process.poll() is None:
                terminate(); process.wait()
        elapsed_ms=int((time.monotonic()-start)*1000)
        if elapsed_ms>int(timeout*1000):
            failure='COMMAND_TIMEOUT'
        log.write_bytes(output)
        record = dict(argv=argv,environment=env,exit_code=code,log=str(log),log_sha256=self.sha(log),
            log_bytes=len(output),elapsed_ms=elapsed_ms,
            failure=failure,owned_process_reaped=True)
        return record

    def command(self, argv, env, path, record):
        # Caller retains even nonzero/timeout records before raising.
        record.update(argv=argv,environment=env,exit_code=None,log=str(path),log_sha256=None,
                      log_bytes=0,elapsed_ms=0,failure='NOT_COMPLETED',owned_process_reaped=False)
        outcome = self.run_bounded(argv,env,path)
        record.update(outcome)
        require(outcome['exit_code'] == 0 and outcome['failure'] is None, 'command failure/timeout/log overflow')
        return outcome

    def bundle_inventory(self, root):
        return inventory(root,excluded=('verification/receipt.json',))

    def verify_bundle(self, root, manifest, expected):
        # Retains every historical payload/HTML/index-slice check.
        payload = self.validate_payload(root,manifest)
        notices = {str(p.relative_to(root)): self.sha(p) for p in self.files(root / 'notices')}
        originals = {'notices/'+str(p.relative_to(self.HERE / 'notices')):self.sha(p)
                     for p in self.files(self.HERE / 'notices')}
        require(len(originals) == 12 and notices == originals == expected['notices'], '12 exact notice identities')
        require(self.output_fingerprints(root) == expected['outputs'], 'runtime bytes changed')
        require(payload == expected['preload_validation'], 'payload validation differs')
        tree = self.bundle_inventory(root)
        require(set(tree['files']) == set(self.ARTIFACTS) | {'build-metadata.json'} | set(notices), 'exact 17 bundle files')
        allowed_dirs = {'notices'} | {str(Path(p).parent) for p in notices}
        if root.name == expected['candidate_id']:
            allowed_dirs.add('verification')
        require(set(tree['directories']) == allowed_dirs, 'exact bundle directory membership')
        return tree

    def execute_candidate(self, candidate_id, pins_path, pins_sha):
        attempt, publication = self.paths(candidate_id)
        require(not attempt.exists() and not publication.exists(), 'candidate already reserved')
        cfg, manifest, observed = self.observe()
        pins = self.authorization(candidate_id,pins_path,pins_sha,observed)
        commands = self.candidate_commands(cfg,observed['units'],attempt)
        env = self.environment(cfg,attempt)
        report = dict(schema_version=1,kind='CANDIDATE_NETWORK_BUILD_RESULT',candidate_id=candidate_id,
            recipe='network_v1',ticket=pins['ticket'],status='INCOMPLETE',fixture_only=self.fixture_only,
            pins=dict(path=str(pins_path),sha256=pins_sha),source_revision=pins['source_revision'],
            source_manifest=pins['source_manifest'],observation=observed,environment=env,
            object_reuse=False,claims=CLAIMS.copy(),compiles=[],link={},syntax={},wasm_validation={},error=None)
        self.reserved=[]
        self.started=time.monotonic()
        try:
            self.reserve(attempt,publication)
            for name in ('objects','deps','bundle','logs','tmp','node-cache'):
                (attempt / name).mkdir()
            shutil.copytree(self.HERE / '.cache',attempt / 'cache',symlinks=False)
            require(inventory(self.HERE / '.cache') == inventory(attempt / 'cache'), 'physical frozen cache copy differs')
            owned=(attempt,publication)
            def boundary():
                self.stable(observed,owned,observed['preservation'])
                require(self.authorization(candidate_id,pins_path,pins_sha,observed,completed=True) == pins,
                        'execution authority changed')
                require(time.monotonic()-self.started <= 3600, 'attempt deadline')
            for index,unit in enumerate(commands['compiles']):
                row=dict(source=unit['source'],object=unit['object'],pre_depfile=unit['pre_depfile'],
                    post_depfile=unit['post_depfile'],pre_scan={},compile={})
                report['compiles'].append(row)
                boundary()
                self.command(unit['pre_command'],env,attempt / 'logs' / f'{index:02}-pre.log',row['pre_scan'])
                row['pre_dependencies']=self.dependencies(Path(unit['pre_depfile']),attempt,observed)
                require(str(self.ROOT / unit['source']) in row['pre_dependencies'], 'source omitted from dependencies')
                boundary()
                require(not Path(unit['object']).exists(), 'stale/reused object')
                self.command(unit['command'],env,attempt / 'logs' / f'{index:02}-compile.log',row['compile'])
                row['post_dependencies']=self.dependencies(Path(unit['post_depfile']),attempt,observed)
                require(row['pre_dependencies'] == row['post_dependencies'], 'compiler dependency closure changed')
                require(Path(unit['object']).read_bytes()[:8] == self.MAGIC, 'invalid fresh Wasm object')
                row['object_sha256']=self.sha(Path(unit['object']))
            for row in report['compiles']:
                require(self.sha(Path(row['object'])) == row['object_sha256'], 'object changed before link')
                require(self.dependencies(Path(row['pre_depfile']),attempt,observed) == row['pre_dependencies'] and
                        self.dependencies(Path(row['post_depfile']),attempt,observed) == row['post_dependencies'],
                        'late dependency changed before link')
            for key in ('link','syntax','wasm_validation'):
                boundary()
                self.command(commands[key],env,attempt / 'logs' / (key+'.log'),report[key])
            report['preload_validation']=self.validate_payload(attempt / 'bundle',manifest)
            shutil.copytree(self.HERE / 'notices',attempt / 'bundle/notices')
            report['notices']={'notices/'+str(p.relative_to(self.HERE / 'notices')):self.sha(p)
                               for p in self.files(self.HERE / 'notices')}
            require(len(report['notices']) == 12, '12 notices required')
            report['outputs']=self.output_fingerprints(attempt / 'bundle')
            report['status']=STATUS
            report['bundle_id']=self.bundle_identity(report)
            metadata=attempt / 'bundle/build-metadata.json'
            write_new(metadata,report)
            report['metadata_sha256']=self.sha(metadata)
            boundary()
            self.verify_bundle(attempt / 'bundle',manifest,report)
            # Publication root was exclusively reserved; copy only validated17 files.
            for name in ('index.html','index.js','index.wasm','index.data','build-metadata.json'):
                shutil.copyfile(attempt / 'bundle' / name,publication / name)
            shutil.copytree(attempt / 'bundle/notices',publication / 'notices')
            (publication / 'verification').mkdir()
            self.verify_bundle(publication,manifest,report)
            require({p:self.sha(publication / p) for p in self.bundle_inventory(publication)['files']} ==
                    {p:self.sha(attempt / 'bundle' / p) for p in self.bundle_inventory(attempt / 'bundle')['files']},
                    'publication copy differs')
            boundary()
            write_new(attempt / 'result.json',report)
            self.owned_layout(attempt,commands)
            freeze=dict(schema_version=1,kind='CANDIDATE_TERMINAL_FREEZE',candidate_id=candidate_id,status=STATUS,
                attempt=inventory(attempt,excluded=('freeze.json',)),
                publication=inventory(publication,excluded=('verification/receipt.json',)),
                receipt_path='verification/receipt.json',elapsed_ms=int((time.monotonic()-self.started)*1000))
            require(freeze['elapsed_ms'] <= 3600000, 'attempt deadline before terminal freeze')
            write_new(attempt / 'freeze.json',freeze)
            return report
        except BaseException as error:
            report['status']='FAIL'; report['error']=str(error)
            if attempt in self.reserved:
                # Only the directory this invocation actually reserved is writable.
                fail=attempt / 'failure.json'
                if not fail.exists():
                    write_new(fail,report)
            raise

    def bundle_identity(self, report):
        return digest_bytes(canonical(dict(inputs=report['observation']['inputs'],outputs=report['outputs'],
            pins_sha256=report['pins']['sha256'],environment=report['environment'],
            commands=[r[k]['argv'] for r in report['compiles'] for k in ('pre_scan','compile')] +
                     [report[k]['argv'] for k in ('link','syntax','wasm_validation')])).encode())

    def owned_layout(self,attempt,commands):
        tree=inventory(attempt,excluded=('freeze.json',))
        require(set(tree['directories']) >= {'objects','deps','logs','bundle','cache','tmp','node-cache'}, 'owned role directory missing')
        require(all(p.split('/')[0] in {'objects','deps','logs','bundle','cache','tmp','node-cache'}
                    for p in tree['directories']), 'unknown owned directory')
        require({p for p in tree['files'] if '/' not in p} == {'result.json'}, 'unknown/failure owned root file')
        expected_objects={str(Path(c['object']).relative_to(attempt)) for c in commands['compiles']}
        expected_deps={str(Path(c[k]).relative_to(attempt)) for c in commands['compiles'] for k in ('pre_depfile','post_depfile')}
        expected_logs={f'logs/{i:02}-{suffix}.log' for i in range(61) for suffix in ('pre','compile')}
        expected_logs|={f'logs/{k}.log' for k in ('link','syntax','wasm_validation')}
        for base,expected in (('objects',expected_objects),('deps',expected_deps),('logs',expected_logs)):
            require({p for p in tree['files'] if p.startswith(base+'/')} == expected, 'unexpected '+base+' membership')
            require(not any(p.startswith(base+'/') for p in tree['directories']), 'unexpected nested '+base+' directory')

    def verify_candidate(self,candidate_id,pins_path,pins_sha,receipt=None):
        """Independent read-only verification: never execute or trust success assertions."""
        attempt,publication=self.paths(candidate_id)
        cfg,manifest,current=self.observe(owned=(attempt,publication))
        result=load_json(attempt / 'result.json')
        require(not (attempt / 'failure.json').exists(), 'failed attempt is terminal')
        expected_keys={'schema_version','kind','candidate_id','recipe','ticket','status','fixture_only','pins',
            'source_revision','source_manifest','observation','environment','object_reuse','claims','compiles',
            'link','syntax','wasm_validation','error','preload_validation','notices','outputs','bundle_id','metadata_sha256'}
        keys(result,expected_keys,'result')
        integer(result['schema_version'],1,1,'result schema')
        require(result['kind']=='CANDIDATE_NETWORK_BUILD_RESULT' and result['status']==STATUS and
                result['recipe']=='network_v1' and result['candidate_id']==candidate_id and result['error'] is None,
                'incomplete/failed/foreign result')
        require(type(result['fixture_only']) is bool and result['fixture_only']==self.fixture_only,
                'FIXTURE_ONLY evidence cannot verify as real')
        observed=result['observation']; keys(observed,OBSERVATION,'result observation')
        for key in OBSERVATION-{'preservation'}:
            require(exact(current[key],observed[key]), 'stale result '+key)
        self.protection_equal(observed['preservation'],current['preservation'],(attempt,publication))
        # Authorize against the pinned ORIGINAL protection inventory, not a union
        # that silently blesses unknown outputs. The phase union was checked above.
        pins=self.authorization(candidate_id,pins_path,pins_sha,observed,completed=True)
        require(result['pins']==dict(path=str(pins_path),sha256=pins_sha) and result['ticket']==pins['ticket'] and
                result['source_manifest']==pins['source_manifest'] and result['source_revision']==pins['source_revision'],
                'result authority/source identity')
        require(result['object_reuse'] is False and type(result['claims']) is dict and result['claims']==CLAIMS and
                all(type(v) is bool for v in result['claims'].values()), 'self acceptance/runtime claim/reuse')
        env=self.environment(cfg,attempt)
        require(result['environment']==env,'fixed environment differs')
        commands=self.candidate_commands(cfg,observed['units'],attempt)
        self.owned_layout(attempt,commands)
        require(type(result['compiles']) is list and len(result['compiles'])==61,'61 fresh compile records')
        def command(record,argv,log):
            keys(record,{'argv','environment','exit_code','log','log_sha256','log_bytes','elapsed_ms','failure','owned_process_reaped'},'command record')
            require(record['argv']==argv and record['environment']==env and type(record['exit_code']) is int and
                    record['exit_code']==0 and record['failure'] is None and record['owned_process_reaped'] is True,
                    'failed/timeout/changed command')
            integer(record['elapsed_ms'],0,120000,'command elapsed')
            require(record['log']==str(log),'foreign command log')
            actual=file_record(log)
            integer(record['log_bytes'],0,MAX_LOG,'log bytes')
            require(actual['sha256']==record['log_sha256'] and actual['bytes']==record['log_bytes'],'stale/corrupt log')
        for index,(row,unit) in enumerate(zip(result['compiles'],commands['compiles'])):
            keys(row,{'source','object','pre_depfile','post_depfile','pre_scan','compile','pre_dependencies','post_dependencies','object_sha256'},'unit record')
            for key in ('source','object','pre_depfile','post_depfile'):
                require(row[key]==unit[key],'foreign/stale unit '+key)
            command(row['pre_scan'],unit['pre_command'],attempt / 'logs' / f'{index:02}-pre.log')
            command(row['compile'],unit['command'],attempt / 'logs' / f'{index:02}-compile.log')
            before=self.dependencies(Path(unit['pre_depfile']),attempt,observed)
            after=self.dependencies(Path(unit['post_depfile']),attempt,observed)
            require(str(self.ROOT / unit['source']) in before and before==after==row['pre_dependencies']==row['post_dependencies'],
                    'actual compiler-discovered dependency mismatch')
            require(self.sha(Path(unit['object']))==row['object_sha256'] and Path(unit['object']).read_bytes()[:8]==self.MAGIC,
                    'missing/changed/reused object')
        for key in ('link','syntax','wasm_validation'):
            command(result[key],commands[key],attempt / 'logs' / (key+'.log'))
        require(result['bundle_id']==self.bundle_identity(result),'bundle identity mismatch')
        metadata=dict(result); metadata.pop('metadata_sha256')
        for root in (attempt / 'bundle',publication):
            self.verify_bundle(root,manifest,result)
            path=root / 'build-metadata.json'
            require(self.sha(path)==result['metadata_sha256'] and path.read_text()==canonical(metadata),'metadata differs')
        freeze=load_json(attempt / 'freeze.json')
        keys(freeze,{'schema_version','kind','candidate_id','status','attempt','publication','receipt_path','elapsed_ms'},'terminal freeze')
        integer(freeze['schema_version'],1,1,'freeze schema')
        integer(freeze['elapsed_ms'],0,3600000,'attempt elapsed')
        require(freeze['kind']=='CANDIDATE_TERMINAL_FREEZE' and freeze['candidate_id']==candidate_id and freeze['status']==STATUS and
                freeze['receipt_path']=='verification/receipt.json','terminal identity')
        require(exact(freeze['attempt'],inventory(attempt,excluded=('freeze.json',))) and
                exact(freeze['publication'],inventory(publication,excluded=('verification/receipt.json',))),
                'original+new exact terminal member/byte inventory')
        receipt_doc=dict(schema_version=1,kind='CANDIDATE_VERIFICATION_RECEIPT',candidate_id=candidate_id,
            status='FIXTURE_ONLY' if self.fixture_only else 'VERIFIED_LINKED_NOT_BROWSER_VERIFIED',fixture_only=self.fixture_only,
            bundle_id=result['bundle_id'],pins_sha256=pins_sha,result_sha256=self.sha(attempt / 'result.json'),
            freeze_sha256=self.sha(attempt / 'freeze.json'),claims=CLAIMS.copy(),
            verifier_inputs={str(self.HERE / name):current['inputs'][str(self.HERE / name)]
                             for name in ('candidate_recipe.py','verify_candidate.py','profile_client.py')})
        receipt_path=publication / 'verification/receipt.json'
        if receipt_path.exists():
            require(receipt_path.read_text()==canonical(receipt_doc),'foreign/stale verification receipt')
        if receipt is not None:
            require(absolute(receipt)==receipt_path,'only fixed candidate verification/receipt.json allowed')
            write_new(receipt_path,receipt_doc)
        return dict(status=receipt_doc['status'],candidate_id=candidate_id,bundle_id=result['bundle_id'],
                    runtime=False,authority=False,P0=False,fixture_only=self.fixture_only)


def build_parser():
    parser=argparse.ArgumentParser(description=__doc__)
    mode=parser.add_mutually_exclusive_group(required=True)
    mode.add_argument('--plan-only',action='store_true')
    mode.add_argument('--execute',action='store_true')
    parser.add_argument('--candidate-id',required=True)
    parser.add_argument('--pins')
    parser.add_argument('--pins-sha256')
    return parser


def build_main(argv=None):
    args=build_parser().parse_args(argv)
    recipe=CandidateRecipe()
    recipe.paths(args.candidate_id)
    if args.execute:
        require(args.pins is not None and args.pins_sha256 is not None,'execution pins AND digest required')
        result=recipe.execute_candidate(args.candidate_id,args.pins,args.pins_sha256)
        print(canonical(dict(status=result['status'],candidate_id=args.candidate_id)))
    else:
        require(args.pins is None and args.pins_sha256 is None,'plan cannot claim execution pins')
        report=recipe.plan(args.candidate_id)
        target=absolute(recipe.HERE / 'tests/candidate' / ('preparation-'+args.candidate_id))
        require(not target.exists(),'preparation output exists')
        target.mkdir(parents=True,exist_ok=False)
        write_new(target / 'plan.json',report)
        print(canonical(dict(status='NOT_EXECUTED',plan=str(target / 'plan.json'))))
    return 0


def verify_main(argv=None):
    parser=argparse.ArgumentParser(description='Read-only independent fixed candidate verification')
    parser.add_argument('--candidate-id',required=True)
    parser.add_argument('--pins',required=True)
    parser.add_argument('--pins-sha256',required=True)
    parser.add_argument('--receipt')
    args=parser.parse_args(argv)
    print(canonical(CandidateRecipe().verify_candidate(args.candidate_id,args.pins,args.pins_sha256,args.receipt)))
    return 0
