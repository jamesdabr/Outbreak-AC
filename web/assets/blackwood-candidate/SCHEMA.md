# T080 candidate DATA schema 1

Authority: T080 revision 5.3 and BLACKWOOD_DATA_FOUNDATION revision 0.1.
The executable strict schema is `validate.py:exact` against `candidate.py:sidecar`
and the SHA-pinned final T076 iteration2 tables. It requires exact types, keys,
array order, IDs and values; booleans do not satisfy integer fields. The full
canonical JSON bytes are checked too. There are no extensible/optional fields.

Coordinates are integer Q10 (1024 per engine unit), foot origin, east/north/up.
Point arrays have three integers and foot z=0. Rectangle arrays have four
integers [x0,y0,x1,y1]; the extraction prism has six [x0,y0,z0,x1,y1,z1]. Bounds
are half-open. Slot offsets are exactly ±1408 Q10, never rounded native starts.

The sidecar has exactly these top-level fields:

| Field | Exact shape / identity |
| --- | --- |
| schema_version / map_revision | integer 1 / integer 1 |
| profile | BLACKWOOD_GREYBOX_CANDIDATE_DATA |
| map_name | blackwood_greybox_v1 |
| coordinate_system | Q10_FOOT_EAST_NORTH_UP |
| source_plan_sha256 / source_report_sha256 | pinned T076 final source SHA256 strings |
| regions | 4 × {id,bounds_q10}, BW-R00..03 clipped quadrants |
| deployment_clusters | 8 × {id,center_q10,aim_cdeg_from_east,slots}, BW-D00..07 |
| each slots array | 4 × {id,position_q10}, cluster ID followed by -S0..3 |
| loot | 32 × {id,position_q10,kind}, BW-L01..32 |
| barricades | 12 × {id,position_q10,axis}, BW-B01..12, axis x/y |
| walkers | 12 × {id,position_q10}, BW-I01..12 |
| reinforcements | 8 × {id,position_q10}, BW-RI01..08 |
| predators | 4 × {id,position_q10}, BW-P01..04 |
| portals | 2 × {id,position_q10}, BW-V01..02 |
| extraction | {id,position_q10,bounds_q10}, BW-E01 |
| reserved_corridors | 4 × {id,bounds_q10}, BW-X01..04 |
| limitations | exact four strings from approved DATA contract |

IDs are globally unique; all arrays are ordered by ID. Loot kinds repeat the
approved eight-item pattern ammo_pistol, ammo_rifle, medical, wood, ammo_pistol,
wood, medical, wood. No stock, awards, HP, cost, actor grants, scripts, runtime
counters, seed policy or navigation graph exist in this sidecar. Panel geometry
is the approved implicit DATA shape 4 wide × 4 high × 0.5 thick; there is no
placed wood geometry or placement permission.

The manifest has exactly schema_version, profile, map_name, map_revision,
coordinate_system, source_plan_sha256, source_report_sha256, entries,
native_decoder, runtime, overlay. The last three are false. Exactly five entries
are sorted by path; each has exactly {path,bytes,sha256,license,notice}, integer
byte size, lowercase SHA256, license MIT and notice LICENSE.txt. Absolute,
traversing, backslash, symlink, duplicate, extra and unhashed members fail.

PROVENANCE.json records eight pinned source/template inputs, the three generation
and validation module hashes, three original texture dependencies, configuration
body hash, exact geometry origin, chosen deterministic lights, yaw conversion,
separate legacy/canonical conventions and limitations. Its entire content is
reconstructed and compared; it cannot authorize runtime behavior.
