#ifndef OUTBREAK_FIXED_H
#define OUTBREAK_FIXED_H

#include <stdint.h>

namespace ob {
constexpr int POSITION_FRAC_BITS = 10;
constexpr int VELOCITY_FRAC_BITS = 16;
constexpr int32_t UNIT_Q16 = 65536;

bool checked_add_i32(int32_t a, int32_t b, int32_t &out);
bool checked_sub_i32(int32_t a, int32_t b, int32_t &out);
bool rounded_mul_div_i32(int32_t a, int32_t b, int32_t denominator, int32_t &out);
uint32_t isqrt_u64(uint64_t value);
// Distinct output references are required. Invalid axes or aliases leave both unchanged.
bool normalize_axes_q16(int16_t x, int16_t y, int32_t &out_x, int32_t &out_y);
}
#endif
