# Outbreak ticket register

Register revision: 0.5. Maintainer: coordinating lead only. D004 accepts T018/T019/T020 within their limited scopes, retains partial T016 as BLOCKED, re-releases T017 at 0.4, and releases T022-T025 under BROWSER_FOUNDATION.md 0.4. All other tickets remain DRAFT/unassigned or explicitly blocked. A released assignment authorizes only its exact scope; dispatch progress and handoff results are recorded separately. No complete browser game or phase acceptance is implied.

| ID | Phase | Ticket | Proposed specialty | Dependencies | Status |
| --- | --- | --- | --- | --- | --- |
| T001 | P0 | [Browser client and dedicated server builds](T001.md) | Engine and Multiplayer | T014/T015 evidence accepted; owner/lead platform decision recorded | DRAFT |
| T002 | P0 | [Shared simulation proposal](T002.md) | Engine and Multiplayer | T014/T015 evidence and owner/lead platform decision before final acceptance | DRAFT |
| T003 | P0 | [Baseline smoke and acceptance profiles](T003.md) | QA and Performance | T001 ACCEPTED for executable smoke; T002 approved for interface-dependent profiles | DRAFT |
| T004 | P1 | [Third-person movement and aim](T004.md) | Player and Combat | P0 ACCEPTED; P1 movement/weapon/interface values frozen | DRAFT |
| T005 | P1 | [Authoritative multiplayer combat](T005.md) | Engine and Multiplayer | P0 ACCEPTED; approved T002 interfaces and P1 values | DRAFT |
| T006 | P2 | [Blackwood encounter greybox](T006.md) | World and Match Systems | P1 ACCEPTED; approved anchor/world interfaces | DRAFT |
| T007 | P2 | [Server-controlled walker encounter](T007.md) | AI and Director | P1 ACCEPTED; T006 map/anchors ready and accepted for this integration; P2 AI parameters frozen | DRAFT |
| T008 | P2 | [Universal down revive and spectator rules](T008.md) | Player and Combat | P1 ACCEPTED; approved squad/life-state interfaces and P2 parameters; T006/T007 accepted before combined phase evidence | DRAFT |
| T009 | P3 | [Finite loot and wooden barricade](T009.md) | World and Match Systems | P2 ACCEPTED; P3 loot/repair/placement parameters and shared obstacle interfaces frozen | DRAFT |
| T010 | P3 | [Match extraction and reset](T010.md) | World and Match Systems | P2 ACCEPTED; P3 lifecycle/boarding parameters frozen; T009 accepted before full-loop evidence | DRAFT |
| T011 | P4 | [Predator Director-lite and eight-player integration](T011.md) | AI and Director | P3 ACCEPTED; P4 cue/perception/budget/recovery parameters and interfaces frozen | DRAFT |
| T012 | P5 | [MVP verification and candidate](T012.md) | QA and Performance | P4 ACCEPTED; T013 ACCEPTED for final MVP completion; approved assets and thresholds | DRAFT |
| T013 | P5 | [LLM tester interface placeholder](T013.md) | QA and Performance with Engine and Multiplayer | Separate owner/lead tester contract APPROVED; implementation phase and precise dependencies set at that time | DRAFT |
| T014 | P0 | [Browser rendering proof](T014.md) | Engine and Multiplayer | Explicitly released isolated spike scope | DRAFT |
| T015 | P0 | [Browser multiplayer transport proof](T015.md) | Engine and Multiplayer | T014 rendering proof accepted; approved temporary transport scope | DRAFT |
| T016 | P0 subset | [Browser toolchain and compilation bootstrap](T016.md) | Engine & Multiplayer / 01a1b92b-53f9-7132-aeb9-72b637ac3a90 | D003 approved experimental subset; independent prerequisites | ACCEPTED via T026 |
| T017 | P0 subset | [Guarded browser frame loop and input lifecycle](T017.md) | player combat / 01a1b92b-cdb9-7202-ac82-dadb42d64f5e | D003 approved experimental subset; independent prerequisites | SUBMITTED / Wasm pending |
| T018 | P0 subset | [Browser bootstrap asset inventory and deterministic manifest](T018.md) | World/Match-Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf | D003 approved experimental subset; independent prerequisites | ACCEPTED |
| T019 | P0 subset | [Loopback browser preflight serving and smoke harness](T019.md) | QA/Performance / 01a1b92d-28be-7110-9ac6-7ae01476c117 | D003 approved experimental subset; independent prerequisites | ACCEPTED |
| T020 | P0 subset | [Browser and native service separation plan](T020.md) | AI-Director / 01a1b92c-689a-71c1-820b-f1062dd0a82b | D003 approved experimental subset; independent prerequisites | ACCEPTED |
| T021 | P0 follow-up | [Experimental browser transport design and real-server proof](T021.md) | Engine & Multiplayer | T014/T020 and approved experimental transport boundary | DRAFT / BLOCKED |
| T022 | P0 subset | [Pinned SDK acquisition and inspect-first setup plan](T022.md) | Engine & Multiplayer | Reviewed T016 partial; D004 acquisition inspection only | ACCEPTED |
| T023 | P0 subset | [Selected-map and startup dependency closure inventory](T023.md) | World/Match-Systems | T018 ACCEPTED; map/profile fixed | ACCEPTED |
| T024 | P0 subset | [Browser WebGL capability diagnostic](T024.md) | QA/Performance | T019 ACCEPTED; diagnostic fixture only | ACCEPTED |
| T025 | P0 subset | [Bounded offline local authentication completion](T025.md) | AI-Director | T020 ACCEPTED; offline adapter boundary fixed | ACCEPTED via T029 |

