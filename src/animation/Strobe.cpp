#include "Strobe.hpp"
#include "../Color.hpp"
#include <cmath>
#include <iostream>

using namespace std;

std::vector<std::vector<int>> Strobe::select_range(int index, const std::vector<Color>& colors) {
    std::vector<std::vector<int>> animation_range;
    int len = colors.size();
    int total_leds = end_led - start_led + 1;

    auto get_range = [&](float start_ratio, float end_ratio) -> std::vector<int> {
        int start = static_cast<int>(start_led + total_leds * start_ratio);
        int end = static_cast<int>(start_led + total_leds * end_ratio);
        std::vector<int> range;
        for (int i = start; i < end; ++i) {
            range.push_back(i);
        }
        return range;
    };

    switch (direction) {
        case 0:  // Normal
            animation_range.push_back(get_range(
                1.0f / len * index,
                1.0f - 1.0f / len * (len - index - 1)));
            break;
        case 1:  // Reverse
            animation_range.push_back(get_range(
                1.0f / len * (len - index - 1),
                1.0f - 1.0f / len * index));
            break;
        case 2:  // Inner to outer
            animation_range.push_back(get_range(
                1.0f / len * index / 2.0f,
                1.0f - 1.0f / len * (len - index - 1) / 2.0f - 0.5f));
            animation_range.push_back(get_range(
                0.5f + 1.0f / len * (len - index - 1) / 2.0f,
                1.0f - 1.0f / len * index / 2.0f));
            break;
        case 3:  // Outer to inner
            animation_range.push_back(get_range(
                1.0f / len * (len - index - 1) / 2.0f,
                1.0f - 1.0f / len * index / 2.0f - 0.5f));
            animation_range.push_back(get_range(
                0.5f + 1.0f / len * index / 2.0f,
                1.0f - 1.0f / len * (len - index - 1) / 2.0f));
            break;
    }

    return animation_range;
}

void Strobe::animate(int beat, int step) {
    std::vector<Color> colors = select_colors(beat);
    int third = static_cast<int>(round(ANIMATION_STEPS * 0.33));
    int half = static_cast<int>(round(ANIMATION_STEPS * 0.5));
    int two_third = static_cast<int>(round(ANIMATION_STEPS * 0.66));
    int half_third = static_cast<int>(round(ANIMATION_STEPS * 0.125));

    bool should_flash = direction == 0 || (direction == 1 && beat % 2 == 0) ||
                        (direction == 2 && beat % 4 == 0) || (direction == 3 && beat % 8 == 0);

    if (!should_flash) return;

    auto turn_on = [&]() {
        for (size_t index = 0; index < colors.size(); ++index) {
            auto animation_ranges = select_range(static_cast<int>(index), colors);
            for (const auto& range : animation_ranges) {
                for (int led : range) {
                    set_pixel_color(led, colors[index].red, colors[index].green, colors[index].blue);
                }
            }
        }
    };

    auto turn_off = [&]() {
        for (int i = start_led; i <= end_led; i++) {
            Color c = black();
            set_pixel_color(i, 0, 0, 0);
        }
    };

    switch (variation) {
        case 0:
            if (step == 0) {
                turn_on();
            } else if (step == third) {
                turn_off();
            }
            break;
        case 1:
            if (step == 0 || step == half) {
                turn_on();
            } else if (step == half_third || step == two_third) {
                turn_off();
            }
            break;
        case 2:
            if (step == 0 || step == third || step == two_third) {
                turn_on();
            } else if (step == half_third || step == third + half_third || step == two_third + half_third) {
                turn_off();
            }
            break;
    }
}
