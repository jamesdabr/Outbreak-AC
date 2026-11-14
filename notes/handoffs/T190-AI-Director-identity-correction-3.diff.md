# T1901.2 — exact identity correction diff

D325 / CAMERA_FOUNDATION0.6. Complete textual diff against the captured T1901.1
three-file source snapshot, with three context lines. Only source strings were
compared; no Python/C++/Node helper, oracle, generator, test or target executed.
D321 routine/row mapping,64 control labels/suite and94-command plan are textually
unchanged. Hashes and scoped validation are recorded in the NEW correction handoff.

```diff
--- a/tests/outbreak/camera/release-1/verify.py
+++ b/tests/outbreak/camera/release-1/verify.py
@@ -1050,6 +1050,22 @@
  (16384,(32653,16677,1222),(1067,1280,-5744),(32768,16384,1024),2977),
  (32768,(32475,8077,1222),(-1280,1067,-5744),(32768,8192,1024),1633),
  (49152,(41075,7899,1222),(-1067,-1280,-5744),(40960,8192,1024),1654))
+# D325's eight existing exclusion seeds, not new target requests.
+# fixture,eye,yaw,pitch,semantic role. All feet derive from the endpoint eye.
+IDENTITY_SEEDS=(
+ (4,(512,512,8192),0,0,'world0-strict-refusal'),
+ (1,(1127,32768,8192),49152,0,'xy-outside-first'),
+ (1,(64409,32768,8192),16384,0,'xy-outside-first'),
+ (1,(32768,1127,8192),0,0,'xy-outside-first'),
+ (1,(32768,64409,8192),32768,0,'xy-outside-first'),
+ (5,(32768,32768,-126464),0,8000,'lower-z-equal-candidate'),
+ (5,(32768,32768,129000),0,-8000,'upper-z-shadow-candidate'),
+ (7,(512,512,8192),0,0,'world0-strict-refusal'))
+IDENTITY_FACE_YAWS=((0,8192,16384,24576),(32768,40960,49152,57344),
+ (16384,24576,32768,40960),(0,8192,49152,57344),
+ (0,16384,32768,49152),(0,16384,32768,49152))
+IDENTITY_XY_RIGS=((1280,-6144,307),(5250,-3439,307),(6144,1280,307),(3439,5250,307),
+ (-1280,6144,307),(-5250,3439,307),(-6144,-1280,307),(-3439,-5250,307))
 FAMILY_RANGES=((0,512,'free'),(512,1280,'blocker'),(1280,1536,'initial'),
  (1536,1792,'recovery'),(1792,2304,'stance'),(2304,2560,'exclusion'),
  (2560,2816,'rounding'),(2816,3072,'none'),(3072,3584,'refusal'),(3584,4096,'metamorphic'))
@@ -1080,6 +1096,26 @@
     row['fixture']=1;row['foot']=(32768,32768,z-row['eye'])
     return row
 
+def identity_exclusion_row(row,index):
+    seed=index//8;h=(index//4)%2;w=(index//2)%2;p=index%2
+    fixture,eye,yaw,pitch,role=IDENTITY_SEEDS[seed]
+    height,eye_height=((3738,3174),(5325,4608))[h]
+    row.update(fixture=fixture,poison=p,weapon=1+w,aim=(yaw,pitch),height=height,
+               eye=eye_height,foot=(eye[0],eye[1],eye[2]-eye_height))
+    predicate={'d325_identity':True,'body_feasible':seed not in (0,7)}
+    predicate.update({'refusal':True,'unchanged_output':True} if role=='world0-strict-refusal' else {'hit':True})
+    return row,predicate
+
+def identity_face_row(row,rank,decoration):
+    aim_index,h=divmod(decoration,2)
+    # Preserve original weapon/poison/default fields; only adopted pose/context.
+    seed=(2,1,4,3,6,5)[rank];fixture,eye,_,pitch,_=IDENTITY_SEEDS[seed]
+    height,eye_height=((3738,3174),(5325,4608))[h]
+    row.update(fixture=fixture,aim=(IDENTITY_FACE_YAWS[rank][aim_index],pitch),height=height,
+               eye=eye_height,foot=(eye[0],eye[1],eye[2]-eye_height))
+    return row,{'d325_identity':True,'hit':True,'body_feasible':True,
+                'feature_axes':[rank//2],'feature_signs':[-1 if rank%2==0 else 1]}
+
 def feature_seed(row,index,oracle,angles):
     if index<384:
         rank=index//64;variant=(index%64)//8;decoration=index%8
@@ -1090,6 +1126,7 @@
     else:
         rank=(index-576)//24;variant=((index-576)%24)//4;decoration=index%4
         axes=[0,1,2];signs=[-1 if not rank&4 else 1,-1 if not rank&2 else 1,-1 if not rank&1 else 1]
+    if len(axes)==1 and variant==5:return identity_face_row(row,rank,decoration)
     row['height'],row['eye']=(3738,3174) if decoration%2==0 else (5325,4608)
     normal=[0,0,0]
     for a,s in zip(axes,signs):normal[a]=s
@@ -1129,8 +1166,6 @@
     if variant==2:raise oracle.ConstructionRequired(row['id'],'near Q32 boundary','precise predicate and literal curved/bin variant certificate pending')
     if len(axes)==1 and variant==4 or len(axes)==3 and variant==4:
         raise oracle.ConstructionRequired(row['id'],'competing first/priority','literal fixed-primitive competing-root certificate pending')
-    if len(axes)==1 and variant==5:
-        raise oracle.ConstructionRequired(row['id'],'primitive0/outside identity','exposed real first-contact identity variant not yet frozen')
     if len(axes)==1 and variant==1:
         raise oracle.ConstructionRequired(row['id'],'shallow face entry','literal nonnormal-entry certificate for the advertised variant pending')
     if len(axes)==1 and variant==7 or len(axes)==3 and variant==5:predicate['normal_margin_lt31']=True
@@ -1227,6 +1262,156 @@
             offset=next(j for j in range(160) if actual[j]!=wanted[j])
             raise ValueError(f'full-field mismatch row-index={index} offset={offset} actual={actual[offset]} expected={wanted[offset]}')
 
+def identity_fixture_certificate(items):
+    """D325 fixed-map source proof during the ONE existing cell decode.
+
+    No sweep, feature/root enumeration or second full oracle query. Domain
+    summaries and the complete F7 all-solid assertion share the same192512
+    cell records that the oracle already needs; only named local cells are
+    additionally read for the structural shade/absence proof.
+    """
+    fixtures_=[];summaries=[];total=0
+    for fid,item in enumerate(items):
+        side=item['side'];cells=[];all_solid=True;lowest_floor=None;highest_ceiling=None
+        for index,cell in enumerate(struct.iter_unpack('<BbbB',item['cells'])):
+            if index%1024==0:tick()
+            kind,floor,ceiling,tag=cell
+            need(kind in (0,4) and not tag and ((kind==0 and floor==ceiling==0) or (kind==4 and floor<ceiling)),'fixed legal cell domain')
+            cells.append(cell);total+=1
+            if kind==4:
+                all_solid=False
+                lowest_floor=floor if lowest_floor is None else min(lowest_floor,floor)
+                highest_ceiling=ceiling if highest_ceiling is None else max(highest_ceiling,ceiling)
+        need(len(cells)==side*side,'fixed complete oracle cell decode')
+        fixtures_.append(dict(item,cells=cells))
+        summaries.append({'fixture':fid,'side':side,'all_solid':all_solid,
+          'lowest_floor':lowest_floor,'highest_ceiling':highest_ceiling,'cell0':list(cells[0])})
+    need(len(fixtures_)==8 and total==192512,'original eight-fixture cell count')
+    absent=(1,2,3,5);shaded=(0,4,6)
+    for fid in absent:need(fixtures_[fid]['cells'][0][0]==4,'primitive0 absent in space cell0')
+    for fid in shaded:
+        cells=fixtures_[fid]['cells'];side=fixtures_[fid]['side']
+        need(all(cells[i]==(0,0,0,0) for i in (0,1,side)),'cell0/east/north solid shade')
+    need(fixtures_[0]['cells'][129]==(0,0,0,0),'accepted F0 northeast local solid DATA')
+    need(summaries[7]['all_solid'] and summaries[7]['side']==256,'complete all-solid F7 source geometry')
+    # Signed i8 floor/ceiling domains plus closed cells/outside XY cover the
+    # full horizontal plane. Lower floors precede/tie -Z; upper ceiling union
+    # precedes +Z by>=1024. Every cell ID and four XY IDs are below -Z's ID.
+    need(all(s['lowest_floor'] is None or s['lowest_floor']>=-128 for s in summaries),'full-input lower floor bound')
+    need(all(s['highest_ceiling'] is None or s['highest_ceiling']<=127 for s in summaries),'full-input upper ceiling bound')
+    need(3*65536-1<196612 and 196611<196612,'cell/XY stable identities below lower outside')
+    need((1024-11)*Q>7732,'upper outside shadow exceeds11 plus time flooring quantum')
+    need(2*255*255>360*360 and (360-255-11)*Q>7732,'neighbor shade exceeds11 plus flooring quantum')
+    camera=(R/'source/outbreak/p1_camera.cpp').read_bytes()
+    need(sha(camera)==SOURCE_PIN,'D302 camera source for World0 structural guard')
+    text=camera.decode('utf-8');start=text.index('bool hit_witness(');end=text.index('\nbool rounded_travel(',start)
+    guard=text[start:end]
+    need('hit.primitive_id<cell_primitive_limit' in guard and
+         'hit.status==QueryStatus::Hit && hit.kind==HitKind::World' in guard and
+         '(hit.primitive_id>=196608 && hit.primitive_id<=196613)' in guard and
+         'cell_primitive_limit=UINT64_C(3)*info.map.side*info.map.side;' in text,
+         'source structural acceptance of valid World0 and six outside IDs')
+    proof={'schema':'D325_FIXED_INPUT_IDENTITY_1','proof_kind':'INDEPENDENT_GEOMETRY_AND_PINNED_SOURCE',
+      'decoded_cells':total,'fixtures':summaries,
+      'world0':{'absent_fixtures':list(absent),'east_north_shaded_fixtures':list(shaded),
+        'F7_all_solid':True,'shadow_path_lower_bound_exclusive':105,
+        'first_and_priority_unavailable':True,'structural_guard_permits':True,'camera_source_sha256':SOURCE_PIN},
+      'outer_z':{'lower_floor_min':-131072,'upper_ceiling_max':130048,'upper_shadow_z_gap':1024,
+        'lower_equal_loses_stable_id':True,'first_and_priority_unavailable':True},
+      'clear_id0_is_world0_hit':False,'general_G2_World0_and_six_outside_obligations':'RETAINED_NOT_PROVED_BY_CAMERA_ROWS'}
+    return fixtures_,proof
+
+def identity_certificate(row,response,cert,oracle,angles,bindings,source_proof):
+    """D325: real firsts versus hidden candidates/refusal/source certificates.
+
+    Plane candidate arithmetic supplements the EXISTING complete oracle result;
+    it does not call sweep/outside/box_candidates/roots or synthesize a Hit.
+    """
+    def require(condition,detail):
+        if not condition:raise oracle.ConstructionRequired(row['id'],'D325 identity role',detail)
+    require(source_proof.get('schema')=='D325_FIXED_INPUT_IDENTITY_1','complete fixed-input/source proof required')
+    face=512<=row['id']<896 and (row['id']-512)%64 in range(40,48)
+    if face:
+        rank=(row['id']-512)//64;local=(row['id']-512)%64-40;aim_index,h=divmod(local,2)
+        seed=(2,1,4,3,6,5)[rank];fixture,eye,_,pitch,role=IDENTITY_SEEDS[seed]
+        yaw=IDENTITY_FACE_YAWS[rank][aim_index];weapon=1;poison=row['id']%2
+    else:
+        require(2432<=row['id']<2496,'exact64 exclusion or48 face variant5 rows')
+        index=row['id']-2432;seed=index//8;h=(index//4)%2;w=(index//2)%2
+        fixture,eye,yaw,pitch,role=IDENTITY_SEEDS[seed];weapon=1+w;poison=index%2
+    height,eye_height=((3738,3174),(5325,4608))[h]
+    foot=(eye[0],eye[1],eye[2]-eye_height)
+    require(row['fixture']==fixture and row['aim']==(yaw,pitch) and row['height']==height and row['eye']==eye_height and row['foot']==foot,'adopted exact aim/height/Eye/foot mapping')
+    require(row['weapon']==weapon and row['poison']==poison and row['flags']==0 and row['revision']==1 and row['count']==row['boxes']==0,'original weapon/poison and live default context')
+    require(row['slot']==65535 and row['rule_value']==0 and row['table_kind']==row['table_index']==row['table_value']==0,'canonical unpatched rules/table')
+    require(3738<=height<=5325 and 3174<=eye_height<=4608 and height-eye_height>=564 and all(0<=foot[i]<=262144 for i in (0,1)) and -131072<=foot[2] and foot[2]+height<=131072,'numeric scalar validity, no authority inference')
+    if pitch==0:delta=IDENTITY_XY_RIGS[YAWS.index(yaw)]
+    else:
+        dx,dy=QK1_LITERALS[yaw//16384][2][:2];delta=(dx,dy,-5744 if pitch==8000 else 6358)
+    require(tuple(cert.get('eye',()))==eye and tuple(cert.get('delta',()))==delta and rig(row,oracle,angles)==delta,'independent accepted-basis full-sum rig')
+    require(cert.get('physical_query') is True and cert.get('body_feasible') is (role!='world0-strict-refusal'),'actual query and independent body label')
+    if role=='world0-strict-refusal':
+        fault=oracle.bound_fault(bindings,'initial_overlap')
+        require(cert.get('initial_distance_squared')==0 and tuple(cert.get('fault',()))==fault,'real cell0 strict-overlap cause and accepted G2 false tuple')
+        require(response==oracle.response(False,fault,oracle.poison(poison),poison),'complete false output/Fault/guards preserve original poison')
+        require('first' not in cert and 'priority' not in cert and source_proof['world0']['structural_guard_permits'],'no published World0 success; structural acceptance is source proof only')
+        # At E512/512/8192, cell0 contains the sphere, whereas neighbors and
+        # four XY outside planes are>=512 away, so the named cause is cell0.
+        require(eye==(512,512,8192) and 512>360 and -131072+360<eye[2]<131072-360,'literal cell0-interior refusal isolated from outer boundaries')
+        cert['identity_coverage']={'role':role,'source_proof':'D325_FIXED_INPUT_IDENTITY_1',
+          'actual_strict_refusal':True,'BODY_FALSE_SCALAR_ONLY':True,'published_world0_hit':False,
+          'absence_shade_unreachable_and_structural_guards':'SOURCE_CERTIFICATE_NOT_TARGET_SUCCESS'}
+        return True
+    require(response[:2]==bytes((1,1)) and response[2:10]==bytes(8),'actual independent successful result')
+    first,priority=cert.get('first'),cert.get('priority');root=cert.get('root')
+    require(type(first) is dict and type(priority) is dict and first.get('status')==priority.get('status')==1 and first.get('kind')==priority.get('kind')==1,'complete successful world witnesses')
+    if role=='xy-outside-first':
+        axis=0 if seed in (1,2) else 1;sign=1 if seed in (1,3) else -1
+        boundary=0 if sign>0 else 65536
+        time=F(sign*360+boundary-eye[axis],delta[axis]);identity=196607+seed
+        require(time==F(767,abs(delta[axis])) and sign*delta[axis]<0 and 0<time<1,'real closing XY outer plane root')
+        require(cert.get('feature_axes')==[axis] and cert.get('feature_signs')==[sign] and cert.get('feature')==2*axis+(sign>0),'real first face normal, opposite outside-region sign')
+        require(first==priority and first.get('id')==identity,'isolated XY first AND independently selected priority')
+        if not face:require(time==F(767,6144) and first['q']==536171861,'four literal exclusion XY first roots/bins')
+        coverage={'role':role,'actual_published_first':identity,'outside_candidate_is_first':True}
+    else:
+        lower=role=='lower-z-equal-candidate';require(lower or role=='upper-z-shadow-candidate','closed hidden-Z role')
+        sign=1 if lower else -1;boundary=-131072 if lower else 131072
+        cell_plane=-131072 if lower else 130048
+        time=F(cell_plane+sign*360-eye[2],delta[2])
+        candidate_time=F(boundary+sign*360-eye[2],delta[2])
+        require(time==(F(531,718) if lower else F(344,3179)) and candidate_time==(F(531,718) if lower else F(856,3179)),'exact cell-first and hidden outer candidate plane times')
+        require(0<time<=candidate_time<1 and sign*delta[2]<0,'actual closing physical Z-plane candidates within segment')
+        # At the candidate the other true outside halfspaces do not intervene;
+        # these are full primitive candidates even though a cell wins first.
+        candidate_center=tuple(F(eye[i])+delta[i]*candidate_time for i in range(3))
+        require(all(360<candidate_center[i]<65536-360 for i in (0,1)),'outer candidate interior XY feature validity')
+        center=tuple(F(eye[i])+delta[i]*time for i in range(3))
+        cell=tuple(center[i]//1024 for i in (0,1))
+        require(all(cell[i]*1024<center[i]<(cell[i]+1)*1024 for i in (0,1)),'unique original cell-face first, not edge/boundary alias')
+        identity=3*(64*cell[1]+cell[0])+(1 if lower else 2)
+        expected_ids=(6049,6241,6238,6046) if lower else (6050,6242,6239,6047)
+        require(identity==expected_ids[yaw//16384] and first.get('id')==identity and cert.get('feature_axes')==[2] and cert.get('feature_signs')==[sign] and cert.get('feature')==4+(sign>0),'real floor/ceiling face first and reviewed original-cell ID')
+        outer_id=196612 if lower else 196613;candidate_q=candidate_time.numerator*Q//candidate_time.denominator
+        require(priority.get('id')<outer_id and priority.get('id')!=0,'outer identity cannot replace independently selected cell priority')
+        if lower:
+            require(candidate_time==time and candidate_q==3176361607 and first['id']<outer_id,'lower-Z equal physical root loses stable identity')
+        else:
+            gap=sum(d*d for d in delta)*(candidate_q-first['q'])**2
+            require(candidate_time>time and delta[2]*(candidate_time-time)==1024 and gap>121*Q*Q,'upper-Z shadow beyond anchored11 Q32 group')
+        coverage={'role':role,'actual_published_first':identity,'outer_candidate_id':outer_id,
+          'outer_candidate_time':[candidate_time.numerator,candidate_time.denominator],
+          'outer_candidate_q':candidate_q,'outer_first_or_priority_unavailable':True,
+          'plane_proof':'BOUNDED_EXACT_ARITHMETIC_USING_EXISTING_RESULT_NOT_SECOND_SWEEP',
+          'source_proof':'D325_FIXED_INPUT_IDENTITY_1'}
+    q=time.numerator*Q//time.denominator
+    require(type(root) is dict and F(*root['lo'])==F(*root['hi'])==time and tuple(root['poly'])==oracle.primitive((-time,1)) and root['q']==q and cert.get('q')==q and first.get('q')==q,'independent own first rational root/time/bin')
+    require(response[82:134]==oracle.encode_hit(first) and first['id']!=0,'full coherent first obstruction, never Clear.id0 as World0')
+    if face:require(cert.get('feature')==rank,'all six real first face ranks retained')
+    coverage['real_first_time']=[time.numerator,time.denominator]
+    cert['identity_coverage']=coverage
+    return True
+
 def qk1_certificate(row,response,cert,oracle,angles):
     """D321 source-only literals; certify the REAL independent sweep result.
 
@@ -1279,7 +1464,7 @@
     require(tuple(cert.get('camera',()))==eye and all(oracle.nearest(F(d,Q))==0 for d in delta),'qs1 displacement rounding follows the checked root/backoff')
     return True
 
-def semantic_certificate(row,predicate,response,cert,oracle,angles):
+def semantic_certificate(row,predicate,response,cert,oracle,angles,bindings,identity_proof):
     """Every requested semantic key must be proved or explicitly returned.
 
     This checks independent arithmetic, never target output. Unproved literal
@@ -1318,6 +1503,8 @@
         checks['d287']=1424<=row['id']<1440 and row['aim']==((0,16384,32768,49152)[j],8000) and cert.get('L0')==5980 and cert.get('k')==23701325 and cert.get('q')==(747731 if g else 0) and cert['first']['id']==((6049,6241,6238,6046)[j] if g else 6046)
     if 'd321_q_k_plus_one' in predicate:
         checks['d321_q_k_plus_one']=qk1_certificate(row,response,cert,oracle,angles)
+    if 'd325_identity' in predicate:
+        checks['d325_identity']=identity_certificate(row,response,cert,oracle,angles,bindings,identity_proof)
     annotations={'pair','relation','member'}
     for key,value in predicate.items():
         if key in annotations:continue
@@ -1359,7 +1546,7 @@
 
 def build_catalog(oracle,items,tables,rules,bindings):
     angles=struct.unpack('<25386i',tables[:-64]);budget=oracle.Budget(START+300)
-    fixtures_=[dict(item,cells=list(struct.iter_unpack('<BbbB',item['cells']))) for item in items]
+    fixtures_,identity_proof=identity_fixture_certificate(items)
     requests=bytearray();expected=bytearray();catalog=[];missing=[];pairs={}
     for case_id in range(4096):
         tick()
@@ -1368,7 +1555,7 @@
             request=encode_row(row);decoded=oracle.decoded(request)
             need(decoded['id']==case_id,'literal ordered catalog')
             response,certificate=oracle.resolve(request,fixtures_,angles,rules,bindings,budget)
-            proved=semantic_certificate(row,predicate,response,certificate,oracle,angles)
+            proved=semantic_certificate(row,predicate,response,certificate,oracle,angles,bindings,identity_proof)
             entry={'id':case_id,'family':next(name for lo,hi,name in FAMILY_RANGES if lo<=case_id<hi),
                    'poison':row['poison'],'row_sha256':sha(request),'expected_sha256':sha(response),
                    'requested_predicates':predicate,'proved_predicates':proved,'certificate':certificate}
@@ -1396,6 +1583,7 @@
     return bytes(requests),bytes(expected),{'rows':catalog,'intervals':budget.intervals,'roots':budget.roots,
       'family_counts':{name:hi-lo for lo,hi,name in FAMILY_RANGES},'pairs':len(pairs),
       'unreachable_positive_q0':{'integer_slack':18422833818914243952,'replacement_rows':[1424,1440]},
+      'identity_reachability_source_certificate':identity_proof,
       'caller_authority_observer_and_motion_state':'NOT_PROVED_BY_NUMERIC_POSES'}
 
 def semantic_coverage(requests,expected,catalog,oracle):
@@ -1412,6 +1600,27 @@
         need(expected[160*j+1]==expected[160*(j+1)+1]==0 and expected[160*j+2:160*j+10]==expected[160*(j+1)+2:160*(j+1)+10],'same exact refusal tuple under both poisons')
     for j in range(1424,1440):need(catalog[j]['proved_predicates'].get('d287') is True,'all16 exact D287 rows')
     for j in range(1456,1472):need(catalog[j]['proved_predicates'].get('d321_q_k_plus_one') is True and decoded[j]['poison']==(j-1456)%2,'all16 exact D321 q=k+1 rows and both poisons')
+    roles={}
+    for j in range(2432,2496):
+        entry=catalog[j];coverage=entry['certificate'].get('identity_coverage',{})
+        need(entry['proved_predicates'].get('d325_identity') is True,'all64 adopted exclusion identity certificates')
+        role=coverage.get('role');roles[role]=roles.get(role,0)+1
+        need(entry['certificate']['body_feasible']==((j-2432)//8 not in (0,7)),'literal feasible versus scalar-only body labels')
+    need(roles=={'world0-strict-refusal':16,'xy-outside-first':32,'lower-z-equal-candidate':8,'upper-z-shadow-candidate':8},'honest published/candidate/refusal role counts')
+    for j in range(2432,2496,2):
+        a,b=dict(decoded[j]),dict(decoded[j+1]);a.pop('id');b.pop('id')
+        need(a.pop('poison')==0 and b.pop('poison')==1 and a==b,'both original poisons for each exclusion h/weapon seed')
+        need(expected[160*j+1]==expected[160*(j+1)+1] and expected[160*j+2:160*j+10]==expected[160*(j+1)+2:160*(j+1)+10],'same real success/refusal/Fault under both exclusion poisons')
+    for rank in range(6):
+        ids=range(512+64*rank+40,512+64*rank+48)
+        actual={(decoded[j]['aim'],decoded[j]['height'],decoded[j]['eye']) for j in ids}
+        pitch=0 if rank<4 else -8000 if rank==4 else 8000
+        wanted={((yaw,pitch),h,e) for yaw in IDENTITY_FACE_YAWS[rank] for h,e in ((3738,3174),(5325,4608))}
+        need(actual==wanted,'four actual face aims times two endpoint stances')
+        need(all(catalog[j]['proved_predicates'].get('d325_identity') is True and
+                 catalog[j]['certificate']['feature']==rank and expected[160*j+1]==1 and
+                 decoded[j]['weapon']==1 and decoded[j]['poison']==j%2 for j in ids),
+             'all48 real first face ranks and original per-row defaults')
     for j in range(2816,3072):need(decoded[j]['weapon']==0 and expected[160*j+46:160*j+58]==bytes(12),'all256 None muzzle fields')
     for j in range(512,1280):
         pred=catalog[j]['requested_predicates'];cert=catalog[j]['certificate']
@@ -1906,7 +2115,7 @@
         if group==0:row['count']=1+j%8;predicate={'clear':True,'actors_excluded':True}
         elif group==1:row['fixture']=1;row['foot']=(262144 if j%2 else 0,32768,8192);predicate={'refusal':True}
         elif group==2:
-            raise oracle.ConstructionRequired(case_id,'primitive0/six outside identities','exact first-versus-candidate identity and literal fixed-fixture mapping required')
+            return identity_exclusion_row(row,j)
         else:row['revision']=(1,2,7,255,65535,65536,0x7fffffff,0xffffffff)[j%8];predicate={'clear':True}
     elif case_id<2816:
         group,local=divmod(case_id-2560,32);seed,variant=divmod(local,4)
--- a/tests/outbreak/camera/release-1/SCHEMA.md
+++ b/tests/outbreak/camera/release-1/SCHEMA.md
@@ -1,6 +1,6 @@
 # Camera proof harness schema — source proposal 1
 
-T1901.1 / D305/D321 / CAMERA_FOUNDATION0.5. **NOT GENERATED, NOT COMPILED,
+T1901.2 / D305/D321/D325 / CAMERA_FOUNDATION0.6. **NOT GENERATED, NOT COMPILED,
 NOT EXECUTED, NOT ACCEPTED.** This file specifies future private harness bytes;
 it adds no production wire format, API, geometry hook or runtime caller.
 Corrected T182 sections4–8 and D287 govern. A later MAIN release must bind real
@@ -234,11 +234,97 @@
 The adopted review is
 `notes/reviews/T197-found-certificate-variants-review-1.md`,SHA256
 9bd6697798fed7fae9ac84505473c13c0f51192de019b4eacf361b37ab5f5bd0.
-This source correction resolves only that supplied stratum. All other open
-grazing/bin/near-tie/negative-half-tie/initial/primitive0/outside/caller/protection
-seams,4096/64/94 totals and every original bound remain. No corpus or target
-result has been produced or accepted here.
+That adoption resolves only the supplied q=k+1 stratum; its sixteen rows/checks
+remain unchanged by D325 below. Other grazing/bin/near-tie/negative-half-tie/
+initial/caller/protection seams,4096/64/94 totals and every original bound remain.
+No corpus or target result has been produced or accepted here.
 
+## D325 identity roles:64 exclusion plus48 real face-variant5 rows
+
+The exact adopted reachability review is
+`notes/reviews/T190-world-zero-outside-reachability-review-1.md`,SHA256
+7ef83b502b47d95eb8f1c5106695414e716aa3d4c8447ad893497f7c51f638a8.
+It distinguishes successful published FIRST, independent hidden/equal candidates,
+real strict-overlap refusals, and structural/source proof. Clear.id0 is never
+counted as a World.id0 Hit. General G2's actual World0/six-outside obligations
+remain; none is removed or replaced by camera's unavailable-publication proof.
+
+Exclusion case_id=`2432+8*s+4*h+2*w+p`;s0..7,h0C3738/3174,h1S5325/4608,
+w0Pistol/w1Rifle,p0/1 original poisons. Foot=Eye−(0,0,e),canonical unpatched
+rules/table,actors0/boxes0,world revision1,ordinary live fixture context.
+
+| s | Fixture/Eye | Aim yaw,pitch | Actual outcome and independent identity role |
+| ---: | --- | --- | --- |
+|0|F4,(512,512,8192)|0,0|strict cell0 refusal; full poison preserved; BODY_FALSE/scalar-only |
+|1|F1,(1127,32768,8192)|49152,0|outside−X196608 FIRST,root767/6144 |
+|2|F1,(64409,32768,8192)|16384,0|outside+X196609 FIRST,root767/6144 |
+|3|F1,(32768,1127,8192)|0,0|outside−Y196610 FIRST,root767/6144 |
+|4|F1,(32768,64409,8192)|32768,0|outside+Y196611 FIRST,root767/6144 |
+|5|F5,(32768,32768,−126464)|0,8000|floor6049 FIRST at531/718; lower outside196612 is equal-root candidate,loses stable ID |
+|6|F5,(32768,32768,129000)|0,−8000|ceiling6050 FIRST at344/3179; upper outside196613 candidate856/3179 is shadowed |
+|7|F7,(512,512,8192)|0,0|strict cell0 refusal; full poison preserved; BODY_FALSE/scalar-only |
+
+Rows s1..6 have independently feasible source bodies; s0/s7 explicitly do not.
+The four XY roots have q536171861 and independently equal first/priority.
+Lower-Z has q3176361607. Z-row priority is independently derived and may be a
+different eligible cell witness; it is never copied from first. The body/scalar
+labels do not grant gameplay authority or caller eligibility.
+
+For face variant5,case_id=`512+64*r+40+2*a+h`,r0..5,a0..3,h0..1.
+Preserve original per-row weaponPistol,poison=case_id%2 and other defaults.
+Use the corresponding XY Eye above or the same F5 Z Eye,not an altered fixture.
+
+| Real first normal r | Existing IDs | Four yaws,each with both endpoint(h,e) pairs | Real FIRST |
+| --- | --- | --- | --- |
+|0,−X|552..559|0,8192,16384,24576;pitch0|high-X outside196609 |
+|1,+X|616..623|32768,40960,49152,57344;pitch0|low-X outside196608 |
+|2,−Y|680..687|16384,24576,32768,40960;pitch0|high-Y outside196611 |
+|3,+Y|744..751|0,8192,49152,57344;pitch0|low-Y outside196610 |
+|4,−Z|808..815|0,16384,32768,49152;pitch−8000|ceiling6050/6242/6239/6047;upper outer candidate shadowed |
+|5,+Z|872..879|0,16384,32768,49152;pitch8000|floor6049/6241/6238/6046;lower outer candidate equal-root |
+
+The inward published normal is opposite the named outside region's sign.
+All48 rows must be actual successful first *face* contacts,retaining all six
+rank/sign groups and four distinct aims×two heights. Pitch0 original-rig D in
+yaw0,8192,...57344 order is(1280,−6144,307),(5250,−3439,307),
+(6144,1280,307),(3439,5250,307),(−1280,6144,307),(−5250,3439,307),
+(−6144,−1280,307),(−3439,−5250,307). XY root is767/abs(Dnormal).
+Z cardinal XY components follow the existing D321 cardinal rotations,with
+D.z−5744 for lower-Z or6358 for upper-Z. No arbitrary D is supplied to a target.
+
+`identity_certificate` checks exact row/context/body/rig; real independent
+first root/time/bin/feature/identity and complete obstruction; both exclusion
+poisons; and the declared role. It adds no sweep/root enumeration. Hidden-plane
+times are exact linear arithmetic from the existing eye/D and true plane at
+±131072: lower equals the real floor root; upper is separated by1024 in Z and
+fails the anchored11-Q32 eligibility predicate. It records those as candidates
+and unavailable publication,not as fabricated TraceHits. Cell0 cases require
+the actual oracle strict-overlap result with THEN-ACCEPTED G2 tuple and full
+prior solution/Fault/guard response; no tuple is guessed.
+
+`identity_fixture_certificate` adds summaries during the existing ONE decode
+of192512 fixed fixture cells: legal0/4/i8 cell domains; F1/F2/F3/F5 cell0 space
+(primitive0 absent); F0/F4/F6 cell0/east/north solids; F0 diagonal solid DATA;
+complete F7 all-solid membership. A pinned camera hit-guard source expression
+still admits a structurally valid World.id0 and all six outside IDs. These are
+source/structural facts,not actual target success or additional control cases.
+
+The adopted global proof is retained: upper ceiling union≤130048 shields
+upper outside131072 by≥1024; lower floor union≥−131072 precedes/ties lower
+outside,with every cell/XY identity lower than196612. Cell0 is absent or shaded
+by east/north solids/outside: at its purported rounded corner at least one
+neighbor is<255 away,so entry precedes by>105 path units,well outside11 even
+after<7732/Q flooring. Beyond Z endpoints a Z outside plane intervenes first;
+F7's complete solid union forces initial overlap. No World0 first/priority can
+be manufactured on these camera fixtures,while valid general G2 World0 rays
+and camera's structural guard remain intact. The proof's role is distinct
+from real112 target rows and the unchanged64 CONTROL_ONLY models.
+
+Coverage requires exactly32 real XY outside-FIRST exclusions,16 real Z
+cell-first/candidate exclusions,16 real cell0 refusals and48 successful face
+rows. All4096 original rows,64 controls,94 children,request512/response160,
+every data/work/time/frame bound and the sixteen D321 rows are unchanged.
+
 | Resource | Fixed bound |
 | --- | ---: |
 | requests |4096*512=2097152 |
--- a/tests/outbreak/camera/release-1/README.md
+++ b/tests/outbreak/camera/release-1/README.md
@@ -1,6 +1,6 @@
 # T190 camera harness — source review package
 
-**T1901.1 / D321 narrow own-source correction. SOURCE ONLY. NOT COMPILED /
+**T1901.2 / D325 narrow own-source correction. SOURCE ONLY. NOT COMPILED /
 NOT EXECUTED / NOT ACCEPTED.** No setup, request,
 golden, control result, preparation, attempt or final evidence has been
 generated by this package. D305 authorizes only these six new files and the
@@ -22,8 +22,8 @@
 Read corrected [T182](../../../../notes/proposals/T182-camera-implementation-release-packet-1.md)
 sections4–8, [T190](../../../../tickets/T190.md),
 [D305](../../../../notes/decisions/D305-camera-proof-harness-source-release.md),
-and [CAMERA_FOUNDATION0.5](../../../../MVP/CAMERA_FOUNDATION.md). D321 additionally
-adopts only the sixteen existing q=k+1 literals below. The adjacent
+and [CAMERA_FOUNDATION0.6](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
+sixteen existing q=k+1 literals; D325 supplies the exact identity/face roles below. The adjacent
 SCHEMA is private test framing, not a new gameplay interface. No code here
 implements MotionState, observer selection, authority or a usable game camera.
 
@@ -40,8 +40,9 @@
 The catalog is **not proved realizable**. Source `ConstructionRequired` gates
 remain for exact edge/corner tangency, shallow-face variants, near-Q32 bins,
 competing first/priority and same-bin roots, later graze/miss, initial
-nonclosing skip then later Hit, primitive0/six-outside identity interpretation,
-and negative displacement half-tie. Other literal candidates, including normal
+nonclosing skip then later Hit,and negative displacement half-tie.
+D325 now resolves the fixed-map identity interpretation and112 inputs below.
+Other literal candidates,including normal
 margin counterexamples, are also subject to exact feature/body/first/root
 checks; existence of a formula is not a passing certificate. Failed semantic
 checks return the affected row; no subset, label-only pass, count substitution,
@@ -91,6 +92,57 @@
 both poisons. No oracle, case generator, control, target or frame check ran in
 this correction; the six-source snapshot remains under review.
 
+## D325: reachable firsts,hidden candidates and primitive-zero refusals
+
+[D325](../../../../notes/decisions/D325-camera-identity-reachability-and-rows.md)
+adopts [the complete fixed-map reachability review](../../../../notes/reviews/T190-world-zero-outside-reachability-review-1.md),
+SHA2567ef83b502b47d95eb8f1c5106695414e716aa3d4c8447ad893497f7c51f638a8.
+Only verify.py's affected construction/semantic/coverage checks and these docs
+changed. The D321 literal table,routine and sixteen rows are preserved.
+oracle.py,wrapper.cpp,wasm_runner.mjs,production and old notes remain read-only.
+
+Existing64 exclusion rows2432..2495 now use2432+8*s+4*h+2*w+p,with independent
+endpoint height,weapon and original poison axes. Seed order is F4 cell0 strict
+refusal;F1 outside−X,+X,−Y,+Y actual firsts;F5 lower-Z equal-root floor-first;
+F5 upper-Z shadowed ceiling-first;F7 cell0 strict refusal. Source bodies are
+feasible except the two explicit cell0 BODY_FALSE/scalar-only seeds. SCHEMA
+lists every eye/aim/root/identity and both endpoint pairs.
+
+The four XY identities196608..196611 are real successful firsts,not priority
+substitutes. Outside-Z196612 is an independently certified equal-root candidate
+losing to a smaller floor ID;outside+Z196613 is a later plane candidate behind
+the real ceiling union. Actual floor/ceiling firsts are6049/6050 for exclusion
+yaw0; other eligible cell priorities remain independently computed. A plane
+candidate is never encoded as a successful published outside-Z obstruction.
+Primitive0 is absent or shaded beyond the11 window on the fixed maps,or causes
+genuine initial strict-overlap refusal. F4/F7 Eye(512,512,8192) rows observe that
+real false result and preserve both complete output poisons using accepted G2
+Fault bindings. Canonical Clear.id0 is not World.id0; source structural guard
+acceptance and separate general G2 World0 success obligations remain intact.
+
+The48 face-variant5 rows retain all actual first normal ranks−X,+X,−Y,+Y,−Z,+Z,
+using exactly row512+64*r+40+2*a+h and four literal aims×two endpoint heights.
+XY normals use the opposite outside-region sign. Z faces are real F5 ceiling/
+floor firsts with hidden/equal outside candidates,not falsely published Z outer
+IDs. Original face weapon/poison/defaults and complete first/priority records
+remain. Coverage checks require all48 real face ranks and all64 truthful roles.
+
+`identity_fixture_certificate` derives complete-input summaries in the existing
+single192512-cell decode,checks the local solid-neighbor shade/space absence,
+full F7 all-solid geometry,i8 floor/ceiling bounds,stable ID order and pinned
+camera guard. This source proof distinguishes unavailable camera first/priority
+from valid general G2/structural World0. `identity_certificate` uses the existing
+independent result to check each actual root/bin/first/body/refusal; exact plane
+arithmetic supplements hidden-Z candidate/root/shadow certificates. It never
+calls another sweep,outside/box candidate stream or root enumeration. Physical
+oracle limits and every original bound remain unchanged. Source/structural
+proof,64 CONTROL_ONLY models and real target rows remain separate claims.
+
+Nothing in this source correction generated a corpus or ran an oracle,control,
+query,target,compiler or runtime. Other literal,authority/protection/native
+closure/full realG2/current G1/frame/caller/gameplay/performance/human gates
+remain. Whole package is under source review; no automatic preparation follows.
+
 THEN-ACCEPTED G2 false tuples/validation order, full real G2 evidence, and current
 changed-source G1 regression are required data bindings. Current geometry.cpp is
 unverified context. `BindingRequired` or the release gate refuses unknown data;
```