| T026 | P0 subset | [Install inspected local SDK and compile real engine objects](T026.md) | Engine & Multiplayer | D005 reviewed prerequisite subset | ACCEPTED scope / D006 |
| T027 | P0 subset | [Original minimal browser map and bootstrap pack](T027.md) | World/Match-Systems | D005 reviewed prerequisite subset | ACCEPTED / D006 pack |
| T028 | P0 subset | [Minimal browser startup and real-game diagnostic state](T028.md) | player combat | D005 reviewed prerequisite subset | ACCEPTED scope / D006 |
| T029 | P0 subset | [Finish offline auth failure and remove browser blocking services](T029.md) | AI-Director | D005 reviewed prerequisite subset | ACCEPTED scope / D006 |
| T030 | P0 subset | [Actual browser game observer and integration harness](T030.md) | QA/Performance | D005 reviewed prerequisite subset | SUBMITTED / real run pending |

## Release and amendments

The lead fills assignment, base state, exact revisions, file allowlist and execution scope before changing a ticket to RELEASED. A phase cannot be skipped through a ticket. Interface proposals are not binding until the lead records approval. Worker questions and completion notes do not change this register.

T013 is deliberately deferred: its placement in final acceptance reserves the requirement, not an instruction to design it now. Its implementation phase/dependencies will be determined in the separate owner/lead discussion.

## First wave integration ownership

T016 owns browser build tooling/platform headers; T017 owns main.cpp only; T018 owns asset inventory/manifest tools; T019 owns loopback QA tooling; T020 is a read-only source separation plan. Source hashes and pre-existing changes are recorded in notes/decisions/D003-source-baseline.json. Every worker must preserve other owners' edits. The lead reviews all output before accepting a ticket or releasing integrated T014/T015 work.

D005 status supersedes the earlier register summary: T022-T024 accepted within their scopes; T016 blocked; T017/T025 partial and followed up by released T026-T030. Full browser/MVP completion remains unproven.

## D006 authoritative review and dispatch

T016/T025/T026/T028/T029 ACCEPTED within source/helper/target-object scope. T027 remains RELEASED for original sky closure. T017 and T030 integrated runtime evidence remain pending (T030 SUBMITTED infrastructure). T031 revision 0.6 RELEASED to Engine for the real full-client compile/link; final pack mount requires accepted sky-closed identity. T033 revision 0.6 RELEASED to AI-Director for independent real native server build only. D006 and its baseline pin exact scope. No running-game, multiplayer, full P0 or MVP acceptance.

| ID | Phase | Work | Assignee | Release basis | Status |
| --- | --- | --- | --- | --- | --- |
| T031 | P0 subset | [Full real browser client link](T031.md) | Engine & Multiplayer | T026/T028/T029 accepted; D006 | RELEASED 0.6 |
| T033 | P0 subset | [Real native dedicated-server build](T033.md) | AI-Director | T020/T025/T029 accepted; D006 | RELEASED 0.6 |

