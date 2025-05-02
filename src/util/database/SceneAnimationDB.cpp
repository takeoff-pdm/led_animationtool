#include "SceneAnimationDB.hpp"
#include "Database.hpp"  // Assuming you have this class for handling DB operations
#include <vector>
#include <map>
#include <iostream>
#include <unordered_map>
#include <variant>

// Helper function to recreate a scene animation from data
std::map<std::string, int> SceneAnimationDB::recreate_scene_animation(const std::vector<std::string>& scene_animation_data) {
    return {
        {"scene_id",          std::stoi(scene_animation_data[0])},
        {"animation_id",      std::stoi(scene_animation_data[1])},
        {"section_id",        std::stoi(scene_animation_data[2])},
        {"color_sequence_id", std::stoi(scene_animation_data[3])}
    };
}

// Add a scene animation to the database
bool SceneAnimationDB::add_scene_animation(int scene_id, int animation_id, int section_id, int color_sequence_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"scene_id", scene_id},
        {"animation_id", animation_id},
        {"section_id", section_id},
        {"color_sequence_id", color_sequence_id}
    };

    std::string sql = "INSERT INTO scene_animations VALUES(:scene_id, :animation_id, :section_id, :color_sequence_id)";
    
    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Remove all scene animations for a given scene_id
bool SceneAnimationDB::remove_scene_animations(int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"scene_id", scene_id}
    };

    std::string sql = "DELETE FROM scene_animations WHERE scene_id = :scene_id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Remove a specific scene animation using scene_id and animation_id
bool SceneAnimationDB::remove_scene_animation(int scene_id, int animation_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"scene_id", scene_id},
        {"animation_id", animation_id}
    };

    std::string sql = "DELETE FROM scene_animations WHERE scene_id = :scene_id AND animation_id = :animation_id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Update a scene animation in the database
bool SceneAnimationDB::update_scene_animation(int scene_id, int animation_id, int section_id, int color_sequence_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"scene_id", scene_id},
        {"animation_id", animation_id},
        {"section_id", section_id},
        {"color_sequence_id", color_sequence_id}
    };

    std::string sql = "UPDATE scene_animations SET section_id = :section_id, color_sequence_id = :color_sequence_id "
                      "WHERE scene_id = :scene_id AND animation_id = :animation_id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Fetch all scene animations from the database
std::vector<std::map<std::string, int>> SceneAnimationDB::fetch_scene_animations() {
    std::vector<std::map<std::string, int>> scene_animations;

    std::string sql = "SELECT scene_id, animation_id, section_id, color_sequence_id FROM scene_animations";
    auto scene_animations_data = Database::fetchall_from_db(sql, {});

    if (scene_animations_data.empty()) {
        return scene_animations;
    }

    for (const auto& scene_animation_data : scene_animations_data) {
        scene_animations.push_back(recreate_scene_animation(scene_animation_data));
    }

    return scene_animations;
}

std::vector<std::map<std::string, int>> SceneAnimationDB::fetch_scene_animations_from_scene(int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {{"scene_id", scene_id}};
    std::string sql = "SELECT scene_id, animation_id, section_id, color_sequence_id FROM scene_animations WHERE scene_id = :scene_id";

    auto scene_animations_data = Database::fetchall_from_db(sql, params);

    if (scene_animations_data.empty()) {
        return {};
    }

    std::vector<std::map<std::string, int>> scene_animations;

    for (const auto& scene_animation_data : scene_animations_data) {
        scene_animations.push_back(recreate_scene_animation(scene_animation_data));
    }

    return scene_animations;
}

std::map<std::string, int> SceneAnimationDB::fetch_scene_animation(int scene_id, int animation_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"scene_id", scene_id},
        {"animation_id", animation_id}
    };

    std::string sql = "SELECT scene_id, animation_id, section_id, color_sequence_id FROM scene_animations WHERE scene_id = :scene_id AND animation_id = :animation_id";

    auto scene_animation_data = Database::fetchone_from_db(sql, params);

    if (scene_animation_data.empty()) {
        return {};
    }

    return recreate_scene_animation(scene_animation_data);
}
