# T214 exact unsupported source initializer forms remain closed

- Author / worker: Engine & Multiplayer /01a1b92b-53f9-7132-aeb9-72b637ac3a90.
- Ticket and revision: T2141.0 / D358 SOURCE CORRECTION ONLY.
- Phase and contract revision: MOTION_RECORD_FOUNDATION0.4.
- Exact clause or interface affected: D358 source-qualified initializer value before
  NORMAL OBJECT/final DATA; prior T208 question4.
- Status: OPEN (lead resolution is recorded separately).

## Question

The correction selects the explicitly allowed fail-closed option: exact complete
static uint8_t/uint32_t zero declarations only. zero=false never accepts arbitrary
normal bytes. Unqualified nonzero/implicit/literal/aggregate/pointer/synthetic
source storage refuses before admission. Which separately reviewed bounded source
grammar and exact source/evidence roles, if any, should later support required
additional forms?

## Evidence and impact

Current wrapper remains read-only and includes the nonzero MR01 string literal,
static Guarded aggregates, ByteView and other nonselected forms. The correction
does not assume these are zero, treat producer agreement as expected source
values, or skip final DATA roles. Actual compilation/emitter discovery is not
authorized. Any eventual required role outside MR-SOURCE-ZERO-1 refuses; this
source delivery is not a completed executable/preparation clearance.

Native .comm/COMMON/unknown normal storage is refused; selected .zerofill/.lcomm
must prove actual defined normal zero-fill section/whole extent/alignment and
source/linked relations. Host graph/native auxiliary/DWARF/compiler/save-temp
questions from T208 remain OPEN and unamended.

All five focused storage fixtures use the selected grammar and valid complete
normal premises except their exact named mutation; S01 deliberately supplies
the source-value1/normal-byte2 unqualified nonzero discriminator and must refuse.
No weaker or vacuous replacement fixture, tool/probe/import or extra leaf is used.

## Options for owner and lead

Retain these required forms refused while reviewing the concrete D358 fixes; or
supply exact inert primary/source evidence and separately release the affected
additional source grammar. A MAIN label/hash alone is not source qualification.
No count/budget/flag/ABI/gate amendment is proposed.

## Work paused

All parser/import/helper/control/test/preparation/compiler/probe/FFI/load/runtime
activity remains outside T214 authority. Independent authorized source, exact
focus definitions, schemas, diffs and handoff are completed without those effects.
