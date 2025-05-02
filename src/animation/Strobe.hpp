#pragma once

#include "Animation.hpp"
#include <vector>

class Strobe : public Animation {
public:
    using Animation::Animation;

    void animate(int beat, int step) override;

private:
    std::vector<std::vector<int>> select_range(int index, const std::vector<Color>& colors);
};
