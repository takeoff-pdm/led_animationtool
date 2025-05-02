#include "SectionAnimationDB.hpp"
#include "Database.hpp"  // Assuming Database class for DB operations
#include "AnimationDB.hpp"  // Assuming Animation class for fetching animations

// Helper function to recreate a section animation from raw data
std::map<std::string, int> SectionAnimationDB::recreate_section_animation(const std::vector<std::string>& section_animation_data) {
    return {
        {"section_id", std::stoi(section_animation_data[0])},
        {"animation_id", std::stoi(section_animation_data[1])},
        {"variation", std::stoi(section_animation_data[2])},
        {"direction", std::stoi(section_animation_data[3])},
        {"offset", std::stoi(section_animation_data[4])}
    };
}

// Add animations to a section
bool SectionAnimationDB::add_section_animations(int section_id, int scene_id) {
    auto animations = AnimationDB::fetch_animations();

    if (!animations.has_value()) {
        return false;
    }

    for (const auto& animation : animations.value()) {
        if (!add_section_animation(section_id, animation.id, scene_id)) {
            return false;
        }
    }

    return true;
}

// Add a single section animation
bool SectionAnimationDB::add_section_animation(int section_id, int animation_id, int scene_id, 
                                              int variation, int direction, int offset) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"section_id", section_id},
        {"animation_id", animation_id},
        {"scene_id", scene_id},
        {"variation", variation},
        {"direction", direction},
        {"off_set", offset}
    };

    std::string sql = "INSERT INTO section_animations VALUES(:scene_id, :section_id, :animation_id, :variation, :direction, :off_set)";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Remove a section animation
bool SectionAnimationDB::remove_section_animation(int section_id, int animation_id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"section_id", section_id},
        {"animation_id", animation_id},
        {"scene_id", scene_id}
    };

    std::string sql = "DELETE FROM section_animations WHERE scene_id = :scene_id AND section_id = :section_id AND animation_id = :animation_id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Update a section animation (variation, direction, offset)
bool SectionAnimationDB::update_section_animation(int section_id, int animation_id, int variation, int direction, 
                                                 int offset, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>>params = {
        {"section_id", section_id},
        {"animation_id", animation_id},
        {"variation", variation},
        {"direction", direction},
        {"off_set", offset},
        {"scene_id", scene_id}
    };

    std::string sql = "UPDATE section_animations SET variation = :variation, direction = :direction, \
                       off_set = :off_set WHERE scene_id = :scene_id AND section_id = :section_id AND animation_id = :animation_id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Fetch a specific section animation by section_id, animation_id, and scene_id
std::map<std::string, int> SectionAnimationDB::fetch_section_animation(int section_id, int animation_id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"section_id", section_id},
        {"animation_id", animation_id},
        {"scene_id", scene_id}
    };

    std::string sql = "SELECT section_id, animation_id, variation, direction, off_set FROM section_animations \
                       WHERE scene_id = :scene_id AND section_id = :section_id AND animation_id = :animation_id";

    auto section_animation_data = Database::fetchone_from_db(sql, params);

    if (section_animation_data.empty()) {
        return {};
    }

    return recreate_section_animation(section_animation_data);
}

// Fetch all section animations by section_id and scene_id
std::vector<std::map<std::string, int>> SectionAnimationDB::fetch_section_animations(int section_id, int scene_id) {
    std::vector<std::map<std::string, int>> section_animations;

    std::unordered_map<std::string, std::variant<int, std::string>> params = {{"section_id", section_id}, {"scene_id", scene_id}};
    std::string sql = "SELECT section_id, animation_id, variation, direction, off_set FROM section_animations \
                       WHERE scene_id = :scene_id AND section_id = :section_id";

    auto section_animations_data = Database::fetchall_from_db(sql, params);

    if (section_animations_data.empty()) {
        return section_animations;
    }

    for (const auto& section_animation_data : section_animations_data) {
        section_animations.push_back(recreate_section_animation(section_animation_data));
    }

    return section_animations;
}