D006-pack-acceptance supersedes the pending pack status above: T027 is ACCEPTED structurally; T031 final preload is cleared for its exact stable pack identity.

T032 revision 0.7 RELEASED to World/Match-Systems: [original audio cue pack](T032.md), governed by D007; isolated from accepted T027 assets/current browser build.

D008: T034 revision 0.8 RELEASED to Player for measured browser GL link fixes. T031 remains RELEASED with exact tools.h native arm64 debug-trap addendum. T033 waits only for stable header before repeating native debug; release server link is measured but not accepted yet.

T035 revision 0.8 RELEASED to QA: notes-only real-browser transport boundary/acceptance proposal; T030 real-build run takes priority when artifact pins arrive. No T021 implementation release.

D007-audio-acceptance: T032 ACCEPTED as original PCM data; actual engine/browser audio remains NOT RUN.

T034 ACCEPTED as scoped native-preserving source/real-object compatibility fixes. Stable hashes: D008-gl-fixes-acceptance.json. T031 all-unit rebuild and final link proceed; no browser render acceptance yet.

D009: T033 ACCEPTED for actual arm64 native release/debug builds and inspection only. T031 safe profile clarified with required explicit GL_UNSAFE_OPTS=0; final link remains RELEASED.

T036 revision1.0 RELEASED to AI-Director: bounded actual native server startup, exact accepted original map/binary, isolated cwd and loopback only under D010. No client/multiplayer acceptance.

D012: first actual browser run FAILS startup signature mismatch, zero frames. T037 RELEASED to QA for bounded trace evidence capture; T038 RELEASED to Player for concrete browser setfont ABI registration fix. No runtime pass.

D013: T031 ACCEPTED as actual compile/link/packaging only, D011 metadata reconciled without runtime changes. T035 ACCEPTED as proposal only. T036 graceful shutdown unresolved; T037/T038 continue. No rendering, transport or MVP acceptance.

D014: T039 revision1.2 RELEASED to AI-Director for contained copied SDL2/hidapi ad-hoc signing and new native release/debug builds, preserving original dependency and evidence. T036 runtime remains partial; no new launch yet.

D015: T037/T038 ACCEPTED as evidence/source/object scope. T040 revision1.3 RELEASED to Engine for same-profile actual integrated browser rebuild and future MAIN-accepted fixes, with each attempt/pin retained. No corrected runtime pass yet.

D018: T041 revision1.5 RELEASED to World for independent original MD3 survivor/pistol/rifle data; no current pack overlay, camera/hitbox/gameplay or runtime acceptance.

D019: exact same-Wasm D017 stack maps heap trap during map configuration load. T042 revision1.6 RELEASED to Player for concrete browser world/entity buffer ownership defect; no speculative global allocator/profile fix.

D020: T039 ACCEPTED copied-signature/build integrity; T036 SUBMITTED partial runtime/shutdown failure. T043 revision1.7 RELEASED to AI for exact signed-copy bounded startup comparison; no source fixes or multiplayer.

T044 revision1.6 RELEASED to QA for static installed WS dependency/initialization/options/license inspection only, independent of priority actual-map startup. No import/execution/network implementation.

D021: T042 ACCEPTED source/actual object/valid-map ownership helper; optional ASan timed out, no sanitizer pass. T040 same-profile rebuild authorized for exact stable worldio hash; actual corrected run pending. Separate RLE hardening question retained.

D023: signed-copy T043 remains SUBMITTED partial due SIGSEGV/static teardown with live workers. T045 revision1.8 RELEASED to AI for real native cooperative stop/wake/join/logger ordering and new builds; no runtime launch until pinned.

D024: D022 first real running-map/WASD/capture progress; strict test still FAIL on GPU diagnostics. T046 RELEASED to Player for precise WebGL1 targeting/strip compatibility; T047 RELEASED to QA for exact SDK notice attribution plus stronger real GPU-error gate and optional actual canvas image. No correct-render/full P0 acceptance.

D025: T044 ACCEPTED static inspection; exact parser-limit meanings retained, no bundled import approval. T048 revision2.0 RELEASED to Engine for exact official standalone ws8.21.0 metadata/archive acquisition/inspection ONLY; no install/import/runtime, current graphics rebuild priority.

