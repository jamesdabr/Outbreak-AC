# T178 corrected final3 publisher and finite plan

Worker MAIN delegate /root/review_native_candidate. T1781.3 / DEFAULT_DEV_BUILD_PREPARATION0.3 / D274, closure0.3. FINAL INVENTORY ONLY. All sources/test jobs/history immutable; prior refused operation and handoff retained. This is the complete corrected standard-library DATA publisher, inspected before its sole invocation. No project module imports, tool/probe/process/FFI/SDK-copy/build/runtime calls. No acceptance authority.

Finite plan: one original300s cutoff,8MiB output maximum (one compact summary),128MiB NEW records. Exactly two original owned roots, three reserved publication slots, seven frozen sources, two existing PASS results, six baseline archive files, complete prior T168 owned graph, and every declared external record. External roles have exactly three observed schemas:376 SHA256 ordinary records,6 SHA256+SHA512 archive records,5 exact0755 alias records. Schema dispatch preserves every declared field and rejects unknown shapes; complete record equality, never subset comparison. Current MAIN authority paths are explicitly refreshed as new current context; old authority/control blobs remain historical, never retargeted. All six archive SHA512 values computed alongside SHA256 and exact metadata. All read-only identities rechecked after publication. No retry/repair after any refusal.

Writes: only NEW web/build/dev_regression/tests/preparation-1/final-3/{inventory.json,receipt.json,freeze.json}. Reserve all three exclusively before owned-directory capture. Fill only those reserved inode identities. Completed inventory bound by receipt; terminal graph includes filled inventory/receipt and every file/directory in module+focused-home except sole direct freeze content-derived hash/length/timestamps; freeze physical kind/device/inode/mode/nlink retained. No unowned-parent metadata. Both passes are retained observations, not rerun or current-contract execution. Original source hashes and historic result pins remain exact while current ticket/contract authority is recorded independently. Pending MAIN review only; holds unchanged.

Execute this exact fenced publisher once after source inspection. Any failure preserves and stops. This note is not itself an operation result.

