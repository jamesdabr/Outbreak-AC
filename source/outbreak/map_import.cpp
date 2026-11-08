#include "map_import.h"
namespace ob {
namespace {
uint32_t u32(const uint8_t *p) {
    return uint32_t(p[0]) | (uint32_t(p[1])<<8) | (uint32_t(p[2])<<16) | (uint32_t(p[3])<<24);
}
int32_t s16(const uint8_t *p) {
    const uint32_t n=uint32_t(p[0]) | (uint32_t(p[1])<<8);
    return n<32768 ? int32_t(n) : int32_t(n)-65536;
}
int8_t s8(uint8_t n) { return static_cast<int8_t>(n<128 ? int32_t(n) : int32_t(n)-256); }
bool fail(MapImportError &error,MapImportError value) { error=value; return false; }

// The first pass checks every byte, including late errors, without touching
// destination storage. Only after it succeeds does the second pass emit cells.
bool stream(const uint8_t *raw,uint32_t bytes,uint32_t offset,uint32_t total,
            FlatCell *destination,MapImportError &error) {
    uint32_t emitted=0;
    FlatCell previous={0,0,0,0};
    while (emitted<total) {
        if (offset==bytes) return fail(error,MapImportError::CellData);
        const uint8_t kind=raw[offset++];
        uint32_t count=1;
        if (kind==255) {
            if (offset==bytes || emitted==0) return fail(error,MapImportError::Run);
            count=raw[offset++];
            if (count==0 || count>total-emitted) return fail(error,MapImportError::Run);
        } else if (kind==0) {
            if (bytes-offset<2) return fail(error,MapImportError::CellData);
            if (raw[offset+1]!=0) return fail(error,MapImportError::Unsupported);
            offset+=2;
            previous.kind=0; previous.floor=0; previous.ceiling=0; previous.tag=0;
        } else if (kind==4) {
            if (bytes-offset<8) return fail(error,MapImportError::CellData);
            const int8_t floor=s8(raw[offset]),ceiling=s8(raw[offset+1]);
            if (floor>=ceiling) return fail(error,MapImportError::CellData);
            if (raw[offset+5]!=0 || raw[offset+7]!=0) return fail(error,MapImportError::Unsupported);
            offset+=8;
            previous.kind=4; previous.floor=floor; previous.ceiling=ceiling; previous.tag=0;
        } else return fail(error,MapImportError::CellType);
        if (destination) for (uint32_t i=0;i<count;++i) destination[emitted+i]=previous;
        emitted+=count;
    }
    if (offset!=bytes) return fail(error,MapImportError::Trailing);
    return true;
}
}

bool decode_flat_map(const uint8_t *raw,uint32_t bytes,FlatCell *cells,uint32_t capacity,
                     FlatMapInfo &out,MapImportError &error) {
    if (!raw || !cells) return fail(error,MapImportError::Null);
    if (bytes<980 || bytes>FLAT_MAP_MAX_RAW_BYTES) return fail(error,MapImportError::Size);
    if (raw[0]!='A' || raw[1]!='C' || raw[2]!='M' || raw[3]!='P') return fail(error,MapImportError::Magic);
    if (u32(raw+4)!=10) return fail(error,MapImportError::Version);
    const uint32_t header=u32(raw+8),factor=u32(raw+12),entities=u32(raw+16);
    if (header<980 || header>5076 || header>bytes) return fail(error,MapImportError::Header);
    if (factor<6 || factor>8) return fail(error,MapImportError::Factor);
    if (entities>1024) return fail(error,MapImportError::Entities);
    // With these bounds, multiply/add cannot overflow uint32_t.
    const uint32_t start=header+16*entities;
    if (start>=bytes) return fail(error,MapImportError::Entities);
    const uint32_t revision=u32(raw+924);
    if (revision==0 || revision>2147483647U) return fail(error,MapImportError::Revision);
    if (u32(raw+916)!=4294957296U || u32(raw+932)!=0) return fail(error,MapImportError::Unsupported);
    const uint32_t side=uint32_t(1)<<factor,total=side*side;
    if (capacity<total) return fail(error,MapImportError::Capacity);
    uint32_t offset=980,records=0;
    while (offset<header) {
        if (++records>16 || header-offset<2) return fail(error,MapImportError::Metadata);
        const uint32_t length=raw[offset++];
        const uint8_t flags=raw[offset++];
        if (length==0 || length>127 || length>header-offset) return fail(error,MapImportError::Metadata);
        if (flags!=65) return fail(error,MapImportError::Unsupported);
        uint32_t zeros=0;
        for (uint32_t i=0;i<length;++i) if (raw[offset+i]==0) ++zeros;
        if (zeros<2 || raw[offset+length-1]!=0) return fail(error,MapImportError::Metadata);
        offset+=length;
    }
    for (uint32_t i=0;i<entities;++i) {
        const uint8_t *e=raw+header+16*i;
        const int32_t x=s16(e),y=s16(e+2),z=s16(e+4),a1=s16(e+6);
        if (x<0 || y<0 || uint32_t(x)>=side || uint32_t(y)>=side || z< -128 || z>127)
            return fail(error,MapImportError::Entities);
        if (e[8]!=1 && e[8]!=2) return fail(error,MapImportError::Unsupported);
        if (e[12]!=0 || e[13]!=0 || e[14]!=0 || e[15]!=0)
            return fail(error,MapImportError::Entities);
        if (e[8]==1) {
            if (a1<1 || a1>255) return fail(error,MapImportError::Entities);
        } else {
            if (a1<0 || a1>3599 || (e[9]!=0 && e[9]!=1 && e[9]!=100) || e[10]!=0 || e[11]!=0)
                return fail(error,MapImportError::Entities);
        }
    }
    if (!stream(raw,bytes,start,total,0,error)) return false;
    // Caller guarantees immutable, nonoverlapping input: the identical pass
    // cannot fail after validation and needs only a single small cell record.
    stream(raw,bytes,start,total,cells,error);
    out.side=static_cast<uint16_t>(side); out.revision=revision;
    out.entity_count=static_cast<uint16_t>(entities); error=MapImportError::None;
    return true;
}
}