D026: T041 ACCEPTED original model data/structural scope, actual engine/render NOT RUN. T049 revision2.1 RELEASED to World for NEW deterministic original79-file media stage and exact five model config permissions; current map/build unchanged.

D027: QA chat direct human hold respected; T047 revision2.2 reassigned exclusively to MAIN for already approved observer graphics/capture integration. Other workers continue; root goal remains active.

T047 ACCEPTED observer implementation/source tests by MAIN (14 focused cases plus exact prior-source reconstruction). QA chat remains held; actual corrected graphics run pending accepted T046 and new T040 pins.

D028: T046 ACCEPTED source/object scope. Current T045 browser/native-client token preservation/target hashes checked for browser integration only, native lifecycle acceptance still pending. T040 graphics rebuild released on exact D028 inputs; MAIN runs next QA under direct QA-chat hold.

D029: T048 source inspection/T049 media assembly ACCEPTED within scopes. T050 revision2.3 RELEASED to Engine for exact vendored WS package + bounded import/dependency-only loopback self-test, AFTER priority graphics bundle. No game transport implementation/acceptance.

D030: T045 ACCEPTED source/build/11 real-thread helper cases only. T051 revision2.4 RELEASED to AI for sequential bounded real release/debug SIGINT lifecycle tests on exact accepted binaries; actual shutdown acceptance still pending.

## D033 coordination review / prerequisite2.5

T050 and T051 ACCEPTED with preserved caveats in D033. T052 RELEASED to player (real gesture audio source); T053 RELEASED to World (separate audio-enabled pack); T054 RELEASED to AI (implementation-ready transport proposal). T040 remains frozen integration; QA direct human hold remains. No full T014/P0/MVP acceptance.

D034/T055 RELEASED to MAIN for actual normal-input geometry/resolution evidence. D035/T056 RELEASED to Engine for responsive shell only; runtime output remains frozen until next accepted-input integration.

D036: T053 DATA and T055 normal-input original geometry accepted. Audio runtime/full focus lifecycle/performance/network and P0 remain unaccepted.

D037: T056 shell source/fixture accepted. T057 RELEASED Engine for fixed loopback gateway component under approved EXPERIMENTAL_TRANSPORT0.1. No actual game/production transport acceptance.

D039: T054 proposal ACCEPTED. T058 RELEASED AI-Director for disjoint actual browser ENet C/JS platform under EXPERIMENTAL_BROWSER_BACKEND0.1. Existing game lifecycle/main remain untouched.

D040: T052 audio source/object/helper ACCEPTED, runtime pending. T059 RELEASED Player for request-specific pointer-lock Promise denial recovery; current runtime output frozen.

D041: T060 RELEASED World for new isolated audio-profile build tooling PREPARATION only. Actual compile/link requires future accepted stable T059 source and MAIN pins/execution release; legacy out untouched.

D042: T059 amended3.1 for exact unverified audio cleanup correction, actual context-state diagnostic and original pointer recovery, fresh evidence only. T052 acceptance historical; new combined source pending T059. T060 tooling stays preparation-only.

D043: gateway/platform contracts0.2 and T057/T0583.2 fix standard browser offer versus negotiated compression and distinguish real browser close observation from logical cleanup. D044: T0603.1 confined exact SDK alias policy; preparation only.

D045: T0573.2 gateway component ACCEPTED. T061 RELEASED Engine for remote-only client/parser/world-update source under approved NETWORK_CLIENT0.1; no main edit/full game link/runtime yet.

D046 resolves existing SDK HTML-minifier alias for T0603.2 preparation. Compiler execution remains unreleased.

D047: T0583.2 platform and T0593.1 source/object/helpers ACCEPTED. D048: T061/client0.2 genuine spectator-first spawn control. D049: T062 RELEASED Player for network-only main wiring/clock/diagnostics, no full build/runtime.

D050: T063 RELEASED AI for actual single browser ENet core -> gateway -> accepted native-c1 component, bounded freshsandbox. Not complete game/two-player proof; no pending client/main sources executed.

D051: T0603.2 preparation ACCEPTED, compiler execution not released. T064 RELEASED World for separate8FFA/rev2 network pack preserving geometry. T061/client contract3.7/0.3 expects newrev2 only for future game profile; original offline/T063 map staysrev1.

