#pragma once

#include "Database.hpp"
#include <string>
#include <vector>
#include <optional>

class AnimationDB {
public:
    int id;
    std::string name;
    std::string description;

    static bool add_animation(int id, const std::string& name, const std::string& description);
    static bool remove_animation(int id);
    static bool update_animation(int id, const std::string& name, const std::string& description);
    static std::optional<std::vector<AnimationDB>> fetch_animations();
    static std::optional<AnimationDB> fetch_animation(int id);

private:
    static AnimationDB recreate_animation(const std::vector<std::string>& animation_data);
};
