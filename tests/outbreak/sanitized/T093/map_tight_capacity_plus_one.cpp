// T093 owned copy; original T084 wrapper remains unchanged.
// Test-only ABI. All large storage is static, never production parser stack.
#include "map_import.h"
#ifdef T084_NATIVE
#include <stdio.h>
#endif
namespace {
uint8_t input[ob::FLAT_MAP_MAX_RAW_BYTES+3],saved[ob::FLAT_MAP_MAX_RAW_BYTES+1];
ob::FlatCell storage[ob::FLAT_MAP_MAX_CELLS+2];
struct GuardInfo { uint8_t before[16]; ob::FlatMapInfo info; uint8_t after[16]; } metadata;
uint8_t output[40+4*ob::FLAT_MAP_MAX_CELLS];
uint32_t output_size;
void word(uint32_t offset,uint32_t value) {
    for (uint32_t i=0;i<4;++i) output[offset+i]=static_cast<uint8_t>((value>>(8*i))&255);
}
bool unchanged(const uint8_t *p,uint32_t n) {
    for (uint32_t i=0;i<n;++i) if (p[i]!=165) return false;
    return true;
}
}
extern "C" {
uint8_t *input_ptr() { return input+1; }
uint8_t *output_ptr() { return output; }
uint32_t output_bytes() { return output_size; }
void run(uint32_t blob_bytes,uint32_t declared,uint32_t capacity,uint32_t nulls) {
    if (blob_bytes>ob::FLAT_MAP_MAX_RAW_BYTES+1) { output_size=0; return; }
    input[0]=165;input[blob_bytes+1]=165;
    for (uint32_t i=0;i<blob_bytes;++i) saved[i]=input[i+1];
    uint8_t *all=reinterpret_cast<uint8_t *>(storage);
    for (uint32_t i=0;i<sizeof(storage);++i) all[i]=165;
    uint8_t *meta=reinterpret_cast<uint8_t *>(&metadata);
    for (uint32_t i=0;i<sizeof(metadata);++i) meta[i]=165;
    ob::MapImportError error=static_cast<ob::MapImportError>(255);
    const bool ok=ob::decode_flat_map(nulls&1?0:input+1,declared,nulls&2?0:storage+1,capacity,metadata.info,error);
    bool input_ok=input[0]==165 && input[blob_bytes+1]==165;
    for (uint32_t i=0;i<blob_bytes;++i) if (saved[i]!=input[i+1]) input_ok=false;
    const uint32_t count=ok?uint32_t(metadata.info.side)*metadata.info.side:0;
    const bool guards=unchanged(all,sizeof(ob::FlatCell)) &&
        unchanged(reinterpret_cast<uint8_t *>(storage+ob::FLAT_MAP_MAX_CELLS+1),sizeof(ob::FlatCell)) &&
        unchanged(metadata.before,16) && unchanged(metadata.after,16);
    const bool failure_untouched=ok || (unchanged(all,sizeof(storage)) && unchanged(meta,sizeof(metadata)));
    const bool tail=unchanged(reinterpret_cast<uint8_t *>(storage+1+count),
                              (ob::FLAT_MAP_MAX_CELLS-count)*sizeof(ob::FlatCell));
    word(0,ok);word(4,static_cast<uint8_t>(error));word(8,metadata.info.side);
    word(12,metadata.info.revision);word(16,metadata.info.entity_count);
    word(20,input_ok);word(24,guards);word(28,failure_untouched);word(32,tail);word(36,count);
    for (uint32_t i=0;i<count;++i) {
        const ob::FlatCell &cell=storage[i+1];
        output[40+4*i]=cell.kind;output[41+4*i]=static_cast<uint8_t>(cell.floor);
        output[42+4*i]=static_cast<uint8_t>(cell.ceiling);output[43+4*i]=cell.tag;
    }
    // T093 native-only additional exact-allocation replay. The unchanged
    // guarded reference call above retains all original oracle-visible bytes.
    if (declared<=blob_bytes && declared<=ob::FLAT_MAP_MAX_RAW_BYTES+1 &&
        capacity<=ob::FLAT_MAP_MAX_CELLS+1) {
        uint8_t *tight_input=new uint8_t[declared];
        ob::FlatCell *tight_cells=new ob::FlatCell[capacity];
        for (uint32_t i=0;i<declared;++i) tight_input[i]=saved[i];
        uint8_t *tight_bytes=reinterpret_cast<uint8_t *>(tight_cells);
        for (uint32_t i=0;i<capacity*sizeof(ob::FlatCell);++i) tight_bytes[i]=165;
        GuardInfo tight_meta;
        uint8_t *tight_meta_bytes=reinterpret_cast<uint8_t *>(&tight_meta);
        for (uint32_t i=0;i<sizeof(tight_meta);++i) tight_meta_bytes[i]=165;
        ob::MapImportError tight_error=static_cast<ob::MapImportError>(255);
        const bool tight_ok=ob::decode_flat_map(nulls&1?0:tight_input,declared,
            nulls&2?0:tight_cells,capacity,tight_meta.info,tight_error);
        bool equal=tight_ok==ok && tight_error==error;
        for (uint32_t i=0;i<declared;++i) if (tight_input[i]!=saved[i]) equal=false;
        for (uint32_t i=0;i<capacity*sizeof(ob::FlatCell);++i)
            if (tight_bytes[i]!=reinterpret_cast<uint8_t *>(storage+1)[i]) equal=false;
        if (!unchanged(tight_meta.before,16) || !unchanged(tight_meta.after,16)) equal=false;
        if (ok) {
            if (tight_meta.info.side!=metadata.info.side ||
                tight_meta.info.revision!=metadata.info.revision ||
                tight_meta.info.entity_count!=metadata.info.entity_count) equal=false;
        } else if (!unchanged(tight_meta_bytes,sizeof(tight_meta))) equal=false;
        if (!equal) word(24,0); // Preserve original schema; fail original canary oracle.
        delete[] tight_cells;delete[] tight_input;
    }
    output_size=40+4*count;
}
}
#ifdef T084_NATIVE
int main() {
    uint8_t header[16];
    while (true) {
        const size_t n=fread(header,1,16,stdin);
        if (n==0) return ferror(stdin)?1:0;
        if (n!=16) return 2;
        uint32_t values[4]={0,0,0,0};
        for (uint32_t j=0;j<4;++j) for (uint32_t k=0;k<4;++k) values[j]|=uint32_t(header[j*4+k])<<(8*k);
        if (values[0]>ob::FLAT_MAP_MAX_RAW_BYTES+1 || fread(input+1,1,values[0],stdin)!=values[0]) return 3;
        run(values[0],values[1],values[2],values[3]);
        if (fwrite(output,1,output_size,stdout)!=output_size) return 4;
    }
}
#endif