D052: T0633.8 exact native sound.h browser-only guarded delta resolution; first preflight launched no nativechild, allotherdeps/binary/runtime unchanged.

D053: T062 main SOURCE accepted. T065 RELEASED Player for canonical original model preload/actual player-path bindings only, network guard; no camera/gameplay/actual render acceptance.

D054: T063 actualnative ENet transport component and T064revision2/8FFA DATA accepted. T066 RELEASED World shared audio/network build PREPARATION; T067 RELEASED AI genuine two-C++-client/native-c2 observer PREPARATION. No full app/c2execution until finalsource/artifact pins/release.

D055: T0613.7 network lifecycle source and T0653.9 canonical model source ACCEPTED at component scope. T068 RELEASED Engine static integration review; T069 RELEASED Player media/input verification preparation. T066/T067 remain active. Full link/game runtime and MVP remain unaccepted.

D056: T002 revision1.0 READY for Engine after T068 review, proposal-only. Full authority/interface freeze remains pending MAIN approval; no gameplay implementation released.

D057: T0674.1 clarifies genuine empty-server automatic native spawn and bounded cross-getter transition timing; no fake request or actual execution release. D058: T0664.0 shared tooling PREPARATION ACCEPTED after independent34-test PASS and source identity review.

D059: T0704.2 RELEASED World for one actual fully pinned network client build into separate network-out; no browser/game execution or source fixes.

D060: T069 notes-only media/input preparation ACCEPTED; currently unavailable runtime subcases remain NOT RUN, not waived. T0714.3 RELEASED Player for concrete P1 camera/control/weapon proposal to MAIN; no gameplay code authorized.

D061: T068 static review ACCEPTED; T002revision1.0 RELEASED Engine for shared authoritative simulation proposal only, awaiting MAIN interface/parameter approval.

D062: T070 SUBMITTED (full link established; external verifier failed); T0724.4 RELEASED World for additive read-only published verification with all original input/protection and exact output gates preserved. No rebuild/runtime.

D063: T0674.2 preparation clarifies actual T070/T072 dependencies, early owned-browser cleanup and exact empty204 favicon route; all runtime permission remains pending.

D064: T072 additive verifier and T070 full network BUILD ACCEPTED after independent19fixture tests and actual read-only complete verification. Original verifier exit2 retained; no browser/game/P0 acceptance. Artifact identities in D064-accepted-network-artifact.json.

D065: T0734.6 RELEASED World for verified developer workflow and concrete clean-checkout gap documentation; no build/runtime/source changes.

D066: T071 proposal delivery ACCEPTED without adopting values; T0744.7 RELEASED Player for isolated source-derived MD3 position-output regression, production/source/artifact unchanged.

D067: T0674.2 observer PREPARATION ACCEPTED after independent17fixture tests/JSsyntax/source review. D068: T0754.8 RELEASED AI for one actual fulltwo-client native-game baseline T075-1, complete MAIN pins cbfa1085f93522064d795bae95b62f51284b1a20951db17392541bb0a65cbc19,26592 files/10trees/48aliases; no gameplay result yet.

D069: T073 developer workflow/gap documentation ACCEPTED; T0764.9 RELEASED World for compact Blackwood/squad/anchor proposal and bounded read-only measurements, no asset or gameplay implementation.

D070: T075 one actual two-full-client baseline FAILED at observer raw1047 guard, initial-vs-inter-frame ambiguity unproven; cleanup supplemented PASS. T0775.0 RELEASED AI observer correction PREPARATION only, historical driver/evidence preserved; no actual retry yet.

D071: T074 source-derived MD3 position-output BUG_REPRODUCED accepted, production NOT FIXED/real rendering NOT RUN; later explicit header/source/build lease required.

D072: T002 frozen full proposal SUBMITTED awaiting full freeze; approved isolated SHARED_NUMERIC_FOUNDATION0.1 and T0785.1 RELEASED Engine for actual portable checked math/native+Wasm oracle verification, no gameplay or P0 acceptance.

D073: T077 corrected observer preparation ACCEPTED after independent25Python/JSsyntax/7extracted-JS classifier tests. D074: T0795.2 RELEASED AI one actual corrected fulltwo-client baseline T079-1, complete pins e8d76c7d6efea2abbfa93f38ff789d83b59f38ec2e1bebfd6c9353fa71687494 (26610files/10trees/48aliases); game/source/backend/limits unchanged.

