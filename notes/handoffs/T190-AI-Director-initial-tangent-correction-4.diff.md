# T1901.3 — exact initial tangent correction diff

D334 / CAMERA_FOUNDATION0.7. Complete unified textual diff against the captured
T1901.2 three-file snapshot,with three context lines. Only source strings were
compared; no Python/C++/Node parser,helper,oracle,generator,test or target ran.
D321/D325 routines/mappings and64-control/94-command sections remain textually
unchanged as recorded in the NEW correction handoff. No second sweep/root stream/
map decode or output replacement is introduced by the new tangent checker.

```diff
--- a/tests/outbreak/camera/release-1/verify.py
+++ b/tests/outbreak/camera/release-1/verify.py
@@ -1066,6 +1066,18 @@
  (0,16384,32768,49152),(0,16384,32768,49152))
 IDENTITY_XY_RIGS=((1280,-6144,307),(5250,-3439,307),(6144,1280,307),(3439,5250,307),
  (-1280,6144,307),(-5250,3439,307),(-6144,-1280,307),(-3439,-5250,307))
+# D334 exact1344+2*j+p inputs and comparison-only paper expectations.
+# yaw,original rig D,new floor ID,own point,camera,muzzle. No response replaces
+# oracle.resolve's complete independently calculated160-byte expected result.
+TANGENT_LITERALS=(
+ (0,(1280,-6136,0),5857,(32982,31744,0),(32975,31776,360),(33126,33433,-119)),
+ (8192,(5244,-3434,0),6052,(33792,32097,0),(33764,32116,360),(32551,33491,-119)),
+ (16384,(6136,1280,0),6244,(33792,32982,0),(33760,32975,360),(32103,33126,-119)),
+ (24576,(3434,5244,0),6433,(33439,33792,0),(33420,33764,360),(32045,32551,-119)),
+ (32768,(-1280,6136,0),6430,(32554,33792,0),(32561,33760,360),(32410,32103,-119)),
+ (40960,(-5244,3434,0),6235,(31744,33439,0),(31772,33420,360),(32985,32045,-119)),
+ (49152,(-6136,-1280,0),6043,(31744,32554,0),(31776,32561,360),(33433,32410,-119)),
+ (57344,(-3434,-5244,0),5854,(32097,31744,0),(32116,31772,360),(33491,32985,-119)))
 FAMILY_RANGES=((0,512,'free'),(512,1280,'blocker'),(1280,1536,'initial'),
  (1536,1792,'recovery'),(1792,2304,'stance'),(2304,2560,'exclusion'),
  (2560,2816,'rounding'),(2816,3072,'none'),(3072,3584,'refusal'),(3584,4096,'metamorphic'))
@@ -1464,7 +1476,83 @@
     require(tuple(cert.get('camera',()))==eye and all(oracle.nearest(F(d,Q))==0 for d in delta),'qs1 displacement rounding follows the checked root/backoff')
     return True
 
-def semantic_certificate(row,predicate,response,cert,oracle,angles,bindings,identity_proof):
+def initial_tangent_certificate(row,response,cert,oracle,angles,fixture,identity_proof):
+    """D334 supplement to the EXISTING complete oracle result.
+
+    Five named already-decoded cells plus fixed plane/window arithmetic only:
+    no second map decode, sweep, root stream, traversal or output substitute.
+    The original F1 fixture is the fixed uniform0/16 source construction.
+    """
+    def require(condition,detail):
+        if not condition:raise oracle.ConstructionRequired(row['id'],'D334 initial tangent/later Hit',detail)
+    require(1344<=row['id']<1360,'exact existing16-row range')
+    j,p=divmod(row['id']-1344,2);yaw,delta,identity,point,camera,muzzle=TANGENT_LITERALS[j]
+    eye=(32768,32768,360)
+    require(yaw==YAWS[j] and row['aim']==(yaw,286) and row['poison']==p,'eight original yaws and both original poisons')
+    require(row['fixture']==1 and row['foot']==(32768,32768,-2814) and row['height']==3738 and row['eye']==3174 and row['weapon']==1,'original F1/default Crouch/Pistol and exact scalar pose')
+    require(row['flags']==0 and row['revision']==1 and row['count']==row['boxes']==0 and row['slot']==65535 and row['rule_value']==0 and row['table_kind']==row['table_index']==row['table_value']==0,'canonical unpatched live context/defaults')
+    require(-131072<=row['foot'][2] and row['foot'][2]+row['height']==924 and row['height']-row['eye']==564,'scalar-valid domain; no living source permission')
+    require(fixture['side']==64 and fixture['revision']==1 and fixture['entities']==0 and len(fixture['cells'])==4096 and
+            identity_proof['fixtures'][1]['cell0']==[4,0,16,0] and identity_proof['fixtures'][1]['lowest_floor']==0 and
+            identity_proof['fixtures'][1]['highest_ceiling']==16,'original fixed F1 and existing one-decode source summary')
+    require(response[:2]==bytes((1,1)) and response[2:10]==bytes(8) and cert.get('physical_query') is True and cert.get('body_feasible') is False,'successful independent sweep, BODY_FALSE/SCALAR_VALID_ONLY')
+    require(tuple(cert.get('eye',()))==eye and tuple(cert.get('delta',()))==delta and rig(row,oracle,angles)==delta and delta[2]==0,'independent accepted-basis full-sum tangent rig')
+    scale=1<<30
+    require((angles[8192],angles[16384],angles[16385+286],angles[16385+8714])==(759250125,scale,53575089,1072404408),'four named certified angle DATA entries')
+    forward,right=((0,1072404408,53575089),(scale,0,0)) if j%2==0 else ((-758304429,758304429,53575089),(759250124,759250124,0))
+    for _ in range(j//2):
+        forward=(-forward[1],forward[0],forward[2]);right=(-right[1],right[0],right[2])
+    require(0<307*scale-6144*forward[2]<scale//2 and right[2]==0,'exact zero vertical rig after ONE complete sum rounding')
+    touched=((31,31),(32,31),(31,32),(32,32));skipped=[]
+    for x,y in touched:
+        require(fixture['cells'][64*y+x]==(4,0,16,0),'named initial floor cell')
+        dx=eye[0]-max(1024*x,min(eye[0],1024*(x+1)))
+        dy=eye[1]-max(1024*y,min(eye[1],1024*(y+1)))
+        require(dx*dx+dy*dy+eye[2]*eye[2]==360*360 and dx*delta[0]+dy*delta[1]+eye[2]*delta[2]==0,'initial exact360 equality and nonclosing derivative0')
+        skipped.append(3*(64*y+x)+1)
+    require(skipped==[6046,6049,6238,6241] and identity not in skipped and cert.get('initial_distance_squared')==360*360,'four whole-primitive skips; later identity must be new')
+    major=max(range(2),key=lambda axis:abs(delta[axis]));minor=1-major;v=abs(delta[major])
+    time=F(1024,v);q=716761165 if j%2==0 else 838681638;remainder=333 if j%2==0 else 358
+    require(v==(6136 if j%2==0 else 5244) and time==(F(128,767) if j%2==0 else F(256,1311)) and
+            time.numerator*Q==time.denominator*q+remainder,'later double-root time and exact floor-Q32 remainder')
+    root=cert.get('root')
+    require(type(root) is dict and F(*root['lo'])==F(*root['hi'])==time and tuple(root['poly'])==oracle.primitive((-time,1)) and root['q']==q,'actual oracle own rational entering root, not a t0/constant-face omission')
+    entry_poly=(1024*1024,-2048*v,v*v)
+    require(entry_poly[1]*entry_poly[1]-4*entry_poly[0]*entry_poly[2]==0 and
+            1024-v*time==0 and 2*v*(v*time-1024)==0 and 0<time<1,'adjacent pre-entry polynomial(1024-v*t)^2 and double-root derivative')
+    cell=[0,0];cell[major]=33 if delta[major]>0 else 30;cell[minor]=32 if delta[minor]>0 else 31
+    center=tuple(F(eye[i])+delta[i]*time for i in range(3))
+    require(fixture['cells'][64*cell[1]+cell[0]]==(4,0,16,0) and 3*(64*cell[1]+cell[0])+1==identity and
+            center[major]==(33792 if delta[major]>0 else 31744) and cell[minor]*1024<center[minor]<(cell[minor]+1)*1024 and center[2]==360,'unique new floor and exact physical-root face validity')
+    horizon=time+F(11,6268)+F(1,Q)
+    require(horizon<F(1,5) and F(abs(delta[major]),5)<2048 and F(abs(delta[minor]),5)<1024,'full anchored11 window has only one new non-skipped floor identity')
+    require(all(32768-abs(delta[i])>360 for i in (0,1)) and 16384-eye[2]>360 and
+            eye[2]+131072>360 and 131072-eye[2]>360,'complete fixed F1 ceiling/outside separation over whole boom')
+    first,priority=cert.get('first'),cert.get('priority');distance=1046 if j%2==0 else 1224
+    literal_hit={'status':1,'kind':1,'id':identity,'actor':(65535,0,0),'q':q,'distance':distance,
+                 'point':point,'normal':(0,0,scale),'zone':0,'origin':0}
+    require(first==priority==literal_hit and cert.get('q')==q and cert.get('feature_axes')==[2] and cert.get('feature_signs')==[1] and cert.get('feature')==5,'complete independently calculated NEW first/priority own witness and D327 canonical face5')
+    a=sum(d*d for d in delta);length=math.isqrt(a);k=(33*Q+length-1)//length;qs=q-k
+    require(a==(39288896 if j%2==0 else 39291892) and length==6268 and k==22612304 and
+            (cert.get('L0'),cert.get('k'),cert.get('qs'),cert.get('clamped'))==(length,k,qs,False) and
+            qs==(694148861 if j%2==0 else 816069334),'nonclamped original ceil33 backoff')
+    require(oracle.offset(eye,forward,right,(-6144,1280,307))==tuple(eye[i]+delta[i] for i in range(3)) and
+            oracle.offset(eye,forward,right,(666,358,-512))==muzzle and
+            tuple(eye[i]+oracle.nearest(F(delta[i]*qs,Q)) for i in range(3))==camera and tuple(cert.get('camera',()))==camera,'original full-sum rig/Eye-based Pistol muzzle/signed displacement rounding')
+    for off,value in ((10,eye),(22,tuple(eye[i]+delta[i] for i in range(3))),(34,camera),(46,muzzle),(58,forward),(70,right)):
+        require(struct.unpack_from('<iii',response,off)==value,'all logical solution fields remain independent complete response values')
+    require(response[82:134]==oracle.encode_hit(first) and response[134:147]==bytes(0x80+3*p+i for i in range(13)) and
+            response[147:160]==bytes(0xa0+3*p+i for i in range(13)),'full own obstruction and both original guard patterns')
+    require(cert.get('physical358_safe') is True and cert.get('projected_margin_ge31') is True and
+            cert.get('normal_margin_lt31') is True and camera[2]==360 and camera[2]-358==2,'physical358 safe by2; original-boom projected margin, not normal31')
+    cert['initial_tangent_coverage']={'source_adoption':'D334','initial_skipped_floor_ids':skipped,
+      'initial_distance_squared':129600,'initial_closing_dot':0,'entry_poly_constant_linear_quadratic':list(entry_poly),
+      'later_time':[time.numerator,time.denominator],'new_floor_first_and_priority':identity,'canonical_face':5,
+      'priority_window_upper':[1,5],'BODY_FALSE_SCALAR_VALID_ONLY':True,
+      'proof_method':'EXISTING_RESULT_FIVE_DECODED_CELLS_FIXED_WINDOW_ARITHMETIC_NO_SECOND_SWEEP'}
+    return True
+
+def semantic_certificate(row,predicate,response,cert,oracle,angles,bindings,identity_proof,fixtures_):
     """Every requested semantic key must be proved or explicitly returned.
 
     This checks independent arithmetic, never target output. Unproved literal
@@ -1505,6 +1593,8 @@
         checks['d321_q_k_plus_one']=qk1_certificate(row,response,cert,oracle,angles)
     if 'd325_identity' in predicate:
         checks['d325_identity']=identity_certificate(row,response,cert,oracle,angles,bindings,identity_proof)
+    if 'd334_initial_tangent' in predicate:
+        checks['d334_initial_tangent']=initial_tangent_certificate(row,response,cert,oracle,angles,fixtures_[1],identity_proof)
     annotations={'pair','relation','member'}
     for key,value in predicate.items():
         if key in annotations:continue
@@ -1555,7 +1645,7 @@
             request=encode_row(row);decoded=oracle.decoded(request)
             need(decoded['id']==case_id,'literal ordered catalog')
             response,certificate=oracle.resolve(request,fixtures_,angles,rules,bindings,budget)
-            proved=semantic_certificate(row,predicate,response,certificate,oracle,angles,bindings,identity_proof)
+            proved=semantic_certificate(row,predicate,response,certificate,oracle,angles,bindings,identity_proof,fixtures_)
             entry={'id':case_id,'family':next(name for lo,hi,name in FAMILY_RANGES if lo<=case_id<hi),
                    'poison':row['poison'],'row_sha256':sha(request),'expected_sha256':sha(response),
                    'requested_predicates':predicate,'proved_predicates':proved,'certificate':certificate}
@@ -1600,6 +1690,11 @@
         need(expected[160*j+1]==expected[160*(j+1)+1]==0 and expected[160*j+2:160*j+10]==expected[160*(j+1)+2:160*(j+1)+10],'same exact refusal tuple under both poisons')
     for j in range(1424,1440):need(catalog[j]['proved_predicates'].get('d287') is True,'all16 exact D287 rows')
     for j in range(1456,1472):need(catalog[j]['proved_predicates'].get('d321_q_k_plus_one') is True and decoded[j]['poison']==(j-1456)%2,'all16 exact D321 q=k+1 rows and both poisons')
+    for j in range(1344,1360):
+        need(catalog[j]['proved_predicates'].get('d334_initial_tangent') is True and
+             catalog[j]['certificate']['initial_tangent_coverage']['initial_skipped_floor_ids']==[6046,6049,6238,6241] and
+             catalog[j]['certificate']['body_feasible'] is False and expected[160*j+1]==1 and
+             decoded[j]['poison']==(j-1344)%2,'all16 adopted exact tangents with later real face Hit and both poisons')
     roles={}
     for j in range(2432,2496):
         entry=catalog[j];coverage=entry['certificate'].get('identity_coverage',{})
@@ -2075,8 +2170,10 @@
             row['aim']=(YAWS[j],8000);near_plane(row,oracle,angles,-2 if stratum==0 else -1);predicate={'refusal':True,'body_feasible':False}
         elif stratum==2:
             row['aim']=(YAWS[j],8000);near_plane(row,oracle,angles,0);predicate={'root_equals':[0,1],'clamped':True,'body_feasible':False}
-        elif stratum in (3,4,5):
-            if stratum==4:raise oracle.ConstructionRequired(case_id,'initial tangent','literal exact nonclosing tangent rig variant pending')
+        elif stratum==4:
+            row.update(fixture=1,weapon=1,height=3738,eye=3174,aim=(YAWS[j],286),foot=(32768,32768,-2814))
+            return row,{'hit':True,'clamped':False,'body_feasible':False,'d334_initial_tangent':True}
+        elif stratum in (3,5):
             row['aim']=(YAWS[j],-8000);row['fixture']=1;row['foot']=(32768,32768,360-row['eye']);predicate={'clear':True,'body_feasible':False}
         elif stratum==6:
             row['aim']=(YAWS[j],8000);near_plane(row,oracle,angles,1);predicate={'hit':True,'clamped':True}
--- a/tests/outbreak/camera/release-1/SCHEMA.md
+++ b/tests/outbreak/camera/release-1/SCHEMA.md
@@ -1,6 +1,6 @@
 # Camera proof harness schema — source proposal 1
 
-T1901.2 / D305/D321/D325 / CAMERA_FOUNDATION0.6. **NOT GENERATED, NOT COMPILED,
+T1901.3 / D305/D321/D325/D334 / CAMERA_FOUNDATION0.7. **NOT GENERATED, NOT COMPILED,
 NOT EXECUTED, NOT ACCEPTED.** This file specifies future private harness bytes;
 it adds no production wire format, API, geometry hook or runtime caller.
 Corrected T182 sections4–8 and D287 govern. A later MAIN release must bind real
@@ -325,6 +325,60 @@
 rows. All4096 original rows,64 controls,94 children,request512/response160,
 every data/work/time/frame bound and the sixteen D321 rows are unchanged.
 
+## D334 exact initial tangent rows with later NEW cell-face Hit
+
+Existing rows1344..1359 now use exactly case_id=`1344+2*j+p`,j0..7,p0/1,
+under D334 and the accepted T201 paper proposal
+`notes/proposals/T201-initial-tangent-construction-1.md`,SHA256
+c93092fb732534cb6ad0ef810233053e739eb89a0cc34ea0f85a62a6fa7bb70e.
+MAIN's independent review is
+`notes/reviews/MAIN-T201-initial-tangent-literal-review-1.md`.
+
+All16 use F1,Eye(32768,32768,360),foot(32768,32768,−2814),Pistol,
+h3738/e3174,pitch286,eight original yaws,canonical unpatched context,
+actors0/boxes0,revision1 and both original full solution/Fault/guard poisons.
+All are **BODY_FALSE / SCALAR_VALID_ONLY**: top924 and gap564 are numeric-valid,
+but the living capsule penetrates floor0. No caller/observer/source permission.
+
+|j/yaw|Exact original rig D|NEW first AND priority floor ID|Exact later time / q|Own point / travel floor|
+| --- | --- | ---: | --- | --- |
+|0/0|(1280,−6136,0)|5857|128/767 /716761165|(32982,31744,0) /1046|
+|1/8192|(5244,−3434,0)|6052|256/1311 /838681638|(33792,32097,0) /1224|
+|2/16384|(6136,1280,0)|6244|128/767 /716761165|(33792,32982,0) /1046|
+|3/24576|(3434,5244,0)|6433|256/1311 /838681638|(33439,33792,0) /1224|
+|4/32768|(−1280,6136,0)|6430|128/767 /716761165|(32554,33792,0) /1046|
+|5/40960|(−5244,3434,0)|6235|256/1311 /838681638|(31744,33439,0) /1224|
+|6/49152|(−6136,−1280,0)|6043|128/767 /716761165|(31744,32554,0) /1046|
+|7/57344|(−3434,−5244,0)|5854|256/1311 /838681638|(32097,31744,0) /1224|
+
+Four initially touched floor IDs6046/6049/6238/6241 each have exact distance360
+and closing derivative0; each is skipped for the whole primitive. The query
+does not become Clear. For the new cell the adjacent entry polynomial is
+(1024−v*t)²,v6136/5244. Its positive double root enters a constant closed
+floor face; D327 keeps that exact root/identity and canonical +Z face5,
+normal(0,0,1073741824),not an edge tag classified at q. All anchored11-eligible
+physical times are below1/5; no second dominant or first minor cell boundary
+is reached in that window. Complete F1 ceiling/outside separation excludes
+other geometry. First and priority are independently derived equal own hits.
+
+`initial_tangent_certificate` checks the existing complete independent oracle
+result against exact inputs/angles/basis/rig/body,initial equalities and skip
+IDs,new cell/entry polynomial/root/bin/feature,all own witness fields,
+L06268,k22612304,nonclamped qs694148861/816069334,signed displacement rounding,
+Eye-based logical Pistol muzzle,all solution fields and both guard patterns.
+It uses only five named cells from the already decoded F1 plus bounded exact
+plane/window arithmetic; no second sweep,root enumeration or map decode.
+All160 expected bytes still come from the existing oracle and are compared
+against each future target; literal checks never replace that response stream.
+
+The physical358 boom/final camera remains safe by2 at Z360. Nonclamped original-
+boom projected margin exceeds31; expanded-floor normal setback is0,not31.
+Coverage requires all16 successful later-Hit certificates and both original
+poisons. D321's16 rows,D325's112 rows/routines,all remaining strata,
+4096/64/94 totals and every original cap remain unchanged. This source
+construction is unexecuted; no complete catalog,query/target/frame/caller or
+full-package acceptance follows.
+
 | Resource | Fixed bound |
 | --- | ---: |
 | requests |4096*512=2097152 |
--- a/tests/outbreak/camera/release-1/README.md
+++ b/tests/outbreak/camera/release-1/README.md
@@ -1,6 +1,6 @@
 # T190 camera harness — source review package
 
-**T1901.2 / D325 narrow own-source correction. SOURCE ONLY. NOT COMPILED /
+**T1901.3 / D334 narrow initial-tangent source correction. SOURCE ONLY. NOT COMPILED /
 NOT EXECUTED / NOT ACCEPTED.** No setup, request,
 golden, control result, preparation, attempt or final evidence has been
 generated by this package. D305 authorizes only these six new files and the
@@ -22,8 +22,9 @@
 Read corrected [T182](../../../../notes/proposals/T182-camera-implementation-release-packet-1.md)
 sections4–8, [T190](../../../../tickets/T190.md),
 [D305](../../../../notes/decisions/D305-camera-proof-harness-source-release.md),
-and [CAMERA_FOUNDATION0.6](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
-sixteen existing q=k+1 literals; D325 supplies the exact identity/face roles below. The adjacent
+and [CAMERA_FOUNDATION0.7](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
+sixteen existing q=k+1 literals; D325 supplies112 identity/face rows; D334 supplies
+sixteen initial-tangent/later-Hit rows below. The adjacent
 SCHEMA is private test framing, not a new gameplay interface. No code here
 implements MotionState, observer selection, authority or a usable game camera.
 
@@ -143,6 +144,45 @@
 closure/full realG2/current G1/frame/caller/gameplay/performance/human gates
 remain. Whole package is under source review; no automatic preparation follows.
 
+## D334: exact initial tangency followed by a new floor-face Hit
+
+[D334](../../../../notes/decisions/D334-camera-initial-tangent-source-literals.md)
+adopts [T201's exact paper construction](../../../../notes/proposals/T201-initial-tangent-construction-1.md),
+SHA256c93092fb732534cb6ad0ef810233053e739eb89a0cc34ea0f85a62a6fa7bb70e,
+after [MAIN's independent review](../../../../notes/reviews/MAIN-T201-initial-tangent-literal-review-1.md).
+Exactly1344+2*j+p now uses F1,Eye(32768,32768,360),foot(32768,32768,−2814),
+default h3738/e3174/Pistol,pitch286,eight original yaws,and both original
+full-output/Fault/guard poisons. Every variant is BODY_FALSE/scalar-only.
+
+The original one-full-sum rig has Dz0 exactly. Four floor IDs6046/6049/6238/6241
+initially touch at radius360 with derivative0 and are skipped nonclosingly for
+the whole primitive. A NEW floor cell later has an entry double root at128/767
+or256/1311. Under D327 its physical root remains while its minimum closed
+feature is +Z face5,normal(0,0,1073741824). The complete query is later Hit,
+not Clear or a reused initially skipped identity. Full first/priority IDs by
+yaw are5857,6052,6244,6433,6430,6235,6043,5854;all eligible times are below1/5,
+where only that new non-skipped cell can contact. Normal/point/time stay coherent.
+
+The bounded `initial_tangent_certificate` checks those facts against the ONE
+existing independent oracle result. It inspects five named already-decoded F1
+cells and supplements exact plane/finite-window arithmetic,with no map decode,
+second sweep,root enumeration or fabricated response. It also checks exact
+row/defaults,certified basis/rig/angles,body/initial equality,new cell/root/bin,
+full own first=priority witness,L06268,k22612304,nonclamped signed backoff,
+Eye-based Pistol muzzle,all logical solution fields/guards and physical358/
+original-boom projected margin. Full expected160-byte responses remain generated
+by the existing oracle and compared in full against future real targets.
+
+This correction replaces only the initial-tangent ConstructionRequired gate.
+It preserves D321's16 and D325's112 literal mappings/routines,all other rows,
+64control labels/suite,94-command plan,and every original bound. The normal
+setback along +Z is0;physical358 clearance is2,while projected margin exceeds31.
+No valid runtime source or observer/shot behavior is inferred from these
+BODY_FALSE scalars. Other grazing/near-bin/near-tie/half-tie/initial and complete
+source/catalog/G2/current-G1/frame/caller/gameplay/human gates remain.
+No source,oracle,generator,control,target or compiler was executed by this
+correction,and no output root or automatic next stage is authorized.
+
 THEN-ACCEPTED G2 false tuples/validation order, full real G2 evidence, and current
 changed-source G1 regression are required data bindings. Current geometry.cpp is
 unverified context. `BindingRequired` or the release gate refuses unknown data;
```

