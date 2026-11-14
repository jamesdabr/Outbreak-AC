# T1901.6 / D359 focused three-source diff

Complete source-text comparison against captured T1901.5. No parser, import, helper or project execution.

```diff
--- a/tests/outbreak/camera/release-1/verify.py
+++ b/tests/outbreak/camera/release-1/verify.py
@@ -1086,6 +1086,17 @@
  (16384,(3072,1280,5628),(16384,20480),3696,((16216,20800),(16204,20795)),((16211,20798),(16199,20793)),(16230,20806)),
  (32768,(-1280,3072,5628),(16384,16384),3120,((16064,16216),(16069,16204)),((16066,16211),(16071,16199)),(16058,16230)),
  (49152,(-3072,-1280,5628),(20480,16384),3129,((20648,16064),(20660,16069)),((20653,16066),(20665,16071)),(20634,16058)))
+# D357/D359 exact1488+2*j+p: yaw,EyeXY,D,earlier face ID,later edge ID.
+# Both physical roots are distinct; q equality never replaces their ordering.
+SAME_BIN_LITERALS=(
+ (0,(33280,32828),(1280,-1067,-5744),6049,6241),
+ (0,(34304,32828),(1280,-1067,-5744),6052,6244),
+ (16384,(32708,33280),(1067,1280,-5744),6241,6238),
+ (16384,(32708,34304),(1067,1280,-5744),6433,6430),
+ (32768,(32256,32708),(-1280,1067,-5744),6238,6046),
+ (32768,(31232,32708),(-1280,1067,-5744),6235,6043),
+ (49152,(32828,32256),(-1067,-1280,-5744),6046,6049),
+ (49152,(32828,31232),(-1067,-1280,-5744),5854,5857))
 FAMILY_RANGES=((0,512,'free'),(512,1280,'blocker'),(1280,1536,'initial'),
  (1536,1792,'recovery'),(1792,2304,'stance'),(2304,2560,'exclusion'),
  (2560,2816,'rounding'),(2816,3072,'none'),(3072,3584,'refusal'),(3584,4096,'metamorphic'))
@@ -1832,6 +1843,223 @@
       'conservative_cells_per_pass':15,'proof_method':'EXISTING_COMPLETE_RESULT_FIXED_BLOCK_CLAMP_REGION_EXCLUSIONS_NO_SECOND_SWEEP'}
     return True
 
+def remaining_contact_certificate(row,response,cert,oracle,angles,fixture,identity_proof):
+    """D359 supplement to the ONE existing complete independent F1 result.
+
+    Fixed polynomials/intervals and named decoded cells only. No second
+    decode, sweep, Root construction, root enumeration or response producer.
+    D334's old routine/mappings are unchanged; its reviewed literals are
+    explicitly translated here for the separately allocated initial-skip rows.
+    """
+    def require(condition,detail):
+        if not condition:raise oracle.ConstructionRequired(row['id'],'D359 remaining contacts',detail)
+    require(1488<=row['id']<1520,'exact existing32-row range')
+    translated=row['id']>=1504;base=1504 if translated else 1488
+    j,p=divmod(row['id']-base,2);scale=1<<30
+    require(row['fixture']==1 and row['weapon']==1 and row['height']==3738 and row['eye']==3174 and
+            row['poison']==p and row['flags']==0 and row['revision']==1 and row['count']==row['boxes']==0 and
+            row['slot']==65535 and row['rule_value']==0 and
+            row['table_kind']==row['table_index']==row['table_value']==0,'original F1/Crouch/Pistol/poison/unpatched defaults')
+    require(response[:2]==bytes((1,1)) and response[2:10]==bytes(8) and
+            cert.get('physical_query') is True and cert.get('body_feasible') is False,
+            'complete independent successful result; BODY_FALSE/SCALAR_VALID_ONLY')
+    summary=identity_proof['fixtures'][1]
+    require(fixture['side']==64 and fixture['revision']==1 and fixture['entities']==0 and
+            len(fixture['cells'])==4096 and summary['cell0']==[4,0,16,0] and
+            summary['lowest_floor']==0 and summary['highest_ceiling']==16,
+            'original uniform F1 SOURCE construction and existing one-decode summary')
+    if not translated:
+        r,a=divmod(j,2);yaw,xy,delta,face_id,edge_id=SAME_BIN_LITERALS[j]
+        eye=(*xy,683)
+        require(row['aim']==(yaw,8000) and row['foot']==(*xy,-2491),'exact eight same-bin poses/four aims/two tile placements')
+        require((angles[0],angles[16384],angles[16385+1000],angles[16385+8000])==
+                (0,scale,186453311,1057429273),'named certified cardinal pitch8000 DATA')
+        forward,right=(0,186453311,1057429273),(scale,0,0)
+        eye_offset=(512+1024*a,60);rig_delta=(1280,-1067,-5744)
+        camera_offset=(65,-54,-291);muzzle_offset=(358,116,144)
+        face_cell,edge_cell=(32+a,31),(32+a,32)
+        point_offset=(584+1024*a,0);edge_raw=(0,-747419,1546188228240)
+        edge_normal=(0,-519,scale-1)
+        for _ in range(r):
+            forward=(-forward[1],forward[0],forward[2]);right=(-right[1],right[0],right[2])
+            eye_offset=(-eye_offset[1],eye_offset[0]);rig_delta=(-rig_delta[1],rig_delta[0],rig_delta[2])
+            camera_offset=(-camera_offset[1],camera_offset[0],camera_offset[2])
+            muzzle_offset=(-muzzle_offset[1],muzzle_offset[0],muzzle_offset[2])
+            face_cell=(63-face_cell[1],face_cell[0]);edge_cell=(63-edge_cell[1],edge_cell[0])
+            point_offset=(-point_offset[1],point_offset[0])
+            edge_raw=(-edge_raw[1],edge_raw[0],edge_raw[2]);edge_normal=(-edge_normal[1],edge_normal[0],edge_normal[2])
+        require(eye[:2]==(32768+eye_offset[0],32768+eye_offset[1]) and delta==rig_delta and
+                (face_id,edge_id)==(3*(64*face_cell[1]+face_cell[0])+1,3*(64*edge_cell[1]+edge_cell[0])+1) and
+                face_id!=edge_id,'actual cardinal rotation and two ORIGINAL distinct floor identities')
+        for x,y in (face_cell,edge_cell):
+            require(fixture['cells'][64*y+x]==(4,0,16,0),'two named already-decoded uniform floor cells')
+        time=F(323,5744);upper=time+F(1,16*Q);q=241517137
+        poly=(340489,-7974344,34132025);cc,bb,aa=poly;disc=bb*bb-4*aa*cc
+        require((aa,bb,cc)==(1067*1067+5744*5744,-2*(60*1067+683*5744),60*60+683*683-360*360) and
+                disc==17103845989436 and 4135679**2<disc<4135680**2 and
+                1067*323==60*5744+1,'actual nonsquare edge polynomial, distinct from full boom squared35770425')
+        require(oracle.evaluate(poly,time)==F(1,5744**2)>0 and oracle.evaluate(poly,upper)<0 and
+                2*aa*upper+bb<0 and 0<F(60,1067)<time<upper<1,
+                'unique ENTERING algebraic edge root tau in(t0,t0+1/(16Q)), STRICTLY later than rational face')
+        require(Q*323==5744*q+1680 and F(q,Q)<time<upper<F(q+1,Q) and
+                F(105,359)+F(1,16)==F(2039,5744)<1,'two distinct physical roots in exactly the same floor-Q32 bin')
+        face_center=tuple(F(eye[k])+delta[k]*time for k in range(3))
+        require(all(face_cell[k]*1024<face_center[k]<(face_cell[k]+1)*1024 for k in (0,1)) and
+                face_center[2]==360,'strict physical face interior at t0, not a closed-edge/equal-root alias')
+        edge_axis=0 if r%2 else 1;inside_axis=1-edge_axis;edge_sign=(-1,1,1,-1)[r]
+        edge_bound=1024*(edge_cell[edge_axis]+int(edge_sign>0))
+        for endpoint in (time,upper):
+            center=tuple(F(eye[k])+delta[k]*endpoint for k in range(3))
+            require(edge_sign*(center[edge_axis]-edge_bound)>0 and center[2]>0 and
+                    edge_cell[inside_axis]*1024<center[inside_axis]<(edge_cell[inside_axis]+1)*1024,
+                    'BOTH strict exterior edge axes over whole isolating interval; feature at physical tau')
+        edge_feature=6+4*(1 if edge_axis==0 else 2)+2*int(edge_sign>0)+1
+        require(edge_feature==(15,13,17,11)[r],'derived physical XY/Z edge rank from strict axes/signs')
+        length2=sum(d*d for d in delta);length=math.isqrt(length2);k=(33*Q+length-1)//length;qs=q-k
+        require((length2,length,k,qs)==(35770425,5980,23701325,217815812) and
+                cert.get('initial_distance_squared')==683*683,'full rig norm/backoff and initial clear floor minimum683')
+        horizon=time+F(11,length)+F(1,Q)
+        require(horizon<F(3,50) and 1024-(512+1280*F(3,50))==F(2176,5)>360 and
+                min(1024+60-1067*F(3,50),1024-60)==964>360,
+                'full anchored11 window<0.06: only the named two floor cells can contact, no priority chaining')
+        end=tuple(eye[k]+delta[k] for k in range(3))
+        lo=tuple(min(eye[k],end[k]) for k in range(3));hi=tuple(max(eye[k],end[k]) for k in range(3))
+        outside_xy=min(lo[0],lo[1],65536-hi[0],65536-hi[1])
+        require(outside_xy==(29952 if a else 30976) and outside_xy>=29952 and outside_xy-360>=29592 and
+                (lo[2],hi[2])==(-5061,683) and 16384-hi[2]==15701 and
+                lo[2]+131072>360 and 131072-hi[2]>360,
+                'D357 CORRECT full-segment exterior bound29952/residual29592, all F1 ceiling/outside exclusions')
+        center_q=tuple(eye[k]*Q+delta[k]*q for k in range(3))
+        edge_lo=(1024*edge_cell[0],1024*edge_cell[1],-131072)
+        edge_hi=(1024*(edge_cell[0]+1),1024*(edge_cell[1]+1),0)
+        own_raw=tuple(center_q[k]-max(edge_lo[k]*Q,min(center_q[k],edge_hi[k]*Q)) for k in range(3))
+        require(own_raw==edge_raw,'OWN actual reported-q center-to-original-edge closest vector')
+        norm2=sum(d*d for d in own_raw);norm=math.isqrt(norm2);norm+=norm*norm<norm2
+        require(edge_raw[2]==360*Q+1680 and 0<747419**2<2*edge_raw[2]+1 and
+                norm==1546188228241 and tuple(oracle.truncate(F(d*scale,norm)) for d in edge_raw)==edge_normal,
+                'later edge OWN reported-q raw/ceil-norm normal, never copied face normal')
+        point=(32768+point_offset[0],32768+point_offset[1],0)
+        normals=((0,0,scale),edge_normal);own_points=[]
+        for normal in normals:
+            own_points.append(tuple(oracle.nearest(F((eye[k]*Q+delta[k]*q)*scale-360*normal[k]*Q,Q*scale)) for k in range(3)))
+        distance=math.isqrt(length2*q*q)//Q
+        require(own_points==[point,point] and distance==336,'each own witness: equal rounded points/q/distance do not identify roots/normals')
+        face_hit={'status':1,'kind':1,'id':face_id,'actor':(65535,0,0),'q':q,'distance':distance,
+                  'point':point,'normal':normals[0],'zone':0,'origin':0}
+        edge_hit={'status':1,'kind':1,'id':edge_id,'actor':(65535,0,0),'q':q,'distance':distance,
+                  'point':point,'normal':edge_normal,'zone':0,'origin':0}
+        priority_hit=edge_hit if edge_id<face_id else face_hit
+        require(cert.get('first')==face_hit and cert.get('priority')==priority_hit and
+                cert.get('feature_axes')==[2] and cert.get('feature_signs')==[1] and cert.get('feature')==5 and
+                (edge_id<face_id)==(j in (2,3,4,5)),
+                'actual earlier coherent face first; later smaller-ID edge priority uses ITS ENTIRE OWN witness in four variants')
+        camera=tuple(eye[k]+camera_offset[k] for k in range(3));muzzle=tuple(eye[k]+muzzle_offset[k] for k in range(3))
+        require(camera[2]==392 and camera[2]-358==34,'actual radius358 floor clearance34, normal32 is not projected31 proof')
+        coverage={'kind':'same-bin','variant':j,'earlier_face_time':[323,5744],
+          'later_edge_polynomial_constant_linear_quadratic':list(poly),'later_edge_branch':-1,'later_edge_discriminant':disc,
+          'later_edge_strict_interval':[[time.numerator,time.denominator],[upper.numerator,upper.denominator]],
+          'strict_distinct_physical_roots':True,'same_q':q,'face_id':face_id,'edge_id':edge_id,
+          'later_edge_feature':edge_feature,'later_edge_feature_axes':[edge_axis,2],
+          'later_edge_feature_signs':[edge_sign,1],'later_edge_own_witness':edge_hit,
+          'nonpublished_competitor_proof':'BOUNDED_MATH_NOT_ADDITIONAL_QUERY_OUTPUT',
+          'first_differs_from_priority':edge_id<face_id,'outside_xy_minimum':outside_xy,
+          'expanded360_outside_xy_residual':outside_xy-360,'conservative_cells_per_pass':9}
+    else:
+        yaw,delta,old_id,old_point,old_camera,old_muzzle=TANGENT_LITERALS[j]
+        shift=(1024,1024,0);identity=old_id+195;eye=(33792,33792,360)
+        point=tuple(old_point[k]+shift[k] for k in range(3));camera=tuple(old_camera[k]+shift[k] for k in range(3))
+        muzzle=tuple(old_muzzle[k]+shift[k] for k in range(3))
+        require(row['aim']==(yaw,286) and yaw==YAWS[j] and row['foot']==(33792,33792,-2814),
+                'eight translated T201 poses; disclosed mathematical reuse, original D334 allocation unchanged')
+        require((angles[8192],angles[16384],angles[16385+286],angles[16385+8714])==
+                (759250125,scale,53575089,1072404408),'named certified cardinal/diagonal pitch286 DATA')
+        forward,right=((0,1072404408,53575089),(scale,0,0)) if j%2==0 else ((-758304429,758304429,53575089),(759250124,759250124,0))
+        for _ in range(j//2):
+            forward=(-forward[1],forward[0],forward[2]);right=(-right[1],right[0],right[2])
+        require(0<307*scale-6144*forward[2]<scale//2 and right[2]==0 and delta[2]==0,
+                'exact zero vertical original rig after ONE full-sum rounding')
+        skipped=[]
+        for x,y in ((32,32),(33,32),(32,33),(33,33)):
+            require(fixture['cells'][64*y+x]==(4,0,16,0),'named translated initial floor')
+            dx=eye[0]-max(1024*x,min(eye[0],1024*(x+1)));dy=eye[1]-max(1024*y,min(eye[1],1024*(y+1)))
+            require(dx*dx+dy*dy+360*360==360*360 and dx*delta[0]+dy*delta[1]+360*delta[2]==0,
+                    'actual initial exact360/nonclosing0; each primitive skips WHOLE, no strict overlap')
+            skipped.append(3*(64*y+x)+1)
+        require(skipped==[6241,6244,6433,6436] and identity not in skipped and
+                cert.get('initial_distance_squared')==360*360,'later NEW identity differs from ALL four whole-primitive skips')
+        major=max(range(2),key=lambda axis:abs(delta[axis]));minor=1-major;v=abs(delta[major])
+        time=F(1024,v);q=(716761165 if j%2==0 else 838681638);remainder=333 if j%2==0 else 358
+        require(time==(F(128,767) if j%2==0 else F(256,1311)) and
+                time.numerator*Q==time.denominator*q+remainder and 1024-v*time==0,
+                'true later double root of adjacent interval(1024-v*t)^2 and exact floor-Q32 remainder')
+        entry_poly=(1024**2,-2048*v,v*v)
+        require(entry_poly[1]**2-4*entry_poly[0]*entry_poly[2]==0 and 2*v*(v*time-1024)==0 and 0<time<1,
+                'actual positive entry double root/derivative0, not omitted constant-face validity')
+        cell=[0,0];cell[major]=34 if delta[major]>0 else 31;cell[minor]=33 if delta[minor]>0 else 32
+        center=tuple(F(eye[k])+delta[k]*time for k in range(3))
+        require(fixture['cells'][64*cell[1]+cell[0]]==(4,0,16,0) and
+                identity==3*(64*cell[1]+cell[0])+1 and identity==(6052,6247,6439,6628,6625,6430,6238,6049)[j] and
+                center[major]==(34816 if delta[major]>0 else 32768) and
+                cell[minor]*1024<center[minor]<(cell[minor]+1)*1024 and center[2]==360,
+                'fifth named cell/NEW ID and exact physical-root canonical +Z face5')
+        length2=sum(d*d for d in delta);length=math.isqrt(length2);k=(33*Q+length-1)//length;qs=q-k
+        require((length2,length,k,qs)==(39288896 if j%2==0 else 39291892,6268,22612304,
+                694148861 if j%2==0 else 816069334),'original full rig/backoff, no changed D334 values')
+        horizon=time+F(11,length)+F(1,Q)
+        require(horizon<F(1,5) and F(abs(delta[major]),5)<2048 and F(abs(delta[minor]),5)<1024,
+                'complete anchored window has only one NEW non-skipped floor identity')
+        end=tuple(eye[k]+delta[k] for k in range(3));lo=tuple(min(eye[k],end[k]) for k in range(3));hi=tuple(max(eye[k],end[k]) for k in range(3))
+        require(all(27656<=lo[k]<=hi[k]<=39928 for k in (0,1)) and
+                min(lo[0],lo[1],65536-hi[0],65536-hi[1])>=25608 and
+                eye[2]+131072>360 and 131072-eye[2]>360 and 16384-eye[2]==16024,
+                'complete translated uniform F1 floor/ceiling/true outside geometry, not assumed infinite-map symmetry')
+        distance=1046 if j%2==0 else 1224
+        literal_hit={'status':1,'kind':1,'id':identity,'actor':(65535,0,0),'q':q,'distance':distance,
+                     'point':point,'normal':(0,0,scale),'zone':0,'origin':0}
+        own_point=tuple(oracle.nearest(F((eye[k]*Q+delta[k]*q)*scale-360*literal_hit['normal'][k]*Q,Q*scale)) for k in range(3))
+        require(cert.get('first')==cert.get('priority')==literal_hit and own_point==point and
+                math.isqrt(length2*q*q)//Q==distance and cert.get('feature_axes')==[2] and
+                cert.get('feature_signs')==[1] and cert.get('feature')==5,
+                'actual later NEW first AND priority with ITS OWN complete root/q/normal/point/travel witness')
+        require(camera[2]==360 and camera[2]-358==2 and cert.get('normal_margin_lt31') is True,
+                'physical358 clearance2; normal setback0 does not replace projected31 certificate')
+        coverage={'kind':'initial-skip','variant':j,'mathematical_reuse':'T201/D334_PLUS_XY_TILE_TRANSLATION',
+          'translation':list(shift),'initial_whole_primitive_skips':skipped,'later_NEW_first_and_priority':identity,
+          'later_entry_polynomial_constant_linear_quadratic':list(entry_poly),'priority_window_upper':[1,5],
+          'conservative_cells_per_pass':35}
+    root=cert.get('root')
+    require(type(root) is dict and F(*root['lo'])==F(*root['hi'])==time and
+            tuple(root['poly'])==oracle.primitive((-time,1)) and root['q']==q,
+            'actual own EARLIEST root certificate, never a substituted priority root')
+    actual_basis=oracle.basis(angles,*row['aim']);ideal=tuple(eye[k]+delta[k] for k in range(3))
+    require(actual_basis==(forward,right) and rig(row,oracle,angles)==delta and
+            tuple(cert.get('eye',()))==eye and tuple(cert.get('delta',()))==delta and tuple(cert.get('ideal',()))==ideal,
+            'actual accepted basis/full-sum rig/eye/ideal from serialized independent resolution')
+    require((cert.get('L0'),cert.get('k'),cert.get('q'),cert.get('qs'),cert.get('clamped'))==(length,k,q,qs,False) and
+            tuple(eye[k]+oracle.nearest(F(delta[k]*qs,Q)) for k in range(3))==camera and tuple(cert.get('camera',()))==camera and
+            oracle.offset(eye,forward,right,(666,358,-512))==muzzle,'full signed camera backoff and Eye-based Pistol muzzle')
+    require(response[10:82]==struct.pack('<18i',*eye,*ideal,*camera,*muzzle,*forward,*right) and
+            response[82:134]==oracle.encode_hit(cert['first']) and
+            response[134:147]==bytes(0x80+3*p+k for k in range(13)) and
+            response[147:160]==bytes(0xa0+3*p+k for k in range(13)),
+            'all160 logical/Fault/own-FIRST obstruction/guard bytes remain the existing independent response')
+    axis=(row['foot'][2]+1126,row['foot'][2]+row['height']-1126)
+    require(row['foot']==(eye[0],eye[1],eye[2]-3174) and row['height']-row['eye']==564 and
+            all(0<=row['foot'][k]<=262144 for k in (0,1)) and -131072<=row['foot'][2] and row['foot'][2]+row['height']<=131072 and
+            axis==((-1688,-202) if translated else (-1365,121)) and axis[0]<0 and
+            cert.get('physical358_safe') is True and cert.get('projected_margin_ge31') is True,
+            'scalar valid but capsule strictly intersects floor; BODY_FALSE/source NOT_PROVED; physical358/projected31 retained')
+    counts=[]
+    for k in (0,1):
+        low=max(0,(lo[k]-360)//1024-int((lo[k]-360)%1024==0));high=min(63,(hi[k]+360)//1024)
+        counts.append(high-low+1)
+    require(counts[0]*counts[1]<=coverage['conservative_cells_per_pass'],
+            'conservative fixed-cell enclosure only, original work caps unchanged, not measured work')
+    coverage.update(source_adoption='D357/D359',poison=p,BODY_FALSE_SCALAR_VALID_ONLY=True,
+      runtime_source_authority='NOT_PROVED',proof_method='EXISTING_COMPLETE_RESULT_FIXED_F1_POLYNOMIAL_WINDOW_NAMED_CELLS_NO_SECOND_SWEEP')
+    cert['remaining_contact_coverage']=coverage
+    return True
+
 def semantic_certificate(row,predicate,response,cert,oracle,angles,bindings,identity_proof,fixtures_):
     """Every requested semantic key must be proved or explicitly returned.
 
@@ -1879,6 +2107,8 @@
         checks['d343_negative_half']=negative_half_certificate(row,response,cert,oracle,angles,fixtures_[1],identity_proof)
     if 'd355_graze_miss' in predicate:
         checks['d355_graze_miss']=graze_miss_certificate(row,response,cert,oracle,angles,fixtures_[4],identity_proof)
+    if 'd359_remaining_contact' in predicate:
+        checks['d359_remaining_contact']=remaining_contact_certificate(row,response,cert,oracle,angles,fixtures_[1],identity_proof)
     annotations={'pair','relation','member'}
     for key,value in predicate.items():
         if key in annotations:continue
@@ -1972,6 +2202,45 @@
         a,b=dict(decoded[j]),dict(decoded[j+1]);a.pop('id');b.pop('id')
         need(a.pop('poison')==0 and b.pop('poison')==1 and a==b,'both full poisons per refusal seed')
         need(expected[160*j+1]==expected[160*(j+1)+1]==0 and expected[160*j+2:160*j+10]==expected[160*(j+1)+2:160*(j+1)+10],'same exact refusal tuple under both poisons')
+    for base,kind in ((1488,'same-bin'),(1504,'initial-skip')):
+        poses=set();different_variants=set()
+        for case_id in range(base,base+16):
+            j,p=divmod(case_id-base,2);row=decoded[case_id]
+            certificate=catalog[case_id]['certificate'];coverage=certificate.get('remaining_contact_coverage',{})
+            if kind=='same-bin':
+                yaw,xy,_,face_id,edge_id=SAME_BIN_LITERALS[j];foot=(*xy,-2491);pitch=8000
+                need(coverage.get('strict_distinct_physical_roots') is True and
+                     coverage.get('same_q')==241517137 and coverage.get('face_id')==face_id and
+                     coverage.get('edge_id')==edge_id and coverage.get('first_differs_from_priority')==(j in (2,3,4,5)) and
+                     coverage.get('outside_xy_minimum')==(29952 if j%2 else 30976) and
+                     coverage.get('expanded360_outside_xy_residual')>=29592,
+                     'all16 actual distinct roots/shared q/each own first-priority witness and corrected D357 bound')
+                if certificate['first']!=certificate['priority']:different_variants.add(j)
+            else:
+                yaw=YAWS[j];foot=(33792,33792,-2814);pitch=286
+                need(coverage.get('initial_whole_primitive_skips')==[6241,6244,6433,6436] and
+                     coverage.get('later_NEW_first_and_priority')==TANGENT_LITERALS[j][2]+195 and
+                     coverage['later_NEW_first_and_priority'] not in coverage['initial_whole_primitive_skips'] and
+                     certificate['first']==certificate['priority'],
+                     'all16 four whole initial skips and a different coherent later NEW first AND priority')
+            need(row['fixture']==1 and row['weapon']==1 and row['aim']==(yaw,pitch) and row['foot']==foot and
+                 (row['height'],row['eye'],row['poison'])==(3738,3174,p) and row['view_flags']==0 and row['revision']==1 and
+                 row['actor_count']==row['box_count']==0 and row['rule_slot']==65535 and
+                 row['rule_value']==row['table_kind']==row['table_index']==row['table_value']==0,
+                 'actual serialized D359 pose/aim/rig/body/poison/default mapping')
+            need(catalog[case_id]['proved_predicates'].get('d359_remaining_contact') is True and
+                 (coverage.get('kind'),coverage.get('variant'),coverage.get('poison'))==(kind,j,p) and
+                 coverage.get('runtime_source_authority')=='NOT_PROVED' and certificate['body_feasible'] is False and
+                 expected[160*case_id:160*case_id+2]==bytes((1,1)),
+                 'all32 actual complete successful own contact certificates; BODY_FALSE/source NOT_PROVED')
+            poses.add((row['aim'],row['foot']))
+        need(len(poses)==8 and different_variants==({2,3,4,5} if kind=='same-bin' else set()),
+             'eight actual poses each; exactly four variants with later-edge priority different from first')
+        for case_id in range(base,base+16,2):
+            left,right=dict(decoded[case_id]),dict(decoded[case_id+1]);left.pop('id');right.pop('id')
+            need(left.pop('poison')==0 and right.pop('poison')==1 and left==right and
+                 expected[160*case_id+2:160*case_id+134]==expected[160*(case_id+1)+2:160*(case_id+1)+134],
+                 'both original full poisons per D359 literal, complete successful solution/Fault equality')
     for base,kind in ((1392,'graze'),(1408,'miss')):
         poses=set()
         for j in range(base,base+16):
@@ -2510,8 +2779,12 @@
             return row,{'clear' if stratum==8 else 'hit':True,'clamped':False,'body_feasible':False,
                         'initial_eye_clearance':361,'d355_graze_miss':True}
         elif stratum in (13,14):
-            name={13:'same-Q32 competing roots',14:'initial nonclosing skip followed by other primitive Hit'}[stratum]
-            raise oracle.ConstructionRequired(case_id,name,'literal independently certified fixed-rig/full-fixture variant required')
+            if stratum==13:
+                yaw,xy,_,_,_=SAME_BIN_LITERALS[j]
+                row.update(fixture=1,weapon=1,height=3738,eye=3174,aim=(yaw,8000),foot=(*xy,-2491))
+            else:
+                row.update(fixture=1,weapon=1,height=3738,eye=3174,aim=(YAWS[j],286),foot=(33792,33792,-2814))
+            return row,{'hit':True,'clamped':False,'body_feasible':False,'d359_remaining_contact':True}
         elif stratum==10:
             row['aim']=(YAWS[j],8000);near_plane(row,oracle,angles,1);predicate={'clamped':True}
         elif stratum==12:
--- a/tests/outbreak/camera/release-1/SCHEMA.md
+++ b/tests/outbreak/camera/release-1/SCHEMA.md
@@ -1,6 +1,6 @@
 # Camera proof harness schema — source proposal 1
 
-T1901.5 / D305/D321/D325/D334/D343/D345/D355 / CAMERA_FOUNDATION0.9. **NOT GENERATED, NOT COMPILED,
+T1901.6 / D305/D321/D325/D334/D343/D345/D355/D357/D359 / CAMERA_FOUNDATION1.0. **NOT GENERATED, NOT COMPILED,
 NOT EXECUTED, NOT ACCEPTED.** This file specifies future private harness bytes;
 it adds no production wire format, API, geometry hook or runtime caller.
 Corrected T182 sections4–8 and D287 govern. A later MAIN release must bind real
@@ -608,6 +608,109 @@
 independent reviewb02d8cc354d585c14670547edc15424054ec026e09bcd70bfcf7d6367eae53f2;
 D345 interpretation and D355 narrow source lease. Old notes remain immutable.
 D321/D325/D334/D343 mappings/routines/coverage,4096/64/94 and every cap remain.
-Unadopted T210 strata13/14 retain their ConstructionRequired gates.
+D359 below separately supplies strata13/14 from qualified T210 mathematics.
 No parser/import/helper/oracle/control/generator/preparation/compiler/query/
 FFI/runtime/output root or target/corpus/frame/realG2/currentG1 acceptance.
+
+## D357/D359 distinct roots/same Q32 and translated initial skips
+
+Only existing1488..1519 change. Same-bin rows1488+2*j+p use j=2*r+a,
+r0..3 quarter rotations about(32768,32768),a0/1 tile placements,p0/1 original
+full poisons. Original F1/Crouch3738/3174/Pistol/pitch8000,base
+Eye(33280+1024*a,32828,683),footZ−2491,canonical unpatched rules/table,
+actors0/boxes0,revision1 and all original defaults remain.
+The original full-sum D is rotation(1280,−1067,−5744),
+FULL boom square35770425,L5980,k23701325,qs217815812.
+
+|j|Yaw|EyeXY|Earlier face first ID|Later edge ID|Priority ID|Edge feature|
+| ---: | ---: | --- | ---: | ---: | ---: | ---: |
+|0|0|(33280,32828)|6049|6241|6049|15|
+|1|0|(34304,32828)|6052|6244|6052|15|
+|2|16384|(32708,33280)|6241|6238|6238|13|
+|3|16384|(32708,34304)|6433|6430|6430|13|
+|4|32768|(32256,32708)|6238|6046|6046|17|
+|5|32768|(31232,32708)|6235|6043|6043|17|
+|6|49152|(32828,32256)|6046|6049|6046|11|
+|7|49152|(32828,31232)|5854|5857|5854|11|
+
+Face t0=323/5744 is strictly interior to its original floor cell atZ360.
+The neighbour's edge excess is34132025*t²−7974344*t+340489,
+discriminant17103845989436>0,nonsquare. Its coefficient34132025 is NOT
+the full boom square. f(t0)=1/5744²>0,f(t0+1/(16Q))<0 and negative derivative
+over that interval prove a genuinely DISTINCT later entering algebraic root tau.
+Both strict exterior edge axes remain valid over the interval.
+Q*323=5744*241517137+1680 and105/359+1/16<1 prove
+t0<tau<t0+1/(16Q)<(q+1)/Q with shared q241517137.
+An equal-root or q-only substitute cannot satisfy this check.
+
+The entire anchored11 window is below0.06. Every other column is at least435.2
+away and every other row at least964 away;only the two named floor identities
+can contact there. Uniform original F1 has no other terrain/actors/boxes.
+Full-segment outsideXY minimum is30976 for a0,29952 for a1,uniformly>=29952;
+expanded360 residual>=29592. This is the D357 correction governing immutable
+T210 notes. Ceilings remain at least15701 away;outsideZ planes stay separated.
+First is always the earlier face. Four variants j2/3/4/5 choose the later
+smaller-ID edge as priority. Camera obstruction remains the complete own FIRST.
+
+Each root's own q/distance336/point is checked. Both rounded points coincide
+at the corresponding rotation of(33352+1024*a,32768,0);their roots/normals
+remain different. Face normal is(0,0,S). Edge actual reported-q closest
+vector is rotation(0,−747419,360Q+1680),ceil norm1546188228241;
+truncation gives rotation(0,−519,S−1). Priority compares the ENTIRE
+corresponding own witness,not swapped ID alone. Exact polynomial/interval/
+feature/own-witness mathematics also certifies the nonpublished competitor
+when priority remains first;metadata labels that supplemental mathematical
+record,not another query result. No new Root construction or root stream.
+
+Whole signed backoff gives rotated(65,−54,−291),cameraZ392.
+Eye-based Pistol muzzle offset is rotation(358,116,144),muzzleZ827.
+Full response positions/bases/own-first obstruction/Fault/guards are checked.
+Body foot−2491/top1247 is scalar-valid but living axis[−1365,121] strictly
+intersects floor0:BODY_FALSE/SCALAR_VALID_ONLY,source authority NOT_PROVED.
+Physical358 clearance34 and original projected31 margin remain separate.
+
+Translated initial-skip rows1504+2*j+p explicitly REUSE reviewed T201/D334
+mathematics plus translation(1024,1024,0),without changing D334's helper,
+table,old rows or coverage. All eight original yaws/pitch286,F1/Pistol/Crouch,
+Eye(33792,33792,360),footZ−2814 and both original poisons remain.
+These are different actual poses,not a claim of a new mechanism.
+
+Initial floor IDs6241/6244/6433/6436 each touch360 with closing dot0;
+no strict overlap exists. Each skips for the WHOLE primitive.
+Later NEW IDs6052/6247/6439/6628/6625/6430/6238/6049 are outside that set.
+Their adjacent polynomial(1024−v*t)² has the true positive double root
+128/767 or256/1311;at physical contact only +Z is strictly exterior,so D327
+canonical feature5 is retained. Five named existing cells supplement the
+fixed uniform F1 premise. Every anchored time<1/5 has only the one new
+non-skipped cell;outsideXY>=25608,ceiling distance16024 and outsideZ
+separations exhaust full fixture geometry.
+
+Translated own points/camera/muzzle are exactly T201+the integer translation;
+IDs add195. Even j retain q716761165/distance1046/qs694148861;
+odd j q838681638/distance1224/qs816069334;all L6268,k22612304.
+Full own first=priority and reported-q witness are checked independently.
+Body foot−2814/top924 overlaps floor:BODY_FALSE/SCALAR_VALID_ONLY,
+source NOT_PROVED. Physical358 clearance2/projected31 are retained;
+normal setback0 is not substituted for projected margin.
+
+`remaining_contact_certificate` uses only fixed basis/scalar/rational/
+polynomial/derivative/window/own-witness checks and named ALREADY decoded cells
+against the ONE existing COMPLETE oracle result. Original F1 source construction
+is the complete geometry premise. Conservative9cells/pass for same-bin
+(18boxes/132intervals/264roots) or35cells/pass for translated skips
+(70boxes/496intervals/992roots) fit unchanged original limits,not measured work.
+No second fixture decode/sweep/root enumeration/constructor/evaluator/search
+or response producer is added. All160 bytes remain from the independent oracle
+and fully compared against future real targets.
+Decoded coverage binds all32 actual requests to their exact poses/defaults/
+poisons and complete certificates,eight actual poses each,exactly four variants
+with first!=priority,and later IDs distinct from every whole-primitive skip.
+
+D359 adopts T210 proposal1e7013d9b40f1a8903a8d1d6d06314fcb9de1e3046101457fc5cb6f3a84441d7,
+full reviewe99cff90d9927b54ba1acdc73a141799bbf95273d8a1b90dd209d3c3e030dce2,
+qualified by D357's corrected29952 bound. All original notes stay immutable.
+D321/D325/D334/D343/D355 mappings/routines/coverage,4096/64/94 and all
+byte/work/time/bit/frame/source/terminal/caller/realG2/currentG1 gates remain.
+Other unconstructed predicates are still gated. No parser/import/helper/oracle/
+control/generator/preparation/compiler/query/FFI/runtime/result-root effect.
+No complete source/corpus/camera/target/runtime/caller/game acceptance.
--- a/tests/outbreak/camera/release-1/README.md
+++ b/tests/outbreak/camera/release-1/README.md
@@ -1,6 +1,6 @@
 # T190 camera harness — source review package
 
-**T1901.5 / D355 narrow later-graze/curved-miss source correction. SOURCE ONLY. NOT COMPILED /
+**T1901.6 / D359 narrow distinct-root/initial-skip source correction. SOURCE ONLY. NOT COMPILED /
 NOT EXECUTED / NOT ACCEPTED.** No setup, request,
 golden, control result, preparation, attempt or final evidence has been
 generated by this package. D305 authorizes only these six new files and the
@@ -22,10 +22,11 @@
 Read corrected [T182](../../../../notes/proposals/T182-camera-implementation-release-packet-1.md)
 sections4–8, [T190](../../../../tickets/T190.md),
 [D305](../../../../notes/decisions/D305-camera-proof-harness-source-release.md),
-and [CAMERA_FOUNDATION0.9](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
+and [CAMERA_FOUNDATION1.0](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
 sixteen existing q=k+1 literals; D325 supplies112 identity/face rows; D334 supplies
 sixteen initial-tangent/later-Hit rows; D343 supplies32 negative-half rows;
-D345/D355 supply32 later-graze/curved-miss rows below. The adjacent
+D345/D355 supply32 later-graze/curved-miss rows; D357/D359 supply32
+distinct-root/initial-skip rows below. The adjacent
 SCHEMA is private test framing, not a new gameplay interface. No code here
 implements MotionState, observer selection, authority or a usable game camera.
 
@@ -41,10 +42,11 @@
 
 The catalog is **not proved realizable**. Source `ConstructionRequired` gates
 remain for exact edge/corner tangency, shallow-face variants, near-Q32 bins,
-competing first/priority and same-bin roots, and other initial strata.
+other competing first/priority cases and other initial strata.
 D325 resolves the fixed-map identity interpretation and112 inputs; D334 resolves
 the exact16 initial-tangent/later-Hit rows; D343 resolves32 negative-half rows;
-D355 resolves only32 reviewed later-graze/curved-miss rows below.
+D355 resolves32 reviewed later-graze/curved-miss rows; D359 resolves only32
+reviewed distinct-root/translated initial-skip rows below.
 Other literal candidates,including normal
 margin counterexamples, are also subject to exact feature/body/first/root
 checks; existence of a formula is not a passing certificate. Failed semantic
@@ -382,9 +384,59 @@
 
 Only these32 formerly gated rows and their supplementary checks/docs change.
 D321/D325/D334/D343 mappings/routines/coverage,64controls,94children and every
-cap remain. T210 notes are unadopted;strata13/14 retain their existing gates.
+cap remain. D359 below separately supplies strata13/14 from qualified T210 mathematics.
 All old T206/T210 notes and source evidence remain immutable.
 No parser/import/helper/oracle/control/generator/preparation/compiler/query/
 FFI/runtime or output-root effect occurred. Complete catalog/source/target/
 realG2/currentG1/frame/caller/gameplay/browser/human gates remain pending.
 Stable source/diff/handoff requires MAIN review;no automatic next stage.
+
+## D357/D359: distinct physical roots and whole-primitive initial skips
+
+[D359](../../../../notes/decisions/D359-camera-remaining-contact-source-release.md)
+releases only1488..1519 from [T210](../../../../notes/proposals/T210-remaining-contact-construction-1.md)
+and its [full mathematical review](../../../../notes/reviews/T210-remaining-contact-math-review-1.md),
+qualified by [D357](../../../../notes/decisions/D357-remaining-camera-mathematics-qualified-receipt.md).
+The corrected uniform outsideXY minimum is29952,radius360 residual29592.
+Old proposal/review/handoff records remain immutable.
+
+Same-bin1488..1503 use four cardinal pitch8000 rotations/two tile placements/
+both poisons,F1/Pistol/Crouch,EyeZ683,footZ−2491,full rig
+rotation(1280,−1067,−5744),L5980,k23701325,qs217815812.
+Unique earlier face t0=323/5744 and a genuinely DISTINCT later algebraic edge
+root of34132025*t²−7974344*t+340489 share q241517137.
+Strict signed polynomial/derivative/interval/bin checks establish their order
+and own valid physical features. The edge coefficient is not full boom35770425.
+The full anchored11 window has only two eligible floor identities.
+First stays the coherent earlier +Z face;four variants choose the later
+smaller-ID edge as priority with ITS OWN normal/feature/point/distance.
+Even when not published,the competitor has a bounded mathematical certificate,
+not another query. Coincident rounded q/points never substitute for root equality.
+
+Initial-skip1504..1519 disclose reuse of T201/D334 mathematics translated
+(1024,1024,0),eight original yaws/pitch286/Eye(33792,33792,360),
+footZ−2814. D334's old helper/mappings/results/coverage remain unchanged.
+Four initial IDs6241/6244/6433/6436 touch360 nonclosingly and each skip for
+the WHOLE primitive. Later NEW IDs6052/6247/6439/6628/6625/6430/6238/6049
+are outside that skip set. Exact later double roots retain D327 canonical
++Z face5;complete first AND priority own witnesses follow the full F1/window proof.
+These are different actual poses,not a claim of a new mechanism.
+
+The new bounded certificate checks actual defaults/serialized associations,
+basis/full-sum rig,root/bin/feature/interval/order,full original F1 exclusions,
+each own first/priority witness,signed camera rounding,Eye-based muzzle,
+all logical fields/Fault/guards and physical358/projected31 evidence.
+Only named already-decoded cells/fixed arithmetic supplement the existing
+complete oracle;no second decode/sweep/Root construction/root stream/search/
+constructor or output substitution. Full160-byte expected observations still
+come from the ONE independent oracle resolution and future real target comparison.
+Work enclosures9 or35cells/pass stay within original caps and are not measured.
+
+All32 are BODY_FALSE/SCALAR_VALID_ONLY with runtime source NOT_PROVED.
+Logical query success does not grant living/observer/shot eligibility.
+Prior D321/D325/D334/D343/D355 tables/routines/coverage,4096/64/94 and
+every original budget/gate remain. All other unresolved constructions still
+refuse;no complete source/catalog/target/realG2/currentG1/frame/caller/browser/
+game/human acceptance follows. No source parser/import/helper/oracle/control/
+generation/preparation/compiler/query/FFI/runtime/output-root effect occurred.
+Stable diff/handoff requires MAIN review;no automatic next stage.
```
