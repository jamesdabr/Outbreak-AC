# Portable format prerequisite

Revision:0.1. Status: APPROVED ISOLATED P0 PREREQUISITES under D079. These unused portable modules freeze only the exact APIs/subsets below; they do not integrate or select a production app protocol, implement gameplay, accept full T002/P0/P1, or replace legacy1300/browser/native code. GOV/BROWSER_FOUNDATION/P0 remain0.5 plus this separately versioned addendum. Existing numeric foundation0.1 unchanged.

Production files are C++11/namespace ob, bounded/no allocation, I/O, SDL/GL/ENet/JS/filesystem/wallclock/exceptions/mutable global state, no large stack arrays. No unrelated public symbol or existing source/header/build/profile edit. All functions assume caller supplies valid allocations for declared buffer lengths and separate control/output objects; input/output/error objects must not overlap. No arbitrary pointer-provenance promise. Error refs report failure; other outputs and destination bytes remain UNCHANGED on any failure. No signed overflow/unaligned loads/struct memcpy/padding/endian/float assumptions.

## A — envelope header (Engine exclusive T083)

NEW source/outbreak/envelope.h/.cpp. Public exact declarations:

```cpp
namespace ob {
constexpr uint32_t ENVELOPE_HEADER_BYTES=36;
constexpr uint32_t ENVELOPE_MAX_PACKET_BYTES=1100;
constexpr uint16_t ENVELOPE_MAJOR=1;
enum class EnvelopeError : uint8_t { None=0,Null=1,Short=2,Magic=3,Version=4,Flags=5,HeaderSize=6,Length=7,Type=8 };
struct EnvelopeHeader {
 uint8_t message_type; uint16_t body_bytes; uint32_t connection_epoch;
 uint8_t match_id[16]; uint32_t sequence;
};
bool decode_envelope(const uint8_t *packet,uint32_t packet_bytes,EnvelopeHeader &out,EnvelopeError &error);
bool encode_envelope_header(const EnvelopeHeader &header,uint8_t *destination,uint32_t capacity,EnvelopeError &error);
}
```

Wire offsets:0..3 literal OBP1;4..5 little-endian major1;6 message_type;7 flags0;8..9 complete packet bytes;10..11 header bytes36;12..15 connection_epoch;16..31 opaque match_id;32..35 sequence. Every scalar explicitly little-endian; opaque ID bytes unchanged. body_bytes is complete_len−36, allowed0..1064. Type0 invalid; every other uint8 accepted by HEADER ONLY. Epoch/sequence/ID zero valid here (prejoin meanings unapproved). Unknown application message types, body content/auth/match/sequence semantics MUST be rejected/validated by a later actual application decoder; header success is no app/admission/state grant.

decode null=>Null; packet_bytes<36=>Short,>1100=>Length before any header read; then validate magic,major,flags,header-size,complete-length exactly equals providedpacket_bytes,nonzero type in that order. On success copy every field/errorNone; never modify input. Trailing/truncated declared payload rejects.

encode writes EXACT first36 bytes, never body/remainingcapacity. null destination=>Null; capacity<36=>Short; body_bytes>1064=>Length; zero type=>Type, in that order. Complete-length field36+body; all flags/header/version constants fixed; errorNone on success. Caller appends body separately; this function does not claim complete packet serialization. Preflight all failure checks before any destination write. Use small staging/local scalar records, no1100-byte payload copy needed.

Tests execute actual SAME production code native ANDWasm plus native ASan/UBSan where installed toolchain supports it, against independent Python struct/integer golden bytes/header oracle. Cover exact offsets/endian/IDs/type0/255/epoch&sequence extrema/body0/1064/1065/65535, every truncation0..35, all provided lengths36..1101, corrupted/unknown header fields/extra body/declared mismatch, output/destination/full guard-canary preservation on failures, untouched trailing destination on success. Bounded deterministic randomized corpus also required. No fake codec, object-only PASS or unknown app-message acceptance claim.

## B — decompressed dry-flat native map subset (World exclusive T084)

NEW source/outbreak/map_import.h/.cpp. Header-only types include stdint.h. Public exact declarations:

```cpp
namespace ob {
constexpr uint32_t FLAT_MAP_MAX_RAW_BYTES=1048576;
constexpr uint32_t FLAT_MAP_MAX_CELLS=65536;
enum class MapImportError : uint8_t { None=0,Null=1,Size=2,Magic=3,Version=4,Header=5,Factor=6,Entities=7,Metadata=8,Unsupported=9,Capacity=10,Revision=11,CellType=12,CellData=13,Run=14,Trailing=15 };
struct FlatCell { uint8_t kind; int8_t floor; int8_t ceiling; uint8_t tag; };
struct FlatMapInfo { uint16_t side; uint32_t revision; uint16_t entity_count; };
bool decode_flat_map(const uint8_t *raw,uint32_t raw_bytes,FlatCell *cells,uint32_t capacity,FlatMapInfo &out,MapImportError &error);
}
```

