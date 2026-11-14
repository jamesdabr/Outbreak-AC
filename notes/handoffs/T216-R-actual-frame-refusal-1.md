# T216 actual operation — both-target geometry-frame refusal

Worker: World & Match Systems / 01a1b92c-db5c-7a10-a0e4-46e1f5a092cf. Authority: D363 / T216 1.0 / G2_FOUNDATION 1.3 and MAIN-T216-exact-dispatch-1.md. ONE actual invocation consumed; original exit 1 observed. FAILED_OR_INCOMPLETE. No retry, repair, source change, additional child, alternate path or new attempt was performed. Attempt-2 remains occupied and preserved. World stops pending MAIN disposition; no R/Q acceptance is claimed.

## Exact dispatch and original terminal

Before invocation, read the full new caller and caller/plan/effect review. Standard shasum confirmed caller 18612 bytes / SHA256 bea5d109ee39f6fcadd18d46b08f0af6cc5b6264fa2cfd3f5513831a66d322e9, review 1dcd0dfb8984b80363c7a69b9ca33809535216a20461103680cdbc84d537b20e and preflight be5033c5f57e5677f1979146a8d5b2d45671cca3f4dbb00af38a3598c991a700. Accepted preparation-4 manifest cf952add045d4ddc9e4f307a34acbc23946d3bf555819bbd8ef7b0c852b6c078 and plan 453f13c7d559aafaf8d76ce77491b880befc0502c8c4522fcbe6b89e386096fb matched. Read-only ls confirmed absent R attempt-2 and Q preparation-1/attempt-1. No preliminary parser/import/helper/version/compiler/probe/rehearsal ran.

Exact entire command, zero extra argv:

```text
/usr/bin/env -i PATH=/usr/bin:/bin LANG=C LC_ALL=C PYTHONDONTWRITEBYTECODE=1 /Library/Frameworks/Python.framework/Versions/3.11/bin/python3.11 -I -B /Users/jd1/code/apps/outbreak/notes/proposals/T216-R-actual-caller-1.py
```

exec_command options: workdir=/Users/jd1/code/apps/outbreak, login=false, tty=true, yield_time_ms=1000, max_output_tokens=8192. The new caller bootstrapped the pinned R actual once. No old caller was invoked.

Initial tool object, retained as T216_original_tool_first:

```json
{"chunk_id":"1ab64b","wall_time_seconds":1.002624791,"session_id":50775,"original_token_count":0,"output":""}
```

ONE empty-input write_stdin on SAME original session 50775, yield_time_ms=1000, max_output_tokens=8192, returned terminal. Retained as T216_original_tool_poll1:

```json
{"chunk_id":"a22e1f","wall_time_seconds":0.617365709,"exit_code":1,"original_token_count":181,"output":"{\"elapsed_seconds\": 8.334259583964013, \"error_type\": \"ValueError\", \"message\": \"complete both-target core/run source-bound frame proof refused: [{\\\"root\\\": \\\"_ZN2ob12sweep_sphereERKNS_13CollisionViewERKNS_6SphereERKNS_4Pos3EtRNS_11TraceResultERNS_5FaultE\\\", \\\"target\\\": \\\"native\\\", \\\"violations\\\": [{\\\"bytes_or_count\\\": 1744, \\\"cap\\\": 1024, \\\"component\\\": \\\"geometry\\\"}]}, {\\\"root\\\": \\\"_ZN2ob13sweep_capsuleERKNS_13CollisionViewERKNS_7CapsuleERKNS_4Pos3EtNS_8ActorRefERNS_11TraceResultERNS_5FaultE\\\", \\\"target\\\": \\\"native\\\", \\\"violations\\\": [{\\\"bytes_or_count\\\": 1776, \\\"cap\\\": 1024, \\\"component\\\": \\\"geometry\\\"}]}, {\\\"root\\\": \\\"_Z\", \"no_retry\": true, \"schema\": \"T216_ORIGINAL_CALLER_1\", \"status\": \"FAILED_OR_INCOMPLETE\"}\r\n"}
```

Original exit 1 was observed without timeout/restart/signal/interrupt/reset. Caller elapsed 8.334259583964013 seconds; source elapsed 8.2802275409922 seconds; tool per-return wall values above are separate observations. Original 300-second budget was not exhausted or reset. Caller message is intentionally truncated; failure.json primary message is also bounded. The full refusal facts are in frame-analysis-refusal.json.

## Retained failure prefix

Owned root: tests/outbreak/geometry/G2/regression-G1/attempt-2. All original files, private SDK/cache, inputs, normal and diagnostic objects/assembly/dependencies/SU records, binaries and logs remain intact.

