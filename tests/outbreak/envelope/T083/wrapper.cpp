#include "envelope.h"
#ifdef T083_NATIVE
#include <iostream>
#include <string>
#endif

namespace {
uint8_t input[1200], output[1300], guarded[1200], saved[1200];
struct HeaderBox { uint8_t before[16]; ob::EnvelopeHeader value; uint8_t after[16]; };
struct ErrorBox { uint8_t before[16]; ob::EnvelopeError value; uint8_t after[16]; };
uint32_t u32(const uint8_t *p)
{
    return uint32_t(p[0]) | (uint32_t(p[1]) << 8) |
           (uint32_t(p[2]) << 16) | (uint32_t(p[3]) << 24);
}
void put(uint8_t *p, uint32_t v, unsigned n)
{
    for(unsigned i=0; i<n; ++i) p[i] = uint8_t((v >> (8*i)) & 255u);
}
void fill(void *p, unsigned n, uint8_t v)
{
    volatile uint8_t *b = static_cast<uint8_t *>(p);
    for(unsigned i=0; i<n; ++i) b[i]=v;
}
void copy(void *to, const void *from, unsigned n)
{
    volatile uint8_t *t=static_cast<uint8_t *>(to);
    const volatile uint8_t *f=static_cast<const uint8_t *>(from);
    for(unsigned i=0; i<n; ++i) t[i]=f[i];
}
bool same(const void *a, const void *b, unsigned n)
{
    const volatile uint8_t *x=static_cast<const uint8_t *>(a), *y=static_cast<const uint8_t *>(b);
    for(unsigned i=0; i<n; ++i) if(x[i]!=y[i]) return false;
    return true;
}
bool guard(const uint8_t *p, unsigned n)
{
    for(unsigned i=0; i<n; ++i) if(p[i]!=0xA5) return false;
    return true;
}
void fields(uint8_t *p, const ob::EnvelopeHeader &h)
{
    p[0]=h.message_type; put(p+1,h.body_bytes,2); put(p+3,h.connection_epoch,4);
    copy(p+7,h.match_id,16); put(p+23,h.sequence,4);
}
}

extern "C" uint8_t *case_buffer() { return input; }
extern "C" uint8_t *result_buffer() { return output; }
extern "C" uint32_t execute(uint32_t bytes)
{
    if(bytes<8 || bytes>sizeof(input)) return 0;
    const unsigned op=input[0], null_pointer=input[1], offset=input[2];
    const uint32_t length=u32(input+4);
    if(op>1 || offset>7 || length>1137 || (op==0 && bytes!=8+length) ||
       (op==1 && bytes!=35)) return 0;
    const unsigned extent=16+offset+length+16;
    fill(guarded,extent,0xA5);
    HeaderBox box, original;
    ErrorBox error;
    fill(&box,sizeof(box),0xA5); fill(&error,sizeof(error),0xA5);
    if(op==1)
    {
        box.value.message_type=input[8];
        box.value.body_bytes=uint16_t(uint32_t(input[9]) | (uint32_t(input[10])<<8));
        box.value.connection_epoch=u32(input+11);
        copy(box.value.match_id,input+15,16);
        box.value.sequence=u32(input+31);
    }
    else copy(guarded+16+offset,input+8,length);
    copy(&original,&box,sizeof(box)); copy(saved,guarded,extent);
    uint8_t *p=null_pointer ? 0 : guarded+16+offset;
    const bool ok=op==0 ? ob::decode_envelope(p,length,box.value,error.value) :
                          ob::encode_envelope_header(box.value,p,length,error.value);
    output[0]=uint8_t(ok); output[1]=uint8_t(error.value);
    output[2]=uint8_t(guard(box.before,16) && guard(box.after,16) &&
                       guard(error.before,16) && guard(error.after,16));
    output[3]=uint8_t(op==1 || same(saved,guarded,extent));
    output[4]=uint8_t(ok || (same(&box,&original,sizeof(box)) && same(saved,guarded,extent)));
    output[5]=uint8_t(op==0 || same(&box,&original,sizeof(box)));
#ifdef T083_NATIVE
    // Repeat against exact-size heap allocations. ASan sees the true end of the
    // declared input/capacity, while the guarded call checks all canary bytes.
    uint8_t *tight=new uint8_t[offset+length];
    copy(tight, saved+16, offset+length);
    HeaderBox again; copy(&again,&original,sizeof(again));
    ob::EnvelopeError tight_error=static_cast<ob::EnvelopeError>(0xA5);
    uint8_t *q=null_pointer ? 0 : tight+offset;
    const bool tight_ok=op==0 ? ob::decode_envelope(q,length,again.value,tight_error) :
                               ob::encode_envelope_header(again.value,q,length,tight_error);
    uint8_t a[27], b[27]; fields(a,box.value); fields(b,again.value);
    if(tight_ok!=ok || tight_error!=error.value || !same(a,b,27) ||
       !same(tight,guarded+16,offset+length) ||
       (!tight_ok && !same(&again,&original,sizeof(again)))) output[2]=0;
    delete[] tight;
#endif
    if(op==0) { fields(output+6,box.value); return 33; }
    copy(output+6,guarded,extent);
    return 6+extent;
}

#ifdef T083_NATIVE
int main()
{
    std::string line;
    const char *hex="0123456789abcdef";
    while(std::getline(std::cin,line))
    {
        if(line.size()%2 || line.size()>2*sizeof(input)) return 2;
        for(unsigned i=0; i<line.size()/2; ++i)
        {
            const size_t a=std::string(hex).find(line[2*i]), b=std::string(hex).find(line[2*i+1]);
            if(a>15 || b>15) return 3;
            input[i]=uint8_t(16*a+b);
        }
        const unsigned size=execute(uint32_t(line.size()/2));
        if(!size) return 4;
        for(unsigned i=0; i<size; ++i) std::cout << hex[output[i]>>4] << hex[output[i]&15];
        std::cout << '\n';
    }
    return std::cin.eof() ? 0 : 5;
}
#endif