D075: T076 proposal/measurement delivery ACCEPTED; approved BLACKWOOD_DATA_FOUNDATION0.1 DATA-only prerequisite and T0805.3 RELEASED World for new original128² candidate/strictQ10sidecar, no overlay/gameplay/finalmap acceptance.

D076: T079 actual fulltwo-game-client normal-loopback baseline ACCEPTED after independent native-mediated movement/cleanup verification; T078 numericSOURCE/native+Wasm94976oracle cases ACCEPTED. No authority/P0/MVP claim. T0815.4 RELEASED Player isolated full-header tagfix/genuine consumer validation; production unchanged.

D077: approved EXPERIMENTAL_IMPAIRMENT0.1/T0825.5 RELEASED AI fixed40ms-eachway/every50th-datagram-loss preparation, explicit minimal controller extension and source-T079 snapshot; no actual impairment run or baseline/game threshold change.

D078: T080 original Blackwood128² candidate DATA ACCEPTED after independent9tests/actualvalidator/122freeze checks; no runtime/nav/balance/phase acceptance.

D079: approved PORTABLE_FORMAT_FOUNDATION0.1; T0835.6 RELEASED Engine header-only envelope codec, T0845.7 RELEASED World decompressed dry-flat map decoder. Actualnative+Wasm/golden/canary/sanitizer gates; no game integration/authority/fullP0 acceptance.

D081: T081 full-header candidate and T082 impairment PREPARATION ACCEPTED in limited scopes. D080: T083/T084 toolchain questions resolved, continue released gates.

| T085 | P0 subset | [Candidate build and MD3 application plan](T085.md) | Player | T081/T073/T070/T072 accepted | RELEASED |
| T086 | P0 subset | [Actual impaired two-client game experiment](T086.md) | AI-Director | T082/T079 accepted; D082 complete pins | RELEASED |

D083: T083/T084 sanitizer gates remain incomplete; T0875.10 RELEASED World bounded installed-runtime startup diagnostics, no parser retry or waiver.

| T087 | P0 subset | [Installed sanitizer startup diagnostic](T087.md) | World/Match-Systems | Preserved T084 timeouts; D083 | RELEASED |

D084: T086 ACCEPTED actual fixed impairment native relay only; approved PLATFORM_DECISION0.1, no full P0 acceptance.

D085: T085 plan/T087 diagnostic deliveries ACCEPTED, T083/T084 SUBMITTED with required sanitizer gate incomplete. T088 Engine candidate tooling prep, T089 Player exact MD3 source fix, T090 World local matched LLVM22 startup, T0151.0 AI integrated transport report RELEASED.

| T088 | P0 subset | [Reusable candidate build tooling](T088.md) | Engine | T085/D085 approved build foundation | RELEASED |
| T089 | P0 subset | [Apply exact MD3 tag fix](T089.md) | Player | T081/T085/T086 accepted | RELEASED |
| T090 | P0 subset | [Matched LLVM sanitizer startup](T090.md) | World | T087/D085 | RELEASED |

D087: T089 source application ACCEPTED; T015 report SUBMITTED, missing T014/lifecycle proof retained. T0915.14 Player read-only metrics source/object; T0925.15 AI native candidate tooling PREPARATION RELEASED.

| T091 | P0 subset | [Browser foundation observations](T091.md) | Player | D087 approved observation contract | RELEASED |
| T092 | P0 subset | [Fresh native candidate tooling](T092.md) | AI-Director | D087 approved native build contract | RELEASED |

D089: T090 matched LLVM22 provisioning/startup ACCEPTED after independent10519entry check. T0935.16 World actual complete nativeASan+UBSan decoder corpus/negative-controls RELEASED, trusted MAIN input pins; T083/T084 still pending those results.

| T093 | P0 subset | [Actual decoder sanitizer corpora](T093.md) | World | T090 accepted/D089 source-tool pins | RELEASED |

D090: T091 read-only source/object/publisher component ACCEPTED; T088/T092 real-source observation unblocked. Approved FOUNDATION_MEASUREMENT0.1/T0945.17 Player component PREPARATION RELEASED, no actual browser run.

| T094 | P0 subset | [Foundation measurement component prep](T094.md) | Player | T091 accepted/D090 | RELEASED |

