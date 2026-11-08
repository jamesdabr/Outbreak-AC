// T093 intentional instrumentation control, never linked into production.
#include <stdint.h>
int main() {
    volatile int32_t maximum=2147483647;
    volatile int32_t one=1;
    volatile int32_t value=maximum+one; // Deliberate signed overflow.
    return value==0;
}
