#include "envelope.h"

namespace ob {
namespace {
uint16_t read_u16(const uint8_t *p)
{
    return static_cast<uint16_t>(static_cast<uint32_t>(p[0]) |
                                 (static_cast<uint32_t>(p[1]) << 8));
}
uint32_t read_u32(const uint8_t *p)
{
    return static_cast<uint32_t>(p[0]) |
           (static_cast<uint32_t>(p[1]) << 8) |
           (static_cast<uint32_t>(p[2]) << 16) |
           (static_cast<uint32_t>(p[3]) << 24);
}
void write_u16(uint8_t *p, uint16_t value)
{
    p[0] = static_cast<uint8_t>(value & 255u);
    p[1] = static_cast<uint8_t>(value >> 8);
}
void write_u32(uint8_t *p, uint32_t value)
{
    for(uint32_t i = 0; i < 4; ++i)
        p[i] = static_cast<uint8_t>((value >> (8 * i)) & 255u);
}
bool fail(EnvelopeError reason, EnvelopeError &error)
{
    error = reason;
    return false;
}
}

bool decode_envelope(const uint8_t *packet, uint32_t packet_bytes,
                     EnvelopeHeader &out, EnvelopeError &error)
{
    if(!packet) return fail(EnvelopeError::Null, error);
    if(packet_bytes < ENVELOPE_HEADER_BYTES) return fail(EnvelopeError::Short, error);
    if(packet_bytes > ENVELOPE_MAX_PACKET_BYTES) return fail(EnvelopeError::Length, error);
    if(packet[0] != 'O' || packet[1] != 'B' || packet[2] != 'P' || packet[3] != '1')
        return fail(EnvelopeError::Magic, error);
    if(read_u16(packet + 4) != ENVELOPE_MAJOR) return fail(EnvelopeError::Version, error);
    if(packet[7]) return fail(EnvelopeError::Flags, error);
    if(read_u16(packet + 10) != ENVELOPE_HEADER_BYTES)
        return fail(EnvelopeError::HeaderSize, error);
    if(read_u16(packet + 8) != packet_bytes) return fail(EnvelopeError::Length, error);
    if(!packet[6]) return fail(EnvelopeError::Type, error);

    EnvelopeHeader candidate = {};
    candidate.message_type = packet[6];
    candidate.body_bytes = static_cast<uint16_t>(packet_bytes - ENVELOPE_HEADER_BYTES);
    candidate.connection_epoch = read_u32(packet + 12);
    for(uint32_t i = 0; i < 16; ++i) candidate.match_id[i] = packet[16 + i];
    candidate.sequence = read_u32(packet + 32);
    out = candidate;
    error = EnvelopeError::None;
    return true;
}

bool encode_envelope_header(const EnvelopeHeader &header, uint8_t *destination,
                            uint32_t capacity, EnvelopeError &error)
{
    if(!destination) return fail(EnvelopeError::Null, error);
    if(capacity < ENVELOPE_HEADER_BYTES) return fail(EnvelopeError::Short, error);
    if(header.body_bytes > ENVELOPE_MAX_PACKET_BYTES - ENVELOPE_HEADER_BYTES)
        return fail(EnvelopeError::Length, error);
    if(!header.message_type) return fail(EnvelopeError::Type, error);

    destination[0] = 'O'; destination[1] = 'B';
    destination[2] = 'P'; destination[3] = '1';
    write_u16(destination + 4, ENVELOPE_MAJOR);
    destination[6] = header.message_type;
    destination[7] = 0;
    write_u16(destination + 8, static_cast<uint16_t>(ENVELOPE_HEADER_BYTES + header.body_bytes));
    write_u16(destination + 10, static_cast<uint16_t>(ENVELOPE_HEADER_BYTES));
    write_u32(destination + 12, header.connection_epoch);
    for(uint32_t i = 0; i < 16; ++i) destination[16 + i] = header.match_id[i];
    write_u32(destination + 32, header.sequence);
    error = EnvelopeError::None;
    return true;
}
}
