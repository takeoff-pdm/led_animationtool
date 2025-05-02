#include "util/configuration/AnimationData.hpp"

const std::vector<AnimationDataEntry> get_animations() {
    std::vector<AnimationDataEntry> animations;

    animations.push_back({0, "MonoColor", "Monochromatic color switching. Variation 1: No fade; Variation 2: Fade out"});
    animations.push_back({1, "Flow", "Flows given colors through the section (Pixel by pixel)"});
    animations.push_back({2, "Shooter", "Shoots given colors through the section (Pixel by pixel)"});
    animations.push_back({3, "Strobe", "Strobe effect. Variation 1: All blinks shortly after each other; Variation 2: All blinks are equally distributed"});
    animations.push_back({4, "Squeeze", "Squeeze section more in more to one side/into the center"});
    
    return animations;
}
