# Movement declaration foundation

Revision:0.1. Status: APPROVED MAIN D303 exact NEW HEADERS ONLY before complete P0/G2. Individually named T189 materializes three declarations. No movement body, validator/generator, codec, test/compiler/runtime or full MotionState/M4 behavior adoption. D284/D295 construction authority remains separate; owner horizontal selector stays pending.

## Sole value home: p1_motion_state.h

MotionState's SOLE complete definition is NEW source/outbreak/p1_motion_state.h. H/T183's proposed p1_types.h home is superseded ONLY for this record. Existing accepted p1_types.h and all other source/headers remain unchanged. Shot's existing forward declaration refers to this type; it is not another definition. Exact file:

```cpp
#ifndef OUTBREAK_P1_MOTION_STATE_H
#define OUTBREAK_P1_MOTION_STATE_H
#include "p1_types.h"
namespace ob {
struct MotionState {
 Pos3 foot; Vel3 velocity; int16_t position_remainder[3];
 uint8_t acceleration_remainder,gravity_remainder; Aim aim;
 Stance stance_from,stance_target; uint8_t stance_elapsed,grounded;
 int32_t stance_start_height_q10,stance_start_eye_q10,height_q10,eye_q10;
 uint32_t last_jump_request; uint16_t flags;
};
}
#endif
```

Both retained stance origins are explicit. The reviewed native envelope is64 bytes/align4, required<=64/align<=8; this header has not been compiled. No packing/field omission or native-memory wire serialization. Future exact field validation, canonical inactive/completed/transition forms and paired generator are still distinct adoption/implementation gates; header materialization cannot produce a valid living actor by itself. Motion60/Own204/baseline1144 encoding remains a reviewed proposal requiring future explicit codec freeze and real byte tests.

## Sole public declaration: p1_motion.h

Exact NEW source/outbreak/p1_motion.h:

```cpp
#ifndef OUTBREAK_P1_MOTION_H
#define OUTBREAK_P1_MOTION_H
#include "p1_geometry.h"
#include "p1_input.h"
#include "p1_motion_state.h"
namespace ob {
struct MoveResult { MotionState motion; uint8_t contacts,pair_passes; };
bool move_one(const CollisionView &,const RulesP1 &,const AngleTables &,
              ActorRef self,const MotionState &,const InputFrame &,
              uint32_t selected_jump_request,
              void *scratch,uint32_t scratch_bytes,MoveResult &,Fault &);
}
#endif
```

This is the sole successor to the unadopted H signature. Explicit self/table/scratch supply identity/resources, never a rate/query/dt/eligibility bypass. Selected jump is request selection, not certified action acceptance. Future implementation must specify complete typed/caller/freshness/scratch lifetime/alias/Fault/proxy and query semantics; none is inferred from a declaration. MoveResult reviewed envelope68/align4<=80/align<=8 remains future compiler proof. Existing InputFrame stays p1_input.h; camera/shot records stay their actual headers. No old overload/fallback.

## Sole PRIVATE joint seam: p1_motion_private.h

Exact NEW source/outbreak/p1_motion_private.h, for future specifically leased motion/store/test consumers only:

```cpp
#ifndef OUTBREAK_P1_MOTION_PRIVATE_H
#define OUTBREAK_P1_MOTION_PRIVATE_H
#include "p1_motion.h"
namespace ob { namespace motion_private {
enum class InputUse:uint8_t { Fresh=1,Held=2,Neutral=3 };
struct TickActorIn {
 ActorRef actor;
 const MotionState *start;
 const InputFrame *selected;
 Tick fresh_input_tick;
 uint32_t jump_request,jump_input_sequence;
 InputUse input_use;
 uint8_t reloading,switching,fire_requested;
};
struct TickIn {
 Tick tick;
 const CollisionView *view;
 const RulesP1 *rules;
 const AngleTables *angles;
 const TickActorIn *actors;
 uint8_t count;
};
struct TickOut {
 ActorRef actor[8];
 MoveResult result[8];
 Reject jump_reason[8];
 uint8_t jump_outcome[8];
 uint8_t count;
};
bool move_joint(const TickIn &,void *scratch,uint32_t scratch_bytes,
                TickOut &,Fault &);
} }
#endif
```

No SimStore/World/advance_tick definition, export, wire record, test hook or implementation is created. Full canonical roster/current-source/freshness/eligibility validation and pure candidate versus real commit remain later exact behavioral contracts. Proposed TickActorIn<=48/TickIn<=48/TickOut<=640 and T180786432/768/query/caller capacities are unchanged, unmeasured until real consumers compile/verify them. Namespace privacy does not grant adapter/presentation/network call authority. No eight independent public moves replace joint server movement.

Only T189 may write these exact NEW headers/own NEW notes; every existing file read-only. No body/build/include consumer/test/fixture/oracle/generator/compiler/SDK/FFI/probe/runtime/network/Git/dependency/worker effect. Literal content/include/sole-home inspection only; compile/ABI/runtime NOT RUN. Full accepted G2/current G1 regression, typed/M4/Fault/alias/prediction/encoding/owner choice and named implementation/evidence/tick/browser/human gates remain; Player/nativeT167/QA/T149 holds unchanged.
