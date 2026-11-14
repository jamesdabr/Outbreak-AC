# Native arm64 debug builds hit the x86 ASSERT instruction

- Author / worker: AI-Director
- Ticket and revision: T033 / 0.6 RELEASED
- Phase and contract revision: P0/BROWSER_FOUNDATION/GOVERNANCE 0.5 plus approved D006 addendum 0.6
- Exact clause or interface affected: T033 criteria 3 and 4, true native arm64 debug executable with source read-only
- Status: OPEN (lead resolution is recorded separately)

## Question

Please release an architecture-correct native ASSERT fix to the exclusive owner of source/src/tools.h, then authorize T033's debug rebuild against the new pinned input. T033 cannot edit this header or suppress assertions.

## Evidence and impact

Actual Apple clang 17 arm64 code generation fails for all eight standalone C++ debug units. Example web/server/out/debug/crypto.compile.log points to crypto.cpp:127 and tools.h:19: `asm("int $3")`, with `error: unrecognized instruction mnemonic`. The browser branch uses __builtin_trap(), but native GNU-compatible compilers always select the x86 assembly even on Apple arm64. Prior syntax-only native checks did not assemble it.

All eight release C++ units and fresh eight ENet C units compile; the real release server links successfully. All eight debug ENet C units compile; no debug executable is claimed. No source file was changed. Complete commands/input/dependency hashes are in web/server/build-report.json.

## Options for owner and lead

Recommended: retain the x86 behavior where desired and add a non-x86 Clang/GCC __builtin_trap() branch, preserving a real terminating assertion. Alternatively use __builtin_trap for GNU-compatible native compilers if approved. Either is a source behavior decision for the header owner, outside this build-only allowlist.

Do not define __EMSCRIPTEN__ for a native server, remove _DEBUG, override ASSERT to success, build an unintended x86 target or suppress assembler errors to claim debug acceptance.

## Work paused

The arm64 debug C++ code-generation/link step is blocked pending the narrow released source fix. Independent release build, dependency/binary inspection, metadata verification and later loopback-launch proposal are completed/continuing. No server launch is authorized or requested here.
