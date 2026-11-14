# Pure shot declaration foundation

Revision:0.1. Status: APPROVED MAIN D294 INTERFACE HEADER ONLY prerequisite before complete P0. Only individually RELEASED T185 may materialize the exact declaration header below. No shot definition/consumer, test/data/oracle/compiler/runtime or gameplay integration is released.

## Exact sole home

NEW source/outbreak/p1_shot.h is the SOLE home of ShotKind, AcceptedShot, SpreadDraw, ShotResolution and resolve_shot. Reuse actual p1_camera.h/p1_geometry.h/p1_rules.h/p1_types.h value homes; no duplicate HitZone/CameraPose/InputFrame or World accessor. Exact header:

```cpp
#ifndef OUTBREAK_P1_SHOT_H
#define OUTBREAK_P1_SHOT_H
#include "p1_camera.h"
namespace ob {
struct MotionState;
enum class ShotKind:uint8_t { Miss=0,Blocked=1,Hit=2 };
struct AcceptedShot {
 ActorRef source; Weapon weapon; uint32_t ordinal,cause_request; Aim aim;
};
struct SpreadDraw { uint32_t cosine_bin,azimuth_bin; };
struct ShotResolution {
 ShotKind kind; HitZone zone; ActorRef target;
 Pos3 origin,end; uint16_t damage; TraceHit contact;
};
bool resolve_shot(const CollisionView &,const RulesP1 &,const AngleTables &,
                  const MotionState &,const AcceptedShot &,SpreadDraw,
                  ShotResolution &,Fault &);
}
#endif
```

MotionState is ONLY a forward declaration of the future sole MAIN-adopted type. It is not a definition, reduced pose substitute or adoption of T183's unreviewed fields/semantics. No .cpp/consumer may infer those fields or compile against a fabricated type. The explicit immutable borrowed AngleTables supplies the actual accepted basis/cone context without private StaticStore access. Full living/source/stance/provenance and immutable lifetime/alias validation remain later exact caller/implementation obligations.

SpreadDraw contains TWO FULL supplied uint32 words despite historical bin field names: cosine_bin passes unchanged as draw0, azimuth_bin as draw1. All uint32 patterns including zero are allowed. The helper does not choose/retry/reseed/advance RNG or grant ordinal/cause/weapon eligibility. AcceptedShot attribution alone is not tick acceptance. None remains camera-only, not a shot mode.

D292 fixes future displacement endpoints/integer diagnostic convergence/early half_angle and late sampling/ordered World guards/coherent successful publication. This declaration-only adoption does NOT adopt the rest of T184's proposed local Fault/validation/storage/evidence-composition table or full M4/MotionState. Exact typed/validation/source/evidence gates remain before implementation. Full actual accepted G1/G2/current regression and camera implementation, portable caller, transaction, two-browser/renderer/human/performance proof remain mandatory. No header existence proves any of them.

T185 may write ONLY this new exact header and own NEW handoff/question. No other header/source/authority/build/asset/dependency edit, compiler/test/fixture/oracle/dataset/project import/SDK/FFI/probe/runtime/network/Git or worker dispatch. Verify literal bytes/includes/sole-home by read-only inspection; report compile/ABI/runtime NOT RUN. MAIN accepts the exact declaration artifact separately. Player/nativeT167/QA/T149/fullphase/human holds unchanged.
