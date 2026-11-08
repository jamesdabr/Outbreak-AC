#ifndef OUTBREAK_ENVELOPE_H
#define OUTBREAK_ENVELOPE_H
#include <stdint.h>

namespace ob {
constexpr uint32_t ENVELOPE_HEADER_BYTES = 36;
constexpr uint32_t ENVELOPE_MAX_PACKET_BYTES = 1100;
constexpr uint16_t ENVELOPE_MAJOR = 1;
enum class EnvelopeError : uint8_t {
    None=0, Null=1, Short=2, Magic=3, Version=4, Flags=5,
    HeaderSize=6, Length=7, Type=8
};
struct EnvelopeHeader {
    uint8_t message_type;
    uint16_t body_bytes;
    uint32_t connection_epoch;
    uint8_t match_id[16];
    uint32_t sequence;
};
// Caller owns valid, nonoverlapping buffers/control/output objects. Header only:
// success does not validate the body or grant application/admission semantics.
bool decode_envelope(const uint8_t *packet, uint32_t packet_bytes,
                     EnvelopeHeader &out, EnvelopeError &error);
bool encode_envelope_header(const EnvelopeHeader &header, uint8_t *destination,
                            uint32_t capacity, EnvelopeError &error);
}
#endif
