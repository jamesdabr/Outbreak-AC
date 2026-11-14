# T1901.4 / D343 focused three-source diff

Source-text comparison only against the captured T1901.3 snapshot. No parser, import or project execution.

```diff
--- a/tests/outbreak/camera/release-1/verify.py
+++ b/tests/outbreak/camera/release-1/verify.py
@@ -1552,6 +1552,110 @@
       'proof_method':'EXISTING_RESULT_FIVE_DECODED_CELLS_FIXED_WINDOW_ARITHMETIC_NO_SECOND_SWEEP'}
     return True
 
+def negative_half_certificate(row,response,cert,oracle,angles,fixture,identity_proof):
+    """D343 bounded supplement to the ONE existing complete F1 result.
+
+    Fixed planes, two tile bounds and body arithmetic only; no additional
+    decode, sweep, root enumeration, search or constructor/output replay.
+    """
+    def require(condition,detail):
+        if not condition:raise oracle.ConstructionRequired(row['id'],'D343 negative displacement half',detail)
+    require(2592<=row['id']<2624,'exact existing32-row range')
+    i,s,p=(row['id']-2592)//4,((row['id']-2592)//2)%2,(row['id']-2592)%2
+    rotated=i>=4;t=1024*(i%4);axis=1 if rotated else 0
+    eye=(3300,33894+t,8192) if rotated else (33894+t,62236,8192)
+    delta=(-6127,-1280,766) if rotated else (-1280,6127,766)
+    yaw=49152 if rotated else 32768;identity=196608 if rotated else 196611
+    height,eye_height=((3738,3174),(5325,4608))[s]
+    require(row['fixture']==1 and row['weapon']==1 and row['aim']==(yaw,-428) and
+            row['height']==height and row['eye']==eye_height and row['poison']==p and
+            row['foot']==(eye[0],eye[1],8192-eye_height),'literal i/s/p, original Pistol/stances/poisons')
+    require(row['flags']==0 and row['revision']==1 and row['count']==row['boxes']==0 and
+            row['slot']==65535 and row['rule_value']==0 and
+            row['table_kind']==row['table_index']==row['table_value']==0,'canonical unpatched context')
+    require(response[:2]==bytes((1,1)) and response[2:10]==bytes(8) and
+            cert.get('physical_query') is True,'successful complete independent observation')
+    scale=1<<30
+    require((angles[0],angles[16384],angles[16385+428],angles[16385+8572])==
+            (0,scale,80134038,1070747421),'four named accepted angle DATA entries')
+    forward,right=oracle.basis(angles,yaw,-428)
+    require((forward,right)==(((1070747421,0,-80134038),(0,-scale,0)) if rotated else
+            ((0,-1070747421,-80134038),(-scale,0,0))),'independent normalized basis')
+    require(tuple(cert.get('eye',()))==eye and tuple(cert.get('delta',()))==delta and
+            rig(row,oracle,angles)==delta,'original full-sum FRU rig, not arbitrary displacement')
+    length2=sum(d*d for d in delta);length=math.isqrt(length2);k=(33*Q+length-1)//length
+    q,qs=2060911351,2038431744;time=F(2940,6127)
+    require((length2,length,k)==(39765285,6305,22479607) and q-k==qs>0 and
+            (cert.get('L0'),cert.get('k'),cert.get('q'),cert.get('qs'))==(length,k,q,qs) and
+            cert.get('clamped') is False,'independent norm/backoff and actual nonclamped bins')
+    require(Q*2940-q*6127==2663 and (q+1)*6127-Q*2940==3464 and
+            (q*6127+Q-1)//Q==((q+1)*6127-1)//Q==2940 and 766<=2940<=6127,
+            'exact floor-Q32 bin and singleton gap2940')
+    root=cert.get('root')
+    require(type(root) is dict and F(*root['lo'])==F(*root['hi'])==time and
+            tuple(root['poly'])==oracle.primitive((-time,1)) and root['q']==q,
+            'actual independently resolved own rational root2940/6127')
+    summary=identity_proof['fixtures'][1]
+    require(fixture['side']==64 and fixture['revision']==1 and fixture['entities']==0 and
+            len(fixture['cells'])==4096 and summary['cell0']==[4,0,16,0] and
+            summary['lowest_floor']==0 and summary['highest_ceiling']==16,
+            'original fixed uniform F1 construction and existing one-decode summary')
+    end=tuple(eye[a]+delta[a] for a in range(3))
+    low=tuple(min(eye[a],end[a]) for a in range(3));high=tuple(max(eye[a],end[a]) for a in range(3))
+    gaps=(low[0]-360,65536-high[0]-360,low[1]-360,65536-high[1]-360,
+          low[2]+131072-360,131072-high[2]-360)
+    target=0 if rotated else 3
+    require(gaps==((-3187,61876,32254+t,31282-t,138904,121754) if rotated else
+            (32254+t,31282-t,61876,-3187,138904,121754)) and
+            all(gap>0 for a,gap in enumerate(gaps) if a!=target),'all five non-target outside planes excluded over WHOLE segment')
+    require(low[2]-360==7832 and 16384-high[2]-360==7066,
+            'strict uniform Z gaps exclude ALL F1 floor/ceiling faces/edges/corners')
+    closing_axis=0 if rotated else 1;sign=1 if rotated else -1
+    bound=0 if rotated else 65536
+    require(sign*(eye[closing_axis]-bound)-360==2940 and
+            sign*delta[closing_axis]==-6127,'only target plane enters, hence unique first AND priority')
+    tile_counts=[]
+    for a in (0,1):
+        lo=max(0,(low[a]-360-1)//1024);hi=min(63,(high[a]+360)//1024)
+        tile_counts.append(max(0,hi-lo+1))
+    require(tile_counts==([4,3] if rotated else [3,4]) and
+            tile_counts[0]*tile_counts[1]<=12,'conservative closed-cell enclosure12/pass, not measured work')
+    first,priority=cert.get('first'),cert.get('priority')
+    normal=(scale,0,0) if rotated else (0,-scale,0)
+    require(type(first) is dict and first==priority and first.get('status')==first.get('kind')==1 and
+            first.get('id')==identity and first.get('q')==q and first.get('zone')==0 and
+            first.get('normal')==normal and cert.get('feature_axes')==[closing_axis] and
+            cert.get('feature_signs')==[sign] and cert.get('feature')==2*closing_axis+(sign>0),
+            'coherent actual World/None own first/priority/normal/feature')
+    product=delta[axis]*qs;displacement=oracle.nearest(F(product,Q))
+    correct=eye[axis]+displacement;absolute=oracle.nearest(F(eye[axis]*Q+product,Q))
+    require(product==-2609192632320 and F(product,Q)==F(-1215,2) and
+            abs(product)%Q==Q//2 and displacement==-608 and
+            F(eye[axis]*Q+product,Q)>0 and correct==33286+t and absolute==correct+1,
+            'negative displacement ties AWAY before integer addition; positive absolute half differs')
+    camera=tuple(cert.get('camera',()))
+    require(camera==tuple(eye[a]+oracle.nearest(F(delta[a]*qs,Q)) for a in range(3)) and
+            camera[axis]==correct and response[34:46]==struct.pack('<iii',*camera) and
+            response[82:134]==oracle.encode_hit(first),'checked selected half in full independently derived response')
+    foot=row['foot'];body_gaps=(eye[0]-1126,65536-eye[0]-1126,eye[1]-1126,65536-eye[1]-1126)
+    require(body_gaps==((2174,61110,32768+t,30516-t) if rotated else
+            (32768+t,30516-t,61110,2174)) and min(body_gaps)>0 and
+            foot[2]==(5018 if s==0 else 3584) and foot[2]>0 and
+            16384-foot[2]-height==(7628 if s==0 else 7475) and height-eye_height>=564 and
+            all(0<=foot[a]<=262144 for a in (0,1)) and -131072<=foot[2] and
+            foot[2]+height<=131072 and cert.get('body_feasible') is True,
+            'BOTH exact body endpoints feasible and scalar-valid; caller authority unproved')
+    require(cert.get('physical358_safe') is True and cert.get('projected_margin_ge31') is True and
+            response[134:147]==bytes(0x80+3*p+a for a in range(13)) and
+            response[147:160]==bytes(0xa0+3*p+a for a in range(13)),'full safety/margin and both poison guards retained')
+    cert['negative_half_coverage']={'source_adoption':'D343','variant':i,'stance':s,'poison':p,
+      'true_root':[2940,6127],'gap':2940,'selected_axis':axis,'selected_product':product,
+      'displacement_first_coordinate':correct,'absolute_rounding_coordinate':absolute,
+      'whole_segment_outside_gaps':list(gaps),'whole_segment_floor_ceiling_gaps':[7832,7066],
+      'conservative_cells_per_pass':12,'BODY_FEASIBLE':True,'runtime_source_authority':'NOT_PROVED',
+      'proof_method':'EXISTING_COMPLETE_RESULT_FIXED_F1_PLANES_BOUNDED_ARITHMETIC_NO_SECOND_SWEEP'}
+    return True
+
 def semantic_certificate(row,predicate,response,cert,oracle,angles,bindings,identity_proof,fixtures_):
     """Every requested semantic key must be proved or explicitly returned.
 
@@ -1595,6 +1699,8 @@
         checks['d325_identity']=identity_certificate(row,response,cert,oracle,angles,bindings,identity_proof)
     if 'd334_initial_tangent' in predicate:
         checks['d334_initial_tangent']=initial_tangent_certificate(row,response,cert,oracle,angles,fixtures_[1],identity_proof)
+    if 'd343_negative_half' in predicate:
+        checks['d343_negative_half']=negative_half_certificate(row,response,cert,oracle,angles,fixtures_[1],identity_proof)
     annotations={'pair','relation','member'}
     for key,value in predicate.items():
         if key in annotations:continue
@@ -1695,6 +1801,23 @@
              catalog[j]['certificate']['initial_tangent_coverage']['initial_skipped_floor_ids']==[6046,6049,6238,6241] and
              catalog[j]['certificate']['body_feasible'] is False and expected[160*j+1]==1 and
              decoded[j]['poison']==(j-1344)%2,'all16 adopted exact tangents with later real face Hit and both poisons')
+    for j in range(2592,2624):
+        coverage=catalog[j]['certificate'].get('negative_half_coverage',{})
+        i,s,p=(j-2592)//4,((j-2592)//2)%2,(j-2592)%2
+        h,e=((3738,3174),(5325,4608))[s];t=1024*(i%4)
+        x,y=(3300,33894+t) if i>=4 else (33894+t,62236)
+        r=decoded[j]
+        need(r['fixture']==1 and r['weapon']==1 and r['aim']==(49152 if i>=4 else 32768,-428) and
+             r['foot']==(x,y,8192-e) and (r['height'],r['eye'],r['poison'])==(h,e,p) and
+             r['view_flags']==0 and r['revision']==1 and r['actor_count']==r['box_count']==0 and
+             r['rule_slot']==65535 and r['rule_value']==r['table_kind']==r['table_index']==r['table_value']==0,
+             'actual serialized D343 row/rig/body/context association')
+        need(catalog[j]['proved_predicates'].get('d343_negative_half') is True and
+             (coverage.get('variant'),coverage.get('stance'),coverage.get('poison'))==
+             ((j-2592)//4,((j-2592)//2)%2,(j-2592)%2) and
+             catalog[j]['certificate']['body_feasible'] is True and expected[160*j+1]==1 and
+             decoded[j]['poison']==(j-2592)%2 and coverage.get('conservative_cells_per_pass')==12,
+             'all32 adopted negative-half variants/stances/poisons and feasible-body certificates')
     roles={}
     for j in range(2432,2496):
         entry=catalog[j];coverage=entry['certificate'].get('identity_coverage',{})
@@ -2219,7 +2342,13 @@
         row['height'],row['eye']=(3738,3174) if seed%2==0 else (5325,4608)
         row.update(aim=(8192+(seed//2)*16384,0),weapon=1+variant//2,poison=variant%2)
         if group==0:predicate={'clear':True,'single_sum_difference':True}
-        elif group==1:raise oracle.ConstructionRequired(case_id,'negative displacement half tie','literal q/product/E-sign certificate required; no absolute-coordinate substitute')
+        elif group==1:
+            i,s,p=local//4,(local//2)%2,local%2
+            height,eye_height=((3738,3174),(5325,4608))[s];t=1024*(i%4)
+            x,y=(3300,33894+t) if i>=4 else (33894+t,62236)
+            row.update(fixture=1,weapon=1,aim=(49152 if i>=4 else 32768,-428),
+                       height=height,eye=eye_height,foot=(x,y,8192-eye_height),poison=p)
+            return row,{'hit':True,'clamped':False,'body_feasible':True,'d343_negative_half':True}
         elif group==2:
             row.update(height=3738,eye=3174,aim=(YAWS[seed],8000));near_plane(row,oracle,angles,(-1,0,1,2)[variant]);predicate={'reserve_distance':359+variant}
         elif group==3:
--- a/tests/outbreak/camera/release-1/SCHEMA.md
+++ b/tests/outbreak/camera/release-1/SCHEMA.md
@@ -1,6 +1,6 @@
 # Camera proof harness schema — source proposal 1
 
-T1901.3 / D305/D321/D325/D334 / CAMERA_FOUNDATION0.7. **NOT GENERATED, NOT COMPILED,
+T1901.4 / D305/D321/D325/D334/D343 / CAMERA_FOUNDATION0.8. **NOT GENERATED, NOT COMPILED,
 NOT EXECUTED, NOT ACCEPTED.** This file specifies future private harness bytes;
 it adds no production wire format, API, geometry hook or runtime caller.
 Corrected T182 sections4–8 and D287 govern. A later MAIN release must bind real
@@ -465,3 +465,61 @@
 occupied. Terminal unlink/retention returning late remains refusal/unresolved;
 no new grace, automatic overwrite, receipt rewrite, retry or final inventory
 follows. Final inventory/receipt/freeze is a separately released future step.
+
+## D343 exact negative displacement half rows
+
+Only existing rows2592..2623 use `2592+4*i+2*s+p`, i0..7,s0/1,p0/1.
+Stance s0 is Crouch(h3738,e3174,footZ5018); s1 is
+Standing(h5325,e4608,footZ3584). Both original output/Fault/guard poisons
+remain p. All use original F1/Pistol,pitch−428,EyeZ8192,actors0/boxes0,
+revision1,canonical unpatched rules/table and all other original defaults.
+
+| i | yaw | EyeXY | D | World first AND priority | normal |
+| --- | ---: | --- | --- | ---: | --- |
+|0..3|32768|(33894+1024*i,62236)|(−1280,6127,766)|196611|(0,−1073741824,0)|
+|4..7, j=i−4|49152|(3300,33894+1024*j)|(−6127,−1280,766)|196608|(1073741824,0,0)|
+
+Both use zoneNone,true root2940/6127,L06305,k22479607,
+qf2060911351,qs2038431744,clampedfalse. For selected baseX/rotatedY,
+D_axis*qs=−2609192632320,so displacement/Q=−607.5 exactly.
+Ties-away displacement rounding gives−608,THEN integer Eye addition gives
+33286+1024*(i%4). Positive absolute-coordinate rounding would give
+33287+1024*(i%4),one unit different; that substitute must fail.
+
+`negative_half_certificate` checks these independently against the existing
+complete oracle result,including four named angle DATA entries,normalized
+basis/full-sum rig,length/backoff,true own rational root and floor-Q32 bin.
+The gap interval is exactly[2940,2940]:Q*2940−qf*6127=2663 and
+(qf+1)*6127−Q*2940=3464. Both positive remainders constrain the same gap.
+
+Complete geometry uses the ORIGINAL uniform F1 source construction and the
+already decoded fixture/summary. Whole-segment floor/ceiling gaps are7832/7066.
+Every other outside plane has a strictly positive whole-segment gap; the
+selected target alone closes from2940 at speed6127. Actors/boxes are absent
+and no F1 solid cells exist. This excludes all other physical roots,including
+cell faces/edges/corners and every anchored11 priority competitor,so the real
+first AND priority must be the target with its own normal/World/None identity.
+The closed swept XY enclosure spans at most3 by4 in-map tiles,conservatively
+12cells/pass. This is mathematical enclosure,not measured source/emitted work.
+No second map decode,sweep,root enumeration or constructor replay is added.
+
+Both original bodies are **BODY_FEASIBLE**: uniform floor/ceiling foot/top gaps
+are5018/7628 or3584/7475; every XY radius1126 gap is positive,minimum2174.
+Numeric feasibility does not authenticate runtime living/observer source
+authority. Certificate metadata explicitly keeps that authority NOT_PROVED.
+The selected camera coordinate,complete own hit,physical358 safety,original
+projected margin and poison guards are checked against the full independently
+derived160-byte observation. All remaining fields still come from the existing
+oracle; no full output is invented from the mathematical constructor record.
+Coverage additionally binds actual serialized32 rows to their i/s/p poses,
+stance/default/context fields and certificates.
+
+D343 adopts only the mathematical inputs reviewed in
+`notes/reviews/T205-found-certificate-variants-review-1.md`,SHA256
+7b45f3b96a91930bf199c65c59275a1401e92c2e2e155b5dc9d8c42c8ad59266.
+The closed raw candidate211e5c799f8ed942849c1959420f39b46d38b4b2738b7c8dd5589484cc35dd2c
+remains immutable mathematical DATA,not CameraSolution/query/runtime evidence.
+T206 mathematics/interpretation are separately governed and unchanged here.
+D32116,D325112,D33416 mappings/routines,all other rows,seams,4096/64/94 and
+every original byte/time/work/frame/source/caller/real-G2/current-G1 gate remain.
+No generator,oracle,parser,control,compiler,target or runtime was executed.
--- a/tests/outbreak/camera/release-1/README.md
+++ b/tests/outbreak/camera/release-1/README.md
@@ -1,6 +1,6 @@
 # T190 camera harness — source review package
 
-**T1901.3 / D334 narrow initial-tangent source correction. SOURCE ONLY. NOT COMPILED /
+**T1901.4 / D343 narrow negative-half source correction. SOURCE ONLY. NOT COMPILED /
 NOT EXECUTED / NOT ACCEPTED.** No setup, request,
 golden, control result, preparation, attempt or final evidence has been
 generated by this package. D305 authorizes only these six new files and the
@@ -22,9 +22,9 @@
 Read corrected [T182](../../../../notes/proposals/T182-camera-implementation-release-packet-1.md)
 sections4–8, [T190](../../../../tickets/T190.md),
 [D305](../../../../notes/decisions/D305-camera-proof-harness-source-release.md),
-and [CAMERA_FOUNDATION0.7](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
+and [CAMERA_FOUNDATION0.8](../../../../MVP/CAMERA_FOUNDATION.md). D321 adopts the
 sixteen existing q=k+1 literals; D325 supplies112 identity/face rows; D334 supplies
-sixteen initial-tangent/later-Hit rows below. The adjacent
+sixteen initial-tangent/later-Hit rows; D343 supplies32 negative-half rows below. The adjacent
 SCHEMA is private test framing, not a new gameplay interface. No code here
 implements MotionState, observer selection, authority or a usable game camera.
 
@@ -40,9 +40,9 @@
 
 The catalog is **not proved realizable**. Source `ConstructionRequired` gates
 remain for exact edge/corner tangency, shallow-face variants, near-Q32 bins,
-competing first/priority and same-bin roots, later graze/miss, initial
-nonclosing skip then later Hit,and negative displacement half-tie.
-D325 now resolves the fixed-map identity interpretation and112 inputs below.
+competing first/priority and same-bin roots, later graze/miss and other initial strata.
+D325 resolves the fixed-map identity interpretation and112 inputs; D334 resolves
+the exact16 initial-tangent/later-Hit rows; D343 resolves only32 negative-half rows below.
 Other literal candidates,including normal
 margin counterexamples, are also subject to exact feature/body/first/root
 checks; existence of a formula is not a passing certificate. Failed semantic
@@ -301,3 +301,40 @@
 permission to execute it. Final inventory/freeze, camera acceptance, composition,
 gameplay caller/authority/observer validation, browser/tick/human evidence and
 all held gates remain separate.
+
+## D343: exact negative half with both feasible body endpoints
+
+[D343](../../../../notes/decisions/D343-camera-negative-half-literal-adoption.md)
+adopts only the eight mathematical literals and both original stance endpoints
+from [the independent T205 review](../../../../notes/reviews/T205-found-certificate-variants-review-1.md),
+SHA2567b45f3b96a91930bf199c65c59275a1401e92c2e2e155b5dc9d8c42c8ad59266.
+Existing32 rows2592+4*i+2*s+p now use F1/Pistol,pitch−428,EyeZ8192,
+yaw32768/four tangential offsets or yaw49152/their reviewed rotation.
+Crouch and Standing keep original3738/3174 and5325/4608,footZ5018/3584;
+both original poison variants remain. Every body is BODY_FEASIBLE.
+Runtime source eligibility remains NOT_PROVED.
+
+The real target alone closes from gap2940 at speed6127. The exact root is
+2940/6127,qf2060911351,L06305,k22479607,qs2038431744.
+Selected baseX/rotatedY displacement is exactly−607.5: correct ties-away
+displacement rounding yields−608 before integer Eye addition,one unit below
+rounding the positive absolute half. This distinction is checked in the actual
+independent complete response,not inferred from a copied constructor label.
+
+The bounded certificate checks actual row/context,accepted angles/basis/rig,
+root/bin/gap,first AND priority World196611 or196608/zoneNone/own normal,
+body endpoints,selected rounding,guards and physical358/projected margin.
+Uniform F1 floor/ceiling gaps7832/7066 and five positive non-target outside
+gaps exclude every competing physical obstruction over the WHOLE segment.
+A conservative3-by4 tile enclosure gives12cells/pass. No second decode,sweep,
+root enumeration or new execution/work allowance is introduced. Full160-byte
+outputs continue through the existing independent oracle and future real target
+comparison; all remaining camera fields are independently derived there.
+
+This changes only the negative-half gate and its32 existing rows/checks/docs.
+D32116,D325112,D33416 mappings/routines,64controls,94children,all other rows
+and unresolved seams/caps remain. The original T205 outputs and three T206
+notes remain immutable; T206 is separately governed. Source/corpus,
+realG2/currentG1,frame/caller/browser/gameplay/human gates are still pending.
+No source/parser/oracle/generator/control/compiler/query/runtime was executed;
+no output roots or automatic follow-on stage are authorized.
```
