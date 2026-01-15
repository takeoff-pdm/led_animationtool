#include "ArtNetPacket.hpp"

#include <array>
#include <cstring>
#include <sstream>

namespace {
constexpr std::array<char, 8> kArtNetId{'A', 'r', 't', '-', 'N', 'e', 't', 0};
constexpr std::size_t kArtNetHeaderSize = 18;
constexpr uint16_t kOpCodeArtDMX = 0x5000;  // Little-endian

uint16_t read_le_uint16(const std::vector<char>& buffer, std::size_t offset) {
    if (offset + 1 >= buffer.size()) {
        return 0;
    }
    return static_cast<uint16_t>(
        static_cast<uint8_t>(buffer[offset]) |
        (static_cast<uint8_t>(buffer[offset + 1]) << 8));
}

uint16_t read_be_uint16(const std::vector<char>& buffer, std::size_t offset) {
    if (offset + 1 >= buffer.size()) {
        return 0;
    }
    return static_cast<uint16_t>(
        (static_cast<uint8_t>(buffer[offset]) << 8) |
        static_cast<uint8_t>(buffer[offset + 1]));
}
}  // namespace

std::optional<ArtNetParseResult> parse_artnet_dmx(const std::vector<char>& payload) {
    if (payload.size() < kArtNetHeaderSize) {
        return std::nullopt;
    }

    if (std::memcmp(payload.data(), kArtNetId.data(), kArtNetId.size()) != 0) {
        return std::nullopt;
    }

    const uint16_t opcode = read_le_uint16(payload, 8);
    if (opcode != kOpCodeArtDMX) {
        return std::nullopt;
    }

    const uint8_t sequence = static_cast<uint8_t>(payload[12]);
    const uint8_t physical = static_cast<uint8_t>(payload[13]);
    const uint16_t universe = read_le_uint16(payload, 14);
    const uint16_t length = read_be_uint16(payload, 16);

    if (payload.size() < kArtNetHeaderSize + length) {
        return std::nullopt;
    }

    ArtNetDMXFrame frame{};
    frame.sequence = sequence;
    frame.physical = physical;
    frame.universe = universe;
    frame.data.reserve(length);
    for (std::size_t i = 0; i < length; ++i) {
        frame.data.push_back(static_cast<uint8_t>(payload[kArtNetHeaderSize + i]));
    }

    std::ostringstream oss;
    oss << "seq=" << static_cast<int>(frame.sequence)
        << " phys=" << static_cast<int>(frame.physical)
        << " universe=" << frame.universe
        << " length=" << frame.data.size();

    return ArtNetParseResult{std::move(frame), oss.str()};
}
