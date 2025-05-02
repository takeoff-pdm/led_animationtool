#pragma once
#include <string>
#include <vector>

struct AnimationDataEntry {
    int id;
    std::string name;
    std::string description;
};

const std::vector<AnimationDataEntry> get_animations();
