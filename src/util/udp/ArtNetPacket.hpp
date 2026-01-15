#pragma once

#include <cstdint>
#include <optional>
#include <string>
#include <vector>

struct ArtNetDMXFrame {
    uint8_t sequence{};
    uint8_t physical{};
    uint16_t universe{};
    std::vector<uint8_t> data;
};

struct ArtNetParseResult {
    ArtNetDMXFrame frame;
    std::string debug_message;
};

std::optional<ArtNetParseResult> parse_artnet_dmx(const std::vector<char>& payload);
