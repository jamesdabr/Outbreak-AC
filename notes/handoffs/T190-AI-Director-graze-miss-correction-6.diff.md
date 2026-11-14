# T1901.5 / D355 focused three-source diff

Complete source-text comparison against the captured T1901.4 snapshot. No parser, import or project execution.

```diff
--- a/tests/outbreak/camera/release-1/verify.py
+++ b/tests/outbreak/camera/release-1/verify.py
@@ -1078,6 +1078,14 @@
  (40960,(-5244,3434,0),6235,(31744,33439,0),(31772,33420,360),(32985,32045,-119)),
  (49152,(-6136,-1280,0),6043,(31744,32554,0),(31776,32561,360),(33433,32410,-119)),
  (57344,(-3434,-5244,0),5854,(32097,31744,0),(32116,31772,360),(33491,32985,-119)))
+# D345/D355 existing1392..1423 only. yaw,D,corner,solid ID,
+# graze EyeXY phases,miss EyeXY phases,graze cameraXY. Comparison-only
+# literals never replace the ONE complete independent oracle response.
+GRAZE_MISS_LITERALS=(
+ (0,(1280,-3072,5628),(20480,20480),3705,((20800,20648),(20795,20660)),((20798,20653),(20793,20665)),(20806,20634)),
+ (16384,(3072,1280,5628),(16384,20480),3696,((16216,20800),(16204,20795)),((16211,20798),(16199,20793)),(16230,20806)),
+ (32768,(-1280,3072,5628),(16384,16384),3120,((16064,16216),(16069,16204)),((16066,16211),(16071,16199)),(16058,16230)),
+ (49152,(-3072,-1280,5628),(20480,16384),3129,((20648,16064),(20660,16069)),((20653,16066),(20665,16071)),(20634,16058)))
 FAMILY_RANGES=((0,512,'free'),(512,1280,'blocker'),(1280,1536,'initial'),
  (1536,1792,'recovery'),(1792,2304,'stance'),(2304,2560,'exclusion'),
  (2560,2816,'rounding'),(2816,3072,'none'),(3072,3584,'refusal'),(3584,4096,'metamorphic'))
@@ -1656,6 +1664,174 @@
       'proof_method':'EXISTING_COMPLETE_RESULT_FIXED_F1_PLANES_BOUNDED_ARITHMETIC_NO_SECOND_SWEEP'}
     return True
 
+def graze_miss_certificate(row,response,cert,oracle,angles,fixture,identity_proof):
+    """D355 fixed edge/clamp/full-F4 proof against the EXISTING result.
+
+    The unchanged fixtures() F4 construction is the full geometry premise.
+    Six named existing decoded cells and bounded arithmetic supplement it;
+    no additional decode, sweep, root stream, constructor or output producer.
+    """
+    def require(condition,detail):
+        if not condition:raise oracle.ConstructionRequired(row['id'],'D355 later graze/curved miss',detail)
+    require(1392<=row['id']<1424,'exact existing32-row range')
+    miss=row['id']>=1408;base=1408 if miss else 1392
+    r,a,p=(row['id']-base)//4,((row['id']-base)//2)%2,(row['id']-base)%2
+    yaw,delta,corner,identity,graze_eyes,miss_eyes,camera_xy=GRAZE_MISS_LITERALS[r]
+    eye=(*(miss_eyes if miss else graze_eyes)[a],361)
+    require(row['fixture']==4 and row['weapon']==1 and row['height']==3738 and row['eye']==3174 and
+            row['foot']==(eye[0],eye[1],-2813) and row['aim']==(yaw,-6000) and row['poison']==p,
+            'exact F4/Pistol/Crouch/cardinal/two-phase/poison association')
+    require(row['flags']==0 and row['revision']==1 and row['count']==row['boxes']==0 and
+            row['slot']==65535 and row['rule_value']==0 and
+            row['table_kind']==row['table_index']==row['table_value']==0,'canonical unpatched defaults')
+    require(response[:2]==bytes((1,1)) and response[2:10]==bytes(8) and
+            cert.get('physical_query') is True and cert.get('body_feasible') is False,
+            'complete independent success; BODY_FALSE/SCALAR_VALID_ONLY, not runtime source')
+    scale=1<<30
+    require((angles[0],angles[16384],angles[16385+3000],angles[16385+6000])==
+            (0,scale,536870912,929887697),'four named certified angle DATA values')
+    forward,right=oracle.basis(angles,yaw,-6000)
+    f0,r0=(0,536870911,-929887696),(scale,0,0)
+    u=((318,173),(313,185))[a] if miss else ((320,168),(315,180))[a]
+    offset=u;v=(1280,-3072);rig_delta=(1280,-3072,5628)
+    muzzle_offset=(358,333,-1089);own_normal=(991146298,412977625,0)
+    for _ in range(r):
+        f0=(-f0[1],f0[0],f0[2]);r0=(-r0[1],r0[0],r0[2])
+        offset=(-offset[1],offset[0]);rig_delta=(-rig_delta[1],rig_delta[0],rig_delta[2])
+        muzzle_offset=(-muzzle_offset[1],muzzle_offset[0],muzzle_offset[2])
+        own_normal=(-own_normal[1],own_normal[0],0)
+    require((forward,right)==(f0,r0) and delta==rig_delta and rig(row,oracle,angles)==delta and
+            tuple(cert.get('eye',()))==eye and tuple(cert.get('delta',()))==delta and
+            tuple(eye[j]-corner[j] for j in (0,1))==offset,'normalized basis/full-sum original rig and actual local placement')
+    length2=sum(d*d for d in delta);length=math.isqrt(length2);k=(33*Q+length-1)//length
+    require((length2,length,k)==(42749968,6538,21678483) and
+            (cert.get('L0'),cert.get('k'))==(length,k),'full boom norm and ceil33 backoff')
+    aa=sum(d*d for d in v);bb=2*sum(u[j]*v[j] for j in (0,1));cc=sum(d*d for d in u)-360*360
+    target_initial=cc+360*360
+    coefficients=((11075584,-248832,1453),(11075584,-335360,2594)) if miss else ((11075584,-212992,1024),(11075584,-299520,2025))
+    require((aa,bb,cc)==coefficients[a],
+            'actual edge distance polynomial, not a plane/parallel-gap substitute')
+    require(target_initial==((131053,132194) if miss else (130624,131625))[a] and
+            target_initial>361*361 and cert.get('initial_distance_squared')==361*361,
+            'true WHOLE-WORLD initial361; separately larger target-local initial squared distance')
+    time=F(-bb,2*aa);clamp_time=F(u[1],3072)
+    closest=tuple(F(u[j])+v[j]*time for j in (0,1));minimum2=sum(d*d for d in closest)
+    require(0<time<clamp_time<1 and all(d>0 for d in closest) and
+            2*aa*time+bb==0 and aa*time*time+bb*time+cc==minimum2-360*360,
+            'positive interior stationary time on the VALID two-exterior-coordinate edge graph')
+    face_gap=F(u[0])+1280*clamp_time
+    require(face_gap==(F(4681,12) if miss else F(390)) and face_gap>360 and
+            -4096<u[1]-3072<0 and u[0]>0,'after Y-clamp: valid east face strictly clear and gap increases to endpoint')
+    if miss:
+        require(bb*bb-4*aa*cc==-262144*9361 and
+                time==((F(243,21632),F(655,43264))[a]) and
+                closest==(F(56172,169),F(23405,169)) and minimum2==F(4681,13)**2 and
+                minimum2-360*360==F(9361,169) and 360<F(4681,13)<361,
+                'strictly positive full-feature quadratic and true curved interior World minimum4681/13')
+    else:
+        factor=(32,45)[a]
+        require((aa,bb,cc)==(3328*3328,-2*3328*factor,factor*factor) and
+                bb*bb-4*aa*cc==0 and time==((F(1,104),F(45,3328))[a]) and
+                closest==(F(4320,13),F(1800,13)) and minimum2==360*360,
+                'genuine later double-root graze, BOTH exterior coordinates, derivative0, no penetration')
+    summary=identity_proof['fixtures'][4]
+    require(fixture['side']==64 and fixture['revision']==1 and fixture['entities']==0 and
+            len(fixture['cells'])==4096 and summary['cell0']==[0,0,0,0] and
+            summary['lowest_floor']==-2 and summary['highest_ceiling']==16,
+            'original fixed F4 construction and existing ONE-decode summary')
+    cell=((19,19),(16,19),(16,16),(19,16))[r]
+    signs=((1,1),(-1,1),(-1,-1),(1,-1))[r]
+    require(fixture['cells'][64*cell[1]+cell[0]]==(0,0,0,0) and
+            identity==3*(64*cell[1]+cell[0]) and
+            corner==tuple(1024*(cell[j]+int(signs[j]>0)) for j in (0,1)),
+            'original unique solid corner-cell identity and actual exposed corner')
+    source_cell=(eye[0]//1024,eye[1]//1024)
+    require(fixture['cells'][64*source_cell[1]+source_cell[0]]==(4,0,16,0),
+            'actual ordinary floor underneath source attains the initial361 lower bound')
+    for x,y,wanted in ((0,0,(0,0,0,0)),(63,63,(0,0,0,0)),
+                       (32,8,(4,1,6,0)),(8,32,(4,-2,4,0))):
+        require(fixture['cells'][64*y+x]==wanted,'named original ring/raised/lowered source premise')
+    end=tuple(eye[j]+delta[j] for j in range(3));ideal=end
+    lo=tuple(min(eye[j],end[j]) for j in range(3));hi=tuple(max(eye[j],end[j]) for j in range(3))
+    require(all(12992<=lo[j]<=hi[j]<=23872 for j in (0,1)) and
+            (lo[2],hi[2])==(361,5989),'complete unchanged paths in conservative common box')
+    require(min(lo[0]-1024,lo[1]-1024,64512-hi[0],64512-hi[1])>=11968 and
+            32768-hi[0]>=8896 and 32768-hi[1]>=8896 and 16384-hi[2]>=10395 and
+            lo[2]+131072>360 and 131072-hi[2]>360,
+            'FULL F4 ring/raised/lowered/ordinary ceiling/true outside exclusion, not whole-map rotation')
+    require(delta[2]>0 and lo[2]==361 and -131072<lo[2]<=hi[2]<131072,
+            'ordinary floors separate from361; solid Z caps never activate')
+    # The original solid block[16384,20480]^2 is a union of the16 fixed cells.
+    # Its corner-then-face distance above exhausts that union. At the graze
+    # only the named corner cell contains K; each other cell is>=1024 inward
+    # on an active axis. No second physical contact can enter first/priority.
+    counts=[]
+    for j in (0,1):
+        low=max(0,(lo[j]-360)//1024-int((lo[j]-360)%1024==0));high=min(63,(hi[j]+360)//1024)
+        counts.append(high-low+1)
+    require(counts[0]*counts[1]<=15 and 2*15*7+6==216,
+            'conservative15 cells/pass,30boxes,216intervals/432roots; original caps unchanged, not measured work')
+    first,priority=cert.get('first'),cert.get('priority')
+    require(type(first) is dict and first==priority and first.get('actor')==(65535,0,0) and
+            first.get('zone')==first.get('origin')==0,'coherent actual first AND anchored priority/NullA/None fields')
+    if miss:
+        q=Q;qs=Q;camera=ideal
+        require(first.get('status')==first.get('kind')==first.get('id')==0 and
+                first.get('q')==Q and first.get('distance')==6538 and first.get('point')==ideal and
+                first.get('normal')==(0,0,0) and 'root' not in cert,
+                'complete canonical Clear pair; never Clear.id0 as World0')
+    else:
+        q=(41297762,58074978)[a];qs=(19619279,36396495)[a]
+        require(time*Q-q==F(6,13) and q-k==qs>0,'own exact floor-Q32 and nonclamped backoff')
+        root=cert.get('root')
+        require(type(root) is dict and F(*root['lo'])==F(*root['hi'])==time and
+                tuple(root['poly'])==oracle.primitive((-time,1)) and root['q']==q,
+                'actual own rational double-root time/bin retained by independent full sweep')
+        require(cert.get('feature_axes')==[0,1] and cert.get('feature_signs')==list(signs) and
+                cert.get('feature')==(9,7,6,8)[r],'true strict exterior XY edge feature, not face at rounded point')
+        raw=tuple(eye[j]*Q+delta[j]*q-corner[j]*Q for j in (0,1))+(0,)
+        normal2=sum(d*d for d in raw);norm=math.isqrt(normal2);norm+=norm*norm<normal2
+        require(normal2==(360*Q)**2+1536*1536 and norm==1546188226561 and
+                tuple(oracle.truncate(F(d*scale,norm)) for d in raw)==own_normal,
+                'OWN reported-q raw/ceil-norm unit witness, not copied exact-root normal')
+        point=tuple(oracle.nearest(F((eye[j]*Q+delta[j]*q)*scale-360*own_normal[j]*Q,Q*scale)) for j in range(3))
+        distance=math.isqrt(length2*q*q)//Q
+        require(first.get('status')==first.get('kind')==1 and first.get('id')==identity and
+                first.get('q')==q and first.get('normal')==own_normal and
+                first.get('point')==point==(*corner,(415,437)[a]) and
+                first.get('distance')==distance==(62,88)[a],
+                'unique physical graze and complete own ID/q/normal/point/travel witness')
+        camera=tuple(eye[j]+oracle.nearest(F(delta[j]*qs,Q)) for j in range(3))
+        require(camera==(*camera_xy,(387,409)[a]),'whole signed displacement rounding for BOTH distinct phases')
+    require((cert.get('q'),cert.get('qs'),cert.get('clamped'))==(q,qs,False) and
+            tuple(cert.get('camera',()))==camera and tuple(cert.get('ideal',()))==ideal,
+            'actual independent full camera result, not a constructor output substitute')
+    muzzle=tuple(eye[j]+muzzle_offset[j] for j in range(3))
+    require(oracle.offset(eye,forward,right,(666,358,-512))==muzzle and muzzle[2]==-728,
+            'original Eye-based one-full-sum Pistol muzzle; no valid shot source inferred')
+    require(response[10:82]==struct.pack('<18i',*eye,*ideal,*camera,*muzzle,*forward,*right) and
+            response[82:134]==oracle.encode_hit(first) and
+            response[134:147]==bytes(0x80+3*p+j for j in range(13)) and
+            response[147:160]==bytes(0xa0+3*p+j for j in range(13)),
+            'all logical solution/witness fields and original poison guards in complete independent response')
+    capsule_axis=(row['foot'][2]+1126,row['foot'][2]+row['height']-1126)
+    require(capsule_axis==(-1687,-201) and -131072<capsule_axis[0]<capsule_axis[1]<0 and
+            row['foot'][2]+row['height']==925 and row['height']-row['eye']==564 and
+            -131072<=row['foot'][2] and row['foot'][2]+row['height']<=131072 and
+            all(0<=eye[j]<=262144 for j in (0,1)) and -8000<=row['aim'][1]<=8000 and
+            cert.get('physical358_safe') is True and (miss or cert.get('projected_margin_ge31') is True),
+            'scalar legal but living capsule overlaps floor; physical358/projected31 distinct from normal31')
+    cert['graze_miss_coverage']={'source_adoption':'D345/D355','kind':'miss' if miss else 'graze',
+      'orientation':r,'phase':a,'poison':p,'whole_World_initial_distance':361,
+      'target_initial_distance_squared':target_initial,'edge_polynomial_constant_linear_quadratic':[cc,bb,aa],
+      'interior_time':[time.numerator,time.denominator],
+      'whole_World_minimum_distance':[4681,13] if miss else [360,1],
+      'clamp_time':[clamp_time.numerator,clamp_time.denominator],
+      'BODY_FALSE_SCALAR_VALID_ONLY':True,'runtime_source_authority':'NOT_PROVED',
+      'fixed_geometry_premise':'ORIGINAL_F4_SOURCE_CONSTRUCTION_ONE_DECODE_SIX_NAMED_CELLS',
+      'conservative_cells_per_pass':15,'proof_method':'EXISTING_COMPLETE_RESULT_FIXED_BLOCK_CLAMP_REGION_EXCLUSIONS_NO_SECOND_SWEEP'}
+    return True
+
 def semantic_certificate(row,predicate,response,cert,oracle,angles,bindings,identity_proof,fixtures_):
     """Every requested semantic key must be proved or explicitly returned.
 
@@ -1701,6 +1877,8 @@
         checks['d334_initial_tangent']=initial_tangent_certificate(row,response,cert,oracle,angles,fixtures_[1],identity_proof)
     if 'd343_negative_half' in predicate:
         checks['d343_negative_half']=negative_half_certificate(row,response,cert,oracle,angles,fixtures_[1],identity_proof)
+    if 'd355_graze_miss' in predicate:
+        checks['d355_graze_miss']=graze_miss_certificate(row,response,cert,oracle,angles,fixtures_[4],identity_proof)
     annotations={'pair','relation','member'}
     for key,value in predicate.items():
         if key in annotations:continue
@@ -1794,6 +1972,31 @@
         a,b=dict(decoded[j]),dict(decoded[j+1]);a.pop('id');b.pop('id')
         need(a.pop('poison')==0 and b.pop('poison')==1 and a==b,'both full poisons per refusal seed')
         need(expected[160*j+1]==expected[160*(j+1)+1]==0 and expected[160*j+2:160*j+10]==expected[160*(j+1)+2:160*(j+1)+10],'same exact refusal tuple under both poisons')
+    for base,kind in ((1392,'graze'),(1408,'miss')):
+        poses=set()
+        for j in range(base,base+16):
+            r,a,p=(j-base)//4,((j-base)//2)%2,(j-base)%2
+            literal=GRAZE_MISS_LITERALS[r];xy=literal[5 if kind=='miss' else 4][a]
+            row=decoded[j];coverage=catalog[j]['certificate'].get('graze_miss_coverage',{})
+            need(row['fixture']==4 and row['weapon']==1 and row['aim']==(literal[0],-6000) and
+                 row['foot']==(*xy,-2813) and (row['height'],row['eye'],row['poison'])==(3738,3174,p) and
+                 row['view_flags']==0 and row['revision']==1 and row['actor_count']==row['box_count']==0 and
+                 row['rule_slot']==65535 and row['rule_value']==row['table_kind']==row['table_index']==row['table_value']==0,
+                 'actual serialized D355 cardinal/phase/poison/rig/body/default association')
+            need(catalog[j]['proved_predicates'].get('d355_graze_miss') is True and
+                 (coverage.get('kind'),coverage.get('orientation'),coverage.get('phase'),coverage.get('poison'))==(kind,r,a,p) and
+                 coverage.get('whole_World_initial_distance')==361 and
+                 coverage.get('target_initial_distance_squared')==((131053,132194) if kind=='miss' else (130624,131625))[a] and
+                 coverage.get('whole_World_minimum_distance')==([4681,13] if kind=='miss' else [360,1]) and
+                 catalog[j]['certificate']['body_feasible'] is False and expected[160*j:160*j+2]==bytes((1,1)),
+                 'all16 exact own graze/miss certificates; World361 and target distances kept separate')
+            poses.add((row['aim'],row['foot']))
+        need(len(poses)==8,'eight distinct actual poses per graze/miss stratum')
+        for j in range(base,base+16,2):
+            left,right=dict(decoded[j]),dict(decoded[j+1]);left.pop('id');right.pop('id')
+            need(left.pop('poison')==0 and right.pop('poison')==1 and left==right and
+                 expected[160*j+2:160*j+134]==expected[160*(j+1)+2:160*(j+1)+134],
+                 'both original full poisons per physical graze/miss, same complete success fields/Fault')
     for j in range(1424,1440):need(catalog[j]['proved_predicates'].get('d287') is True,'all16 exact D287 rows')
     for j in range(1456,1472):need(catalog[j]['proved_predicates'].get('d321_q_k_plus_one') is True and decoded[j]['poison']==(j-1456)%2,'all16 exact D321 q=k+1 rows and both poisons')
     for j in range(1344,1360):
@@ -2300,8 +2503,14 @@
             row['aim']=(YAWS[j],-8000);row['fixture']=1;row['foot']=(32768,32768,360-row['eye']);predicate={'clear':True,'body_feasible':False}
         elif stratum==6:
             row['aim']=(YAWS[j],8000);near_plane(row,oracle,angles,1);predicate={'hit':True,'clamped':True}
-        elif stratum in (7,8,13,14):
-            name={7:'later graze from distance361',8:'miss from distance361',13:'same-Q32 competing roots',14:'initial nonclosing skip followed by other primitive Hit'}[stratum]
+        elif stratum in (7,8):
+            orientation,phase=divmod(j,2);literal=GRAZE_MISS_LITERALS[orientation]
+            x,y=literal[5 if stratum==8 else 4][phase]
+            row.update(fixture=4,weapon=1,height=3738,eye=3174,aim=(literal[0],-6000),foot=(x,y,-2813))
+            return row,{'clear' if stratum==8 else 'hit':True,'clamped':False,'body_feasible':False,
+                        'initial_eye_clearance':361,'d355_graze_miss':True}
+        elif stratum in (13,14):
+            name={13:'same-Q32 competing roots',14:'initial nonclosing skip followed by other primitive Hit'}[stratum]
             raise oracle.ConstructionRequired(case_id,name,'literal independently certified fixed-rig/full-fixture variant required')
         elif stratum==10:
             row['aim']=(YAWS[j],8000);near_plane(row,oracle,angles,1);predicate={'clamped':True}
--- a/tests/outbreak/camera/release-1/SCHEMA.md
+++ b/tests/outbreak/camera/release-1/SCHEMA.md
@@ -1,6 +1,6 @@
 # Camera proof harness schema — source proposal 1
 
-T1901.4 / D305/D321/D325/D334/D343 / CAMERA_FOUNDATION0.8. **NOT GENERATED, NOT COMPILED,
+T1901.5 / D305/D321/D325/D334/D343/D345/D355 / CAMERA_FOUNDATION0.9. **NOT GENERATED, NOT COMPILED,
 NOT EXECUTED, NOT ACCEPTED.** This file specifies future private harness bytes;
 it adds no production wire format, API, geometry hook or runtime caller.
 Corrected T182 sections4–8 and D287 govern. A later MAIN release must bind real
@@ -523,3 +523,91 @@
 D32116,D325112,D33416 mappings/routines,all other rows,seams,4096/64/94 and
 every original byte/time/work/frame/source/caller/real-G2/current-G1 gate remain.
 No generator,oracle,parser,control,compiler,target or runtime was executed.
+
+## D345/D355 exact later-graze and curved interior full-miss rows
+
+Only existing graze1392..1407 and miss1408..1423 change. Each uses
+`base+4*r+2*a+p`,r0..3 cardinal orientations,a0/1 genuinely different
+phases,p0/1 original full poisons. All retain F4/Pistol/Crouch3738/3174,
+pitch−6000,EyeZ361,footZ−2813,gap564,revision1,actors0/boxes0,
+canonical unpatched rules/table and original other defaults.
+
+|r/yaw|D|Graze EyeXY phase0 / phase1|Miss EyeXY phase0 / phase1|Graze first AND priority ID|
+| --- | --- | --- | --- | ---: |
+|0/0|(1280,−3072,5628)|(20800,20648)/(20795,20660)|(20798,20653)/(20793,20665)|3705|
+|1/16384|(3072,1280,5628)|(16216,20800)/(16204,20795)|(16211,20798)/(16199,20793)|3696|
+|2/32768|(−1280,3072,5628)|(16064,16216)/(16069,16204)|(16066,16211)/(16071,16199)|3120|
+|3/49152|(−3072,−1280,5628)|(20648,16064)/(20660,16069)|(20653,16066)/(20665,16071)|3129|
+
+D345 resolves initial361 as the TRUE minimum over the complete participating
+World,furnished by ordinary floor0 at the source. That floor separates upward.
+The future target's distinct initial squared distances stay explicit:
+graze130624/131625,miss131053/132194,all>361². They are never relabeled361.
+
+Accepted basis at yaw0 is F(0,536870911,−929887696),R(1073741824,0,0),
+from raw norm ceilS+1;the other bases are exact signed quarter rotations.
+One complete signed FRU sum gives the stated original rig,L06538,k21678483.
+The local transverse velocity is(1280,−3072),not the full boom norm.
+
+For graze,local original NE-corner offsets are(320,168)/(315,180).
+The excess polynomials are respectively(3328*t−32)² and(3328*t−45)²:
+true positive double roots1/104 and45/3328,derivative0,and BOTH exterior
+coordinates(4320/13,1800/13). Actual edge ranks9/7/6/8 retain their own
+original solid IDs3705/3696/3120/3129. After the minor clamp,the original
+block-union face gap390>360 increases. The complete block touches exactly
+once;every other block cell is farther,so first AND priority are that one ID.
+
+Own q41297762/58074978 each has fractional residual6/13;qs19619279/36396495,
+clampedfalse. Own reported-q raw normal numerators1427250670080/594687780864
+have squared norm(360Q)²+1536²,ceil norm1546188226561.
+Truncated own normal is the signed rotation of(991146298,412977625,0),
+not a copied exact-root normal. Own point is the actual cornerXY/Z415 or437,
+distance62/88,World/NullA/zoneNone/originNone. Backed-off cameraXY by r is
+(20806,20634),(16230,20806),(16058,16230),(20634,16058),Z387/409.
+Both phases share that XY but retain different source poses/Z/results.
+
+For miss,local offsets(318,173)/(313,185) give nonconstant quadratics
+(A,B,C)=(11075584,−248832,1453)/(11075584,−335360,2594).
+Both discriminants are−262144*9361. Their valid interior minima at243/21632
+or655/43264 attain(56172/169,23405/169),distance4681/13=360+1/13<361.
+Squared excess9361/169 is strictly positive. After the minor clamp,the gap
+4681/12>360 increases. This is a genuine curved approach/retreat FULL miss,
+not a parallel constant361 label. Complete first/priority are canonical
+Clear/kindNone/id0/NullA/qQ/distance6538/pointIdeal/normal0/zoneNone/originNone;
+camera=Ideal. Clear.id0 is not a World0 Hit.
+
+`graze_miss_certificate` binds all of this to the actual complete oracle result.
+Its complete F4 premise is the UNCHANGED original `fixtures()` construction:
+outer ring,solid[16,20)²,raised1/6 patch[32,40)×[8,16),lowered−2/4 patch
+[8,16)×[32,40),ordinary0/16 elsewhere. Six bounded reads from the EXISTING
+decoded cells check original corner/source-floor/two ring/two patch records.
+They supplement that fixed source premise,not replace it with a local-map claim.
+The full path box[12992,23872]²/Z[361,5989] leaves11968 to the ring,
+8896 to each differently placed patch,10395 to ordinary ceilings,and strict
+outside-plane clearance. Ordinary floors separate from361;the block's
+corner-then-face proof exhausts its union. No hidden first/priority contact
+remains;for miss,the actual whole-World minimum is4681/13.
+
+A bounded two-axis enclosure proves at most15cells/pass,30floor/ceiling boxes,
+216generic intervals/432roots,within all ORIGINAL caps. These are mathematical
+bounds,not measured work/frame/performance. There is no second fixture decode,
+sweep,root enumeration,constructor or output producer.
+
+All32 are BODY_FALSE/SCALAR_VALID_ONLY:foot−2813/top925 are scalar-valid,but
+living centerline[−1687,−201] strictly overlaps ordinary floor0. Runtime source
+authority stays NOT_PROVED. Physical358 safety and nonclamped projected margin
+are checked independently;no normal31 claim follows from a tangent.
+Logical Pistol muzzle remains Eye-based,with rotated offset(358,333,−1089),
+Z−728. Full Eye/Ideal/Camera/Muzzle/F/R/own hit/Fault/poison guards are checked
+against the ONE existing independent160-byte observation,whose all160 bytes
+remain the expected target comparison. No fabricated constructor output.
+Decoded coverage binds all original32 serialized requests/defaults/stances/
+phases/poisons to these certificates,eight distinct poses per stratum.
+
+Adopted mathematics: T206 proposala6e570646fdcf1fe1be8c7b64aacbe72269b9c0c07da28b5e2ea8455e258d4ed;
+independent reviewb02d8cc354d585c14670547edc15424054ec026e09bcd70bfcf7d6367eae53f2;
+D345 interpretation and D355 narrow source lease. Old notes remain immutable.
+D321/D325/D334/D343 mappings/routines/coverage,4096/64/94 and every cap remain.
+Unadopted T210 strata13/14 retain their ConstructionRequired gates.
+No parser/import/helper/oracle/control/generator/preparation/compiler/query/
+FFI/runtime/output root or target/corpus/frame/realG2/currentG1 acceptance.
--- a/tests/outbreak/camera/release-1/README.md
+++ b/tests/outbreak/camera/release-1/README.md
@@ -1,6 +1,6 @@
 # T190 camera harness — source review package
 
-**T1901.4 / D343 narrow negative-half source correction. SOURCE ONLY. NOT COMPILED /
+**T1901.5 / D355 narrow later-graze/curved-miss source correction. SOURCE ONLY. NOT COMPILED /
 NOT EXECUTED / NOT ACCEPTED.** No setup, request,
 golden, control result, preparation, attempt or final evidence has been
 generated by this package. D305 authorizes only these six new files and the
@@ -22,9 +22,10 @@
 Read corrected [T182](../../../../notes/proposals/T182-camera-implementation-release-packet-1.md)
 sections4–8, [T190](../../../../tickets/T190.md),
 [D305](../../../../notes/decisions/D305-camera-proof-harness-source-release.md),
-and [CAMERA_FOUNDATION0.8](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
+and [CAMERA_FOUNDATION0.9](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
 sixteen existing q=k+1 literals; D325 supplies112 identity/face rows; D334 supplies
-sixteen initial-tangent/later-Hit rows; D343 supplies32 negative-half rows below. The adjacent
+sixteen initial-tangent/later-Hit rows; D343 supplies32 negative-half rows;
+D345/D355 supply32 later-graze/curved-miss rows below. The adjacent
 SCHEMA is private test framing, not a new gameplay interface. No code here
 implements MotionState, observer selection, authority or a usable game camera.
 
@@ -40,9 +41,10 @@
 
 The catalog is **not proved realizable**. Source `ConstructionRequired` gates
 remain for exact edge/corner tangency, shallow-face variants, near-Q32 bins,
-competing first/priority and same-bin roots, later graze/miss and other initial strata.
+competing first/priority and same-bin roots, and other initial strata.
 D325 resolves the fixed-map identity interpretation and112 inputs; D334 resolves
-the exact16 initial-tangent/later-Hit rows; D343 resolves only32 negative-half rows below.
+the exact16 initial-tangent/later-Hit rows; D343 resolves32 negative-half rows;
+D355 resolves only32 reviewed later-graze/curved-miss rows below.
 Other literal candidates,including normal
 margin counterexamples, are also subject to exact feature/body/first/root
 checks; existence of a formula is not a passing certificate. Failed semantic
@@ -338,3 +340,51 @@
 realG2/currentG1,frame/caller/browser/gameplay/human gates are still pending.
 No source/parser/oracle/generator/control/compiler/query/runtime was executed;
 no output roots or automatic follow-on stage are authorized.
+
+## D345/D355: later true graze and curved interior full miss
+
+[D355](../../../../notes/decisions/D355-camera-graze-miss-source-release.md)
+releases only the32 existing1392..1423 rows from
+[T206's proposal](../../../../notes/proposals/T206-later-graze-miss-construction-1.md),
+after [independent review](../../../../notes/reviews/T206-graze-miss-review-1.md)
+and [D345's measurement decision](../../../../notes/decisions/D345-camera-initial-distance-measurement.md).
+Initial361 is the complete-World minimum furnished by the separating ordinary
+floor. The future edge's larger initial squared distances130624/131625 for
+graze,131053/132194 for miss,remain separately explicit.
+
+The fixed F4/Pistol/Crouch/pitch−6000/EyeZ361 cases use four cardinal rotations,
+two genuinely distinct phases and both original poisons. Original full-sum rig
+is rotation(1280,−3072,5628),L6538,k21678483. Graze has an actual positive
+double-root XY edge tangency at1/104 or45/3328,unique first=priority original
+solid ID3705/3696/3120/3129. Miss has a strictly positive nonconstant quadratic,
+valid interior minimum4681/13 and increasing clear face continuation.
+The full miss publishes the complete canonical Clear pair,not just no root on
+one chosen polynomial.
+
+The bounded certificate checks exact rows/basis/rig,whole-World and target
+initial distances,polynomial/discriminant/derivative/active intervals,
+corner-then-face continuation,complete unchanged F4 exclusions,
+own first/priority/features/root/bin/reported-q normal/point/distance,
+signed camera rounding,Eye-based muzzle,all logical fields/guards and safety.
+The original fixed F4 source construction and six named existing decoded cells
+support the proof. Ring/raised/lowered/ordinary-floor/ceiling/outside regions
+are all excluded explicitly;whole-map symmetry is never assumed.
+A conservative15cells/pass enclosure stays inside original bounds and claims
+no measured work. One fixture decode/one complete oracle result per row remain.
+
+Every source body is BODY_FALSE/SCALAR_VALID_ONLY:foot−2813/top925 are
+numerically valid,but the living capsule overlaps floor0. Runtime source
+authority remains NOT_PROVED. Radius358 safety and original projected31 margin
+do not imply normal31 retreat at tangency or valid observer/shot eligibility.
+All160 output bytes remain independently produced by the existing oracle and
+fully compared against future real targets. Decoded coverage verifies every
+actual32 request,including eight distinct poses and both poisons per stratum.
+
+Only these32 formerly gated rows and their supplementary checks/docs change.
+D321/D325/D334/D343 mappings/routines/coverage,64controls,94children and every
+cap remain. T210 notes are unadopted;strata13/14 retain their existing gates.
+All old T206/T210 notes and source evidence remain immutable.
+No parser/import/helper/oracle/control/generator/preparation/compiler/query/
+FFI/runtime or output-root effect occurred. Complete catalog/source/target/
+realG2/currentG1/frame/caller/gameplay/browser/human gates remain pending.
+Stable source/diff/handoff requires MAIN review;no automatic next stage.
```