D091: T0885.18 Engine/T0925.19 AI re-released same prep ownership under candidate contracts0.2: shared source-package superset validated in full, exact structured historical preservation; no consumed-input/link exceptions.

D092: T083/T084/T093 ACCEPTED exact portable source/native+Wasm+sanitizer scope; original failures/limits retained. T0955.20 World frozen prerequisite package/stager RELEASED.

| T095 | P0 subset | [Frozen browser prerequisites](T095.md) | World | Existing SDK/cache/D092 approved package contract | RELEASED |

D093: T094 component prep ACCEPTED, actual benchmark/integration not run. T0965.21 Player source whitelist/overlay audit RELEASED for MAIN clean revision review.

| T096 | P0 subset | [Review concrete source overlay](T096.md) | Player | D093/T085/D091 source package | RELEASED |

D094: T095 World re-released5.22 under package0.2; original-cache mode question resolved by explicit new-package-only normalization.

D096: T0885.18 ACCEPTED preparation/private record schema only. T0021.1 Engine RELEASED complete P1 concrete-record/wire/seam notes; numeric rules fixed, full P0/MAIN interface approval still required before gameplay.

D097: T0975.23 Engine RELEASED narrow source-discovery correction; T088 prep historical, corrected source reviewed before clean build. T002 notes resume after T097 freeze.

| T097 | P0 subset | [Correct production source discovery](T097.md) | Engine | T088/T096 findings/D097 | RELEASED |

D098: T092 SUBMITTED pending T0985.24 AI FAT-inspection/ordinary-owned-output corrections.

| T098 | P0 subset | [Correct native inspection and owned links](T098.md) | AI-Director | T092 review/D098 | RELEASED |

D099: T096 path proposal/audit ACCEPTED after independent860-path checks; final source/content/build approval pending. T0991.0 Player RELEASED notes-only candidate-runtime admission/foundation controller proposal. T095/T097/T098 continue; QA hold unchanged.

| T099 | P0 subset | [Plan candidate runtime validation](T099.md) | Player | T096/T094 accepted; D099 | RELEASED |

D100: T092/T098 native tooling PREPARATION ACCEPTED after independent38 guarded tests/full18-file freeze check and targeted source review; actual native build not run. T1001.0 AI RELEASED source provenance reconciliation for MAIN clean-source review.

| T100 | P0 subset | [Reconcile engine source provenance](T100.md) | AI-Director | D064/D087/D090/D099/D100 | RELEASED |

D101: actual T095 archive/data independently matched; stager acceptance pending exact clean-checkout report-parent correction. T1011.0 World RELEASED after original T095 handoff/freeze; preserve archive/CREATE history, correct guard/tests and explicitly bind successor manifest to new stager.

| T101 | P0 subset | [Fix stager report parent creation](T101.md) | World | T095 data review/D101 | RELEASED |

D102: T100 source-provenance audit ACCEPTED after independent154-source/52-reference checks; final reviewed revision/build pending. T1021.0 AI RELEASED fixed native external prerequisite identity collection, no compiler/tool execution.

| T102 | P0 subset | [Collect native external inputs](T102.md) | AI-Director | T100/T098 accepted; D102 | RELEASED |

D103: T099 planning delivery ACCEPTED; proposed admission/runtime schemas/budgets remain unapproved. Approved BROWSER_CAPABILITY_PROBE0.1/T1031.0 Player preparation for fixed local cache/blocking/GPU facts; no actual browser/service execution.

| T103 | P0 subset | [Prepare browser capability probe](T103.md) | Player | T099 accepted/D103 probe contract | RELEASED |

D104: T097 corrected discovery source/preparation ACCEPTED after independent six regressions/full12-file freeze and source-scope check; Engine resumes T002 notes. T095 original44-file freeze/data verified, delivery SUBMITTED pending T101 corrected stager review; actual builds/staging not run.

D105: T102 external native identity collection ACCEPTED after independent912-file/seven-link/15-reference verification. MAIN source inventory reconciled; final T101/clean-root/source revision and actual builds pending.

D106: T095/T101 package/corrected stager/successor metadata ACCEPTED. MAIN authorized explicit887-path local source commit/fresh no-hardlink clone and one bounded DATA-only prerequisite stage there; compiler/build/runtime gates remain separate.
