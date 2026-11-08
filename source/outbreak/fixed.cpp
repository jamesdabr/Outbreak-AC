#include "fixed.h"

namespace ob {
namespace {
bool store_i32(int64_t value, int32_t &out)
{
    if(value < INT32_MIN || value > INT32_MAX) return false;
    out = static_cast<int32_t>(value);
    return true;
}
}

bool checked_add_i32(int32_t a, int32_t b, int32_t &out)
{
    return store_i32(static_cast<int64_t>(a) + b, out);
}

bool checked_sub_i32(int32_t a, int32_t b, int32_t &out)
{
    return store_i32(static_cast<int64_t>(a) - b, out);
}

bool rounded_mul_div_i32(int32_t a, int32_t b, int32_t denominator, int32_t &out)
{
    if(!denominator) return false;
    const int64_t product = static_cast<int64_t>(a) * b;
    const int64_t divisor = denominator;
    int64_t quotient = product / divisor;
    const int64_t remainder = product % divisor;
    // Products cannot be INT64_MIN; divisor/remainder magnitudes are <=2^31.
    const int64_t magnitude = remainder < 0 ? -remainder : remainder;
    const int64_t divisor_magnitude = divisor < 0 ? -divisor : divisor;
    if(magnitude * 2 >= divisor_magnitude)
        quotient += (product < 0) != (divisor < 0) ? -1 : 1;
    return store_i32(quotient, out);
}

uint32_t isqrt_u64(uint64_t value)
{
    // Exclusive upper bound may be 2^32; midpoint squares stay within uint64.
    uint64_t low = 0, high = UINT64_C(4294967296);
    while(low + 1 < high)
    {
        const uint64_t middle = low + (high - low) / 2;
        if(middle * middle <= value) low = middle;
        else high = middle;
    }
    return static_cast<uint32_t>(low);
}

bool normalize_axes_q16(int16_t x, int16_t y, int32_t &out_x, int32_t &out_y)
{
    if(&out_x == &out_y || x < -127 || x > 127 || y < -127 || y > 127)
        return false;
    const int64_t sum = static_cast<int64_t>(x) * x + static_cast<int64_t>(y) * y;
    int64_t result_x, result_y;
    if(sum <= 127 * 127)
    {
        result_x = static_cast<int64_t>(x) * UNIT_Q16 / 127;
        result_y = static_cast<int64_t>(y) * UNIT_Q16 / 127;
    }
    else
    {
        // sum<=32258, radicand<2^47, numerator magnitude<2^40.
        const uint64_t radicand = static_cast<uint64_t>(sum) << 32;
        uint64_t denominator = isqrt_u64(radicand);
        if(denominator * denominator != radicand) ++denominator;
        result_x = static_cast<int64_t>(x) * INT64_C(4294967296) /
                   static_cast<int64_t>(denominator);
        result_y = static_cast<int64_t>(y) * INT64_C(4294967296) /
                   static_cast<int64_t>(denominator);
    }
    // Validated axes prove both results are within [-65536,65536].
    out_x = static_cast<int32_t>(result_x);
    out_y = static_cast<int32_t>(result_y);
    return true;
}
}
