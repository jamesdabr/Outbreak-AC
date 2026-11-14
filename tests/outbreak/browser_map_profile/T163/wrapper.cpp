#include "browser_map_profile.h"
#include "browser_map_profile.h"
#ifndef T163_GUARD_ONLY
#include <stdint.h>
#ifdef T163_NATIVE
#include <stdio.h>
#endif
static uint8_t request[96];
struct Guarded { uint8_t before[8],bytes[192],after[8]; };
static Guarded response;
static uint32_t u32(const uint8_t *p){return uint32_t(p[0])|(uint32_t(p[1])<<8)|(uint32_t(p[2])<<16)|(uint32_t(p[3])<<24);}
static int32_t s32(const uint8_t *p){const uint32_t n=u32(p);return n<=INT32_MAX?int32_t(n):int32_t(int64_t(n)-INT64_C(4294967296));}
static void put(uint8_t *p,uint32_t n){for(unsigned i=0;i<4;++i)p[i]=uint8_t(n>>(8*i));}
static void text(uint8_t *out,unsigned capacity,const char *value){for(unsigned i=0;i<capacity-1 && value[i];++i)out[i]=uint8_t(value[i]);}
extern "C" {
uint32_t request_address(){return uint32_t(uintptr_t(request));}
uint32_t response_address(){return uint32_t(uintptr_t(response.bytes));}
uint32_t request_capacity(){return 96;}
uint32_t response_capacity(){return 192;}
uint32_t run(){
    bool name_end=false,loaded_end=false;
    for(unsigned i=0;i<32;++i){if(!request[i])name_end=true;if(!request[32+i])loaded_end=true;}
    if(!name_end||!loaded_end||request[88]>1||request[89]>1||request[90]>3)return 1;
    uint8_t original[96];for(unsigned i=0;i<96;++i)original[i]=request[i];
    for(unsigned i=0;i<8;++i)response.before[i]=response.after[i]=uint8_t(0xa0+i);
    for(unsigned i=0;i<192;++i)response.bytes[i]=0;
    const char *received=request[90]&1?nullptr:reinterpret_cast<const char *>(request);
    const char *loaded=request[90]&2?nullptr:reinterpret_cast<const char *>(request+32);
    const int rev=s32(request+64),loaded_rev=s32(request+68),bytes=s32(request+72),advertised=s32(request+76),mode=s32(request+80),result=s32(request+84);
    const bool receipt=request[88]!=0,incompatible=request[89]!=0;
    using namespace ob_browser_map;
    text(response.bytes,32,name());text(response.bytes+32,48,cgz_path());text(response.bytes+80,48,cfg_path());put(response.bytes+128,uint32_t(revision()));
    text(response.bytes+132,32,receipt_name(receipt));put(response.bytes+164,uint32_t(receipt_revision(receipt)));
    const uint32_t flags=uint32_t(name_matches(received))|
        (uint32_t(loaded_matches(loaded,loaded_rev,bytes))<<1)|
        (uint32_t(startup_loaded(result,loaded,loaded_rev,bytes))<<2)|
        (uint32_t(observed_matches(received,rev,loaded,loaded_rev,bytes,mode,2))<<3)|
        (uint32_t(pre_change(received,mode,2,advertised,rev,loaded,loaded_rev,bytes))<<4)|
        (uint32_t(post_change(result,incompatible,received,mode,2,advertised,rev,loaded,loaded_rev,bytes))<<5)|
        (uint32_t(spawn_matches(receipt,loaded,loaded_rev,bytes,mode,2))<<6);
    put(response.bytes+168,flags);
    bool unchanged=true,guards=true;
    for(unsigned i=0;i<96;++i)if(original[i]!=request[i])unchanged=false;
    for(unsigned i=0;i<8;++i)if(response.before[i]!=uint8_t(0xa0+i)||response.after[i]!=uint8_t(0xa0+i))guards=false;
    put(response.bytes+172,uint32_t(unchanged)|(uint32_t(guards)<<1));
    return 0;
}
}
#ifdef T163_NATIVE
int main(){
    unsigned count=0;
    while(true){const size_t n=fread(request,1,96,stdin);if(!n)return ferror(stdin)?1:0;
        if(n!=96||++count>1024||run()||fwrite(response.bytes,1,192,stdout)!=192)return 2;}
}
#endif
#endif
