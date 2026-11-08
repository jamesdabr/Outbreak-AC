#include "fixed.h"

// Test-owned ABI/state only; no production export hooks.
static int32_t first, second;
extern "C" int32_t result_x() { return first; }
extern "C" int32_t result_y() { return second; }
extern "C" uint32_t root(uint64_t value) { return ob::isqrt_u64(value); }
extern "C" int run(int op, int32_t a, int32_t b, int32_t c)
{
    first = 123456789;
    second = -987654321;
    switch(op)
    {
        case 0: return ob::checked_add_i32(a, b, first);
        case 1: return ob::checked_sub_i32(a, b, first);
        case 2: return ob::rounded_mul_div_i32(a, b, c, first);
        case 3: return ob::normalize_axes_q16(static_cast<int16_t>(a), static_cast<int16_t>(b), first, second);
        case 4: return ob::normalize_axes_q16(static_cast<int16_t>(a), static_cast<int16_t>(b), first, first);
        // Input/output aliasing for scalar APIs remains well-defined by value arguments.
        case 5: first = a; return ob::checked_add_i32(first, b, first);
        case 6: first = a; return ob::checked_sub_i32(first, b, first);
        case 7: first = a; return ob::rounded_mul_div_i32(first, b, c, first);
    }
    return -1;
}

#ifdef T078_NATIVE
#include <iostream>
int main()
{
    int op;
    while(std::cin >> op)
    {
        if(op == 8)
        {
            uint64_t value;
            if(!(std::cin >> value)) return 2;
            std::cout << 1 << ' ' << root(value) << ' ' << 0 << '\n';
        }
        else
        {
            int32_t a, b, c;
            if(!(std::cin >> a >> b >> c)) return 2;
            const int status = run(op, a, b, c);
            std::cout << status << ' ' << first << ' ' << second << '\n';
        }
    }
    return std::cin.eof() ? 0 : 3;
}
#endif