Input is ALREADY BOUNDED-DECOMPRESSED ACMPv10 bytes, NOT gzip/file/config. A later outer adapter must bound gzip/CRC/output/hash; tests use inspected Pythonstdlib gzip/zlib on pinned T064/T080 files only. This decoder never executes/parses map configs into gameplay or instantiates entities.

Null raw/cells=>Null; raw length outside[980,1048576]=>Size. Header magicACMP/version10; positive little-endian header_size[980,5076], factor6..8(side1<<factor), signed native entitycount0..1024, header+16*count strictly before EOF; revision at924 in[1,INT32_MAX]. Native waterlevel at916 must be−10000(dry), inlinecfgsize at932 must0; unsupported features reject, never silently flatten. Header texture mappings/material bytes may be ignored ONLY as nongeometry; remaining relevant native geometry modifiers below cannot be ignored. Count/offset/size multiplication/addition checked before access. capacity>=side² required.

Header extension either empty or<=16 sequential bounded informational HX_MAPINFO records: one-byte length1..127 then one-byte flags65, exact in-header payload length, at least2NULs endingNUL, no config/otherflag/extendedvarint accepted. Unknown or overlong record unsupported/metadata failure. This is deliberately the known owned dry-flat subset, not general native-map compatibility.

Entity records are16 bytes <hhhhBBBBhbB; permit ONLY LIGHT1/PLAYERSTART2, x/y in[0,side),z in[-128,127]. LIGHT radius(attr1)1..255/unusedattr5..7 zero; PLAYERSTART attr1[0,3599],attr2 in{0,1,100},otherattrs zero. Unknown mapmodel/item/clip/entity behavior rejected. Valid records are inspected/skipped, not deployed/collision objects/authority inputs. Canonical squad anchors remain the separately accepted Q10 sidecar; legacy starts never substitute.

RLE stream starts header+16*entities, emits exactlyside² cells row-major x-fast. Ordinary SOLID0 consumes next2 bytes(walltexture,vdelta), requires vdelta0, outputs{kind0,floor0,ceiling0,tag0}. Ordinary SPACE4 consumes next8 bytes: signedfloor,signedceil,wtex,ftex,ctex,vdelta,upper,tag; floor<ceil, vdelta0/tag0 required, material/upper indices otherwise nongeometry bytes ignored. Outputs{kind4,decodedfloor,decodedceil,tag0}. Unknown cell kind=>CellType; unsupported vdelta/tag=>Unsupported; badfloor/ceil=>CellData. Repeat255 consumes one unsignedcount1..255, needs previous ordinary/repeated cell and count<=remaining; elseRun. No zero runs, overflow, missing bytes or trailing payload. Signedbytes decoded by explicit arithmetic (no implementation-defined unsigned-to-signed truncation). Do not assume another native corner/heightfield/clip/mip shape is SPACE.

No partial output on ANY error, including late RLE/trailing failure: validate complete immutableinput first, then emit in second pass (or equivalent bounded strategy without large stack/canonical mutation). Caller input remains immutable duringcall/nonoverlappingcellstorage. Out metadata updated only after successful full emission. No allocation/huge scratchstate; production stack<=4096bytes. Grid is physical flat-cell data only, not capsule/actor/world-query/nav/mask correctness proof.

Tests execute actual SAME production source native ANDWasm and native ASan/UBSan where installed. Compare every positive decoded cell/meta against independent source geometry/golden generated grids for pinned T064 map2/T080 candidate and synthetic factor6/7/8 flat maps. Native engine importer/rendering NOT inferred. Cover all header/count/offset/capacity/revision/extensions/entities/cell types/signed heights/truncation/RLEfirst/zero/overshoot/EOF/trailing/late-error canary cases and deterministic malformed/fuzz corpus. Entire outputs/canaries unchanged on failure, not a hash alone. Positive tests full field equality; bounded batches/output. Unsupported known features reject explicitly.

## Tools/evidence shared gate

Use already-installed inspected nativeclang/SDKClang/LLD/Node/Python and task-owned frozen cache/sysroot/temp/logs only; no acquisition/global/SDK/cache mutation. Minimal directWasm test linking/explicit named testABI exports only, no full game/ports/browser/native server/network or export-all/error suppression. Existing inspected compiler-memory builtin/libc archive may be linked if required, with recorded identity; final testWasm must run without unimplemented imports. New dependency/unsupported runtime/flag => question. Test wrapper exports are not production API. Record source/ABI/tool/flags/commands/corpus/native+Wasm+sanitizer outputs and failures; preserve game/source/src/enet/artifacts/SDK. Other test-controller owners may update their separate directories and are not transitive inputs unless actually consumed. MAIN reviews before dependent code/build integration. All P0/P1/MVP/authority/human gates remain.