| Artifact | Bytes | SHA256 |
| --- | ---: | --- |
| FAILURE | 56 | 1c4929c3a0c0613f14d24f22691b743e80eb97f432efe155ef4702b8fdd0cd5d |
| failure.json | 59969 | dbe4fcb87ffa31715a48bd79de6dc96a15a3f032e44e296fb4de36fdd1a53869 |
| frame-analysis-refusal.json | 568821 | db8123ab44a5571625088a5eda8265d4059181abf39b6fe2e1ca33fe7f5c01cb |
| actual-dependencies.json | 603103 | df211704bd5a3002fec969d8fe5c753b5f22a0ec25a38d77c6683794e7ecd630 |
| inspected-plan.json | 37651 | 8ba73171e2911c29a7182ed53c582ba7e4835f11d9847c1b4f715ce484bade1a |
| geometry-native | 299168 | 08577a7fcd2a954206cf9ed95e703f842abfe980f38fdc3b5eba6f939e5fd976 |
| geometry.wasm | 310765 | 18d0fc8736a9457ce47b4d28960a6c24c40ad03e21b9ac5ba99b9223c889880b |
| setup.bin | 915564 | b96adfac57cc4a3b51768d86a9a92206d92199ea9359ca08c9b4e1f2bb2064a9 |
| corpus.bin | 2709120 | d6f1a202961c82cccde81a003aca448aa54942c5f077055907482d46b0d6a642 |
| expected.bin | 2686976 | 580ead76672dce81f30b50cee37b70f59a87c62008e2d9b61a16803aa55d3ad5 |

FAILURE is exactly `T187 R incomplete/failed actual attempt; do not consume` plus newline. No manifest.json, processes.json, frame-analysis.json, review-ready-owned-graph.json, native.responses.bin or wasm.responses.bin exists. Final graph/terminal/protection publication was NOT REACHED; no substitute was generated. The binary hashes equal A1's hashes, but these binaries were freshly compiled and linked by this operation, not reused.

## Executed prefix and complete refusal

Exactly the 26 prepared compile/diagnostic/link/version commands ran. Every final receipt in failure.json reports ok=true, reaped=true, owned_group_observed_quiescent=true, retention_complete=true and returncode=0. All 26 record D260 POST_REAP_ABSENT resolution. Last aggregate_output_seen and aggregate_output_retained are 514 bytes. These are successful supervised build-command receipts, not successful whole-operation terminal or functional proof. The two real target arrays 26/27 were NOT executed; no real 16384-row response stream or comparison exists.

The reviewed private SDK copy and fixed real Darwin waitid/ctypes/libSystem supervision were reached within this operation. Exact copy checks returned before children. Later full SDK/dependency/history/protection postflight was NOT REACHED.

Source-role binding advanced beyond A1's missing-template refusal. Complete both-target core/run frame analysis gathered the following 12 violations. Every entry is the **geometry chain component**, cap **1024 bytes**:

| Entry point | Native bytes | Wasm bytes |
| --- | ---: | ---: |
| sweep_sphere | 1744 | 1524 |
| sweep_capsule | 1776 | 1528 |
| sweep_capsule_world_rational | 1728 | 1596 |
| headroom | 1760 | 1520 |
| trace_ray | 1728 | 1540 |
| run | 1776 | 1596 |

Exact mangled roots and full profiles/source roles/normal callee/owner/local facts are retained in frame-analysis-refusal.json. `run` propagates the maximum geometry chain; this report does not identify a caller-cap violation. No cap change, normal-body exemption, owner waiver or source repair was attempted. All-root frame acceptance failed; target execution correctly remained blocked. Compile/link success is not current-source G1 regression or G2 moving-query acceptance.

## Postflight observations and limits

The caller reached actual after all 51 complete preflight descriptor/hash checks. After original terminal, ordinary shasum independently rechecked all 51 pinned file hashes: 13 sources, 18 current controls, canonical Python, 12 accepted preparation-4 files and seven authority/evidence files. Every SHA matched the caller inventory and MAIN preflight. Production p1_geometry.cpp remains b5b842a0f745205e877f765a61a0dcc6a5b5f53a0aebe0f99ee2e9cd07c4c804; Q verify remains 9876c59579468df28241786f23a69f2a0985b05824bbc7a8fafcb7b59c9f386d; R verify remains 398b1eb0f548df4e98ed75cebdcfb64f61064df9170d2b7550d8cd42c94ac2cf. No source or authority write occurred.

Caller post-return all-51 descriptor checks were NOT REACHED because actual raised. Complete source dependency/SDK/header/tool/G0/history/preparation postflight, final owned graph and successful terminal were also NOT REACHED. Own post-terminal hash equality is not descriptor/topology/SDK/history proof. MAIN must independently check protected roles and full graphs against its original preflight; all protected roles remain frozen pending that disposition.

Observed: exact once-only dispatch, original terminal exit 1, 26 successful supervised build commands, full retained frame refusal and bounded read-only postflight. Failed: whole R actual at geometry-chain frame caps. Not run or qualified: both target responses, real regression, complete final postflight, Q/camera/browser/game/phase/human/MVP acceptance. No further operation or held-scope work is authorized by this failure handoff.