```python
from pathlib import Path
import os,stat,time,json,hashlib,re
ROOT=Path('/Users/jd1/code/apps/outbreak')
START=time.monotonic();END=START+300;MAX_NEW=134217728;written=0
FILE_KEYS={'kind','device','inode','mode','nlink','bytes','mtime_ns','ctime_ns','sha256'}
ARCHIVE_KEYS=FILE_KEYS|{'sha512'}
LINK_KEYS={'kind','device','inode','mode','nlink','mtime_ns','ctime_ns','raw_text','declared_target'}
NUMBERS={'device','inode','mode','nlink','bytes','mtime_ns','ctime_ns'}
roots=['web/build/dev_regression','tests/outbreak/builder_reap/T178']
final=roots[0]+'/tests/preparation-1/final-3'
slots=[final+'/'+n for n in ('inventory.json','receipt.json','freeze.json')]
excluded=slots[2]
def check():
    if time.monotonic()>=END:raise TimeoutError('original final3 data-operation300s')
def need(v,s):
    if not v:raise ValueError(s)
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,sort_keys=True,indent=2)+'\n').encode()
def path(n):return Path(n) if n.startswith('/') else ROOT/n
def physical(s):return dict(device=s.st_dev,inode=s.st_ino,mode=stat.S_IMODE(s.st_mode),nlink=s.st_nlink)
def meta(s,kind):return dict(kind=kind,**physical(s),bytes=s.st_size,mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns)
def shape(row):
    need(type(row) is dict,'typed external record')
    keys=set(row);need(keys in (FILE_KEYS,ARCHIVE_KEYS,LINK_KEYS),'exact declared external record schema')
    for k in keys&NUMBERS:need(type(row[k]) is int and row[k]>=0,'nonbool external integer '+k)
    if keys==LINK_KEYS:
        need(row['kind']=='link' and type(row['raw_text']) is str and type(row['declared_target']) is str and row['mode']==493 and row['nlink']==1,'declared0755 alias fields')
    else:
        need(row['kind']=='file' and row['nlink']>=1,'ordinary external file fields')
        for k,count in (('sha256',64),('sha512',128)):
            if k in keys:need(type(row[k]) is str and re.fullmatch('[0-9a-f]{'+str(count)+'}',row[k]),'declared digest '+k)
    return keys

def record(n,owned=False,archive=False):
    check();p=path(n);s=p.lstat();need(stat.S_ISREG(s.st_mode) and (not owned or s.st_nlink==1),'ordinary file '+n)
    before=meta(s,'file');h=hashlib.sha256();h512=hashlib.sha512() if archive else None
    with p.open('rb',buffering=0) as f:
        while True:
            check();b=f.read(1048576)
            if not b:break
            h.update(b)
            if archive:h512.update(b)
    need(meta(p.lstat(),'file')==before,'stable file '+n)
    out=dict(before,sha256=h.hexdigest())
    if archive:out['sha512']=h512.hexdigest()
    need(set(out)==(ARCHIVE_KEYS if archive else FILE_KEYS),'complete generated file record')
    return out

def alias(n,prior):
    need(shape(prior)==LINK_KEYS,'exact alias schema');check();p=path(n);s=p.lstat()
    need(stat.S_ISLNK(s.st_mode) and stat.S_IMODE(s.st_mode)==493 and s.st_nlink==1,'exact0755 declared alias '+n)
    text=os.readlink(p);target=str(p.resolve(strict=True))
    need(text==prior['raw_text'] and target==prior['declared_target'],'exact alias text/target '+n)
    out=dict(kind='link',**physical(s),mtime_ns=s.st_mtime_ns,ctime_ns=s.st_ctime_ns,raw_text=text,declared_target=target)
    need(meta(p.lstat(),'link')==meta(s,'link'),'stable alias '+n);need(set(out)==LINK_KEYS,'complete generated alias record');return out

def observed(n,prior):
    schema=shape(prior)
    out=alias(n,prior) if schema==LINK_KEYS else record(n,archive=schema==ARCHIVE_KEYS)
    need(set(out)==schema,'same full declared role schema '+n);return out

def graph(skip=None):
    g=dict(directories={},files={},links={})
    for root in roots:
        for parent,dirs,files in os.walk(path(root),followlinks=False):
            check();p=Path(parent);n=str(p.relative_to(ROOT));s=p.lstat();need(stat.S_ISDIR(s.st_mode),'owned ordinary directory '+n)
            g['directories'][n]=meta(s,'directory')
            for item in dirs:need(not (p/item).is_symlink(),'no owned directory alias')
            for item in files:
                n=str((p/item).relative_to(ROOT));need(not (p/item).is_symlink(),'no owned file alias')
                if n!=skip:g['files'][n]=record(n,True)
    return g

def syncdir():
    check();fd=os.open(path(final),os.O_RDONLY|os.O_DIRECTORY)
    check();os.fsync(fd);check();os.close(fd)

def fill(n,data):
    global written
    check();need(len(data)+written<=MAX_NEW,'new records128MiB cap')
    need(n in slots and record(n,True)==reservations[n],'exclusive unchanged reserved slot')
    check();fd=os.open(path(n),os.O_WRONLY|os.O_NOFOLLOW)
    need(physical(os.fstat(fd))=={k:reservations[n][k] for k in ('device','inode','mode','nlink')},'reserved descriptor identity')
    offset=0
    while offset<len(data):
        check();count=os.write(fd,data[offset:offset+1048576]);need(type(count) is int and count>0,'data write progress');offset+=count
    check();os.fsync(fd);check();os.close(fd);written+=len(data);syncdir()
    result=record(n,True);need(result['bytes']==len(data) and result['sha256']==sha(data),'durable filled record readback');return result

# Every declared input/path is read and fully validated before publication.
absent=[roots[0]+'/attempts',roots[0]+'/candidates','web/repro/blackwood-source-manifest.json',roots[0]+'/tests/preparation-1/final-2']
need(not os.path.lexists(path(final)),'fresh final3 including alias absence')
for n in absent:need(not os.path.lexists(path(n)),'retained absent root '+n)
focus_n=roots[1]+'/preparation-1/focused-1/result.json';full_n=roots[0]+'/tests/preparation-1/pass-11/result.json'
focus_b=path(focus_n).read_bytes();full_b=path(full_n).read_bytes()
need(sha(focus_b)=='94a620c6d5884b4a564dcdbf8be51f81a70f52831493ac89ad2ed774ef44e7f6','retained exact focused result')
need(sha(full_b)=='591d9c40e0f7b069aeb7a020ed883415aaf8edd5a0b3db80891181b2a9dc4e3a','retained exact full result')
focus=json.loads(focus_b);full=json.loads(full_b)
need(focus['status']=='PASS_FIXTURE_ONLY' and focus['cases']==16 and full['status']=='PASS_FIXTURE_ONLY' and full['groups']==228 and full['leaf_scenarios']==247,'both exact observed PASS')
source={n:record(n,True) for n in focus['source_hashes']}
need(len(source)==7 and {n:r['sha256'] for n,r in source.items()}==focus['source_hashes'],'frozen seven sources')
need(all(full['source_hashes'][Path(n).name]==r['sha256'] for n,r in source.items() if n.startswith(roots[0]+'/')),'full frozen six sources')
for n,r in source.items():
    need(record(roots[1]+'/preparation-1/focused-1/sources/'+n,True)['sha256']==r['sha256'],'focused frozen source snapshot '+n)
    if n.startswith(roots[0]+'/'):need(record(roots[0]+'/tests/preparation-1/pass-11/sources/'+Path(n).name,True)['sha256']==r['sha256'],'full frozen source snapshot '+n)
old_n=roots[0]+'/tests/preparation-1/final-1/freeze.json';old_b=path(old_n).read_bytes()
need(sha(old_b)=='c443756bf4d1d231312d5743c59934e87348d8e2d03067bd92f6779115d2a291','immutable accepted T168 freeze');old=json.loads(old_b)
changed={roots[0]+'/'+n for n in ('recipe.py','test_recipe.py','SCHEMA.md','README.md')}
for n,r in old['owned_graph']['files'].items():
    if n not in changed:need(record(n,True)==r,'historical owned file unchanged '+n)
external={};schema_counts={'sha256':0,'sha256_sha512':0,'alias':0}
for group,items in old['external_roles'].items():
    newgroup={'current_final_inventory_authority':'historical_T168_authority_paths_current_context','current_review_and_MAIN_receipt':'accepted_T168_review_and_MAIN_receipt'}.get(group,group);external[newgroup]={}
    for n,prior in items.items():
        schema=shape(prior);schema_counts['alias' if schema==LINK_KEYS else 'sha256_sha512' if schema==ARCHIVE_KEYS else 'sha256']+=1
        row=observed(n,prior)
        if not n.startswith(('MVP/','tickets/')):need(row==prior,'complete immutable typed external identity '+n)
        external[newgroup][n]=row
need(schema_counts==dict(sha256=376,sha256_sha512=6,alias=5),'finite exact declared external schemas')
auth=['tickets/T178.md','MVP/DEFAULT_DEV_BUILD_PREPARATION.md','MVP/BUILDER_TERMINAL_GROUP_CLOSURE.md','notes/decisions/D274-default-dev-role-specific-final-inventory.md','notes/decisions/D263-builder-terminal-group-corrections.md','notes/decisions/D269-strict-original-reap-builder-correction.md','notes/decisions/D271-builder-original-cutoff-clarification.md','notes/decisions/D272-default-dev-strict-reap-release.md','AGENTS.md','MVP/GOVERNANCE.md','notes/decisions/D235-Darwin-nonreaping-wait-adapter.md','notes/decisions/D236-Blackwood-verifier-receipt-correction.md','notes/decisions/D238-builder-command-persistence-cutoffs.md']
external['current_T178_inventory_only_authority']={n:record(n) for n in auth}
need('Revision:1.3' in path(auth[0]).read_text() and 'RELEASED FINAL INVENTORY ONLY D274' in path(auth[0]).read_text() and 'Revision:0.3' in path(auth[1]).read_text(),'current inventory-only revisions')
baseline='notes/reviews/MAIN-T178-source-baseline-1'
need(record(baseline+'/manifest.json')['sha256']=='da4be7392462c33bfd8bc4bc6e1b59c1616f602792dd96de52671b46a7210e99','MAIN strict-reap baseline manifest')
external['MAIN_T178_immutable_source_baseline']={str(p.relative_to(ROOT)):record(str(p.relative_to(ROOT))) for p in sorted(path(baseline).iterdir())}
base=json.loads(path(baseline+'/manifest.json').read_bytes())
for n,r in base['source'].items():
    need(external['MAIN_T178_immutable_source_baseline'][baseline+'/'+Path(n).name]['sha256']==r['sha256'],'MAIN source archive binding')
    need(record(roots[1]+'/preparation-1/pre-edit/'+Path(n).name,True)['sha256']==r['sha256'],'immutable pre-edit source binding')
refs=['notes/decisions/D250-default-dev-preparation-acceptance.md','notes/reviews/MAIN-T168-final-freeze-review-1.json','notes/reviews/MAIN-T168-final-preparation-integrity-1.json','notes/handoffs/T168-final-freeze-1.md','notes/handoffs/T175-final-submission-1.md','notes/questions/T175-original-reap-ECHILD-1.md','notes/handoffs/T178-source-freeze-preinspection-1.md','notes/handoffs/T178-final3-data-operation-plan-1.md','notes/handoffs/T178-final-submission-1.md','notes/handoffs/T178-corrected-final3-operation-1.md']
external['accepted_T168_preserved_T175_and_T178_refusal_current_publisher_context']={n:record(n) for n in refs}
need(external['accepted_T168_preserved_T175_and_T178_refusal_current_publisher_context']['notes/handoffs/T178-final-submission-1.md']['sha256']=='bb51e4803c112edd8714889bad063f07a9916f9107dc31138cfe5683337cd8c1','immutable prior refusal handoff')
external_sha=sha(enc(external));before=graph()
role_context=dict(current_lease='T1781.3 D274: FINAL INVENTORY ONLY, pending MAIN review',historical_authority='All old authority/index/control blobs remain historical bytes; current authority paths explicitly refreshed as new records, not retargeted old controls.',dependency_context='Installed-tool roles do not permit hardlinks for source/dependency/owned records; exact0755 declared aliases only.',archive_schema='All6 archives compute both declared SHA256+SHA512 and exact ordinary metadata; no field dropping/subset comparison.',system_dyld_role='D235 lazy libSystem.B.dylib declaration only; no fabricated ordinary file or native call.',native_support='UNPROVEN by guarded fakes',actual_build_or_runtime=False,project_import_or_tool_execution=False,ctypes_import_or_library_load=False,whole_SDK_or_cache_execution_closure_claim=False)
# Mutation begins only after complete source/evidence/role/protection checks.
check();path(final).mkdir(mode=493);reservations={}
for n in slots:
    check();fd=os.open(path(n),os.O_CREAT|os.O_EXCL|os.O_WRONLY|os.O_NOFOLLOW,420)
    check();os.fchmod(fd,420);check();os.fsync(fd);check();os.close(fd);reservations[n]=record(n,True)
syncdir();prefill=graph()
need(set(prefill['files'])==set(before['files'])|set(slots) and set(prefill['directories'])==set(before['directories'])|{final},'only three files and owned final3 directory added')
need(all(prefill['files'][n]==v for n,v in before['files'].items()),'all protected files unchanged across reservation')
inventory=dict(schema_version=1,kind='DEFAULT_DEV_STRICT_REAP_PREPARATION_CANDIDATE_INVENTORY',ticket='T1781.3',status='PENDING_MAIN_REVIEW',owned_roots=roots,current_sources=source,external_roles=external,external_roles_sha256=external_sha,prior_owned_graph=prefill,reserved_final_slots=reservations,absent_roots={n:True for n in absent},historical_controls_not_retargeted=True,role_context=role_context,scope='Historical pre-fill empty slot identities; final freeze binds filled inventory/receipt and complete two-root graph. Sole terminal self-content exclusion.')
inv=fill(slots[0],enc(inventory))
receipt=dict(schema_version=1,kind='DEFAULT_DEV_STRICT_REAP_PREPARATION_CANDIDATE_RECEIPT',ticket='T1781.3',status='PENDING_MAIN_REVIEW',inventory=dict(path=slots[0],**inv),current_sources=source,external_roles_sha256=external_sha,guarded_jobs={focus_n:dict(record=record(focus_n,True),cases=16,elapsed_s=focus['elapsed_s'],new_test_run=False),full_n:dict(record=record(full_n,True),groups=228,leaf_scenarios=247,elapsed_s=full['elapsed_s'],new_test_run=False)},acceptance_claim=False,actual_build=False,actual_runtime=False,real_project_execution=False)
rec=fill(slots[1],enc(receipt));g=graph(excluded);self_res=dict(kind='file',**physical(path(excluded).lstat()))
freeze=dict(schema_version=1,kind='DEFAULT_DEV_STRICT_REAP_PREPARATION_CANDIDATE_FREEZE',ticket='T1781.3',status='FROZEN_PENDING_MAIN_REVIEW',acceptance_pending_MAIN=True,owned_roots=roots,owned_graph=g,owned_graph_sha256=sha(enc(g)),ordinary_member_files=len(g['files']),ordinary_files_including_self=len(g['files'])+1,owned_directories=len(g['directories']),links=len(g['links']),completed_inventory=inv,completed_receipt=rec,current_sources=source,external_roles=external,external_roles_sha256=external_sha,role_context=role_context,only_self_exclusion=excluded,self_reservation=self_res,self_exclusion_semantics='Only direct final3/freeze.json content-derived hash/length/timestamps excluded; physical kind/device/inode/mode/nlink pinned. No other file/directory/link exclusion.',parent_directory_metadata_outside_owned_roots=False,absent_roots={n:True for n in absent},actual_build=False,actual_runtime=False)
fr=fill(slots[2],enc(freeze))
need(graph(excluded)==g,'final complete two-root graph unchanged')
need(dict(kind='file',**physical(path(excluded).lstat()))==self_res,'direct freeze physical identity')
for group,items in external.items():
    for n,row in items.items():need(observed(n,row)==row,'final complete typed external role unchanged '+n)
for n in absent:need(not os.path.lexists(path(n)),'final absent root '+n)
need({n:record(n,True) for n in source}==source,'final frozen seven source identities')
need(record(slots[0],True)==inv and record(slots[1],True)==rec and record(slots[2],True)==fr,'durable final three readbacks')
check()
summary=dict(status='PENDING_MAIN_REVIEW',inventory_sha256=inv['sha256'],receipt_sha256=rec['sha256'],freeze_sha256=fr['sha256'],owned_files=len(g['files'])+1,owned_directories=len(g['directories']),links=len(g['links']),external_role_records=sum(len(v) for v in external.values()),declared_role_schema_counts=schema_counts,owned_graph_sha256=freeze['owned_graph_sha256'],new_bytes=written,elapsed_s=time.monotonic()-START)
out=json.dumps(summary,sort_keys=True);need(len(out.encode())<8388608,'output8MiB cap');print(out)
```
