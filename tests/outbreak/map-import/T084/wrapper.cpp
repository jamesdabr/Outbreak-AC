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
