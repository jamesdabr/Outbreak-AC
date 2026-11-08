#ifndef OB_MAP_IMPORT_H
#define OB_MAP_IMPORT_H
#include <stdint.h>
namespace ob {
constexpr uint32_t FLAT_MAP_MAX_RAW_BYTES=1048576;
constexpr uint32_t FLAT_MAP_MAX_CELLS=65536;
enum class MapImportError : uint8_t { None=0,Null=1,Size=2,Magic=3,Version=4,Header=5,Factor=6,Entities=7,Metadata=8,Unsupported=9,Capacity=10,Revision=11,CellType=12,CellData=13,Run=14,Trailing=15 };
struct FlatCell { uint8_t kind; int8_t floor; int8_t ceiling; uint8_t tag; };
struct FlatMapInfo { uint16_t side; uint32_t revision; uint16_t entity_count; };
bool decode_flat_map(const uint8_t *raw,uint32_t raw_bytes,FlatCell *cells,uint32_t capacity,FlatMapInfo &out,MapImportError &error);
}
#endif
