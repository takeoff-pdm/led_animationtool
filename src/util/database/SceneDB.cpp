#include "SceneDB.hpp"
#include "Database.hpp"
#include "SectionDB.hpp"
#include "ColorDB.hpp"
#include "ColorSequenceDB.hpp"
#include "SectionAnimationDB.hpp"
#include <vector>
#include <map>
#include <iostream>

// Helper function to recreate a scene from data
std::map<std::string, std::string> SceneDB::recreate_scene(const std::vector<std::string>& scene_data) {
    return {
        {"id", scene_data[0]},
        {"name", scene_data[1]},
        {"description", scene_data[2]}
    };
}

// Add a scene to the database
bool SceneDB::add_scene(int id, const std::string& name, const std::string& description) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"id", std::to_string(id)},
        {"name", name},
        {"description", description}
    };

    std::string sql = "INSERT INTO scenes VALUES(:id, :name, :description)";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Remove a scene from the database
bool SceneDB::remove_scene(int id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {{"id", std::to_string(id)}};
    std::string sql = "DELETE FROM scenes WHERE id = :id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Update a scene's name and description
bool SceneDB::update_scene(int id, const std::string& name, const std::string& description) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"id", std::to_string(id)},
        {"name", name},
        {"description", description}
    };

    std::string sql = "UPDATE scenes SET name = :name, description = :description WHERE id = :id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Fetch all scenes from the database
std::vector<std::map<std::string, std::string>> SceneDB::fetch_scenes() {
    std::vector<std::map<std::string, std::string>> scenes;

    std::string sql = "SELECT id, name, description FROM scenes";
    auto scenes_data = Database::fetchall_from_db(sql, {});

    if (scenes_data.empty()) {
        return scenes;
    }

    for (const auto& scene_data : scenes_data) {
        scenes.push_back(recreate_scene(scene_data));
    }

    return scenes;
}

// Fetch a specific scene by its ID
std::map<std::string, std::string> SceneDB::fetch_scene(int id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {{"id", std::to_string(id)}};
    std::string sql = "SELECT id, name, description FROM scenes WHERE id = :id";

    auto scene_data = Database::fetchone_from_db(sql, params);

    if (scene_data.empty()) {
        return {};
    }

    return recreate_scene(scene_data);
}

// Load a scene with all its related data
bool SceneDB::load_scene(int scene_id) {
    bool success = false;

    // Handle Sections
    auto workspace_sections = SectionDB::fetch_sections(scene_id);
    if (!workspace_sections.empty()) {
        for (const auto& section : workspace_sections) {
            SectionDB::remove_section(std::get<int>(section.at("id")));
        }
    }

    auto sections = SectionDB::fetch_sections(scene_id);
    for (const auto& section : sections) {
        SectionDB::add_section(std::get<int>(section.at("id")), std::get<std::string>(section.at("name")), 
                              std::get<int>(section.at("start_led")), std::get<int>(section.at("end_led")), scene_id);
    }

    // Handle ColorDB Sequences
    auto workspace_color_sequences = ColorSequenceDB::fetch_color_sequences(scene_id);
    if (!workspace_color_sequences.has_value()) {
        for (const auto& color_sequence : workspace_color_sequences.value()) {
            ColorSequenceDB::remove_color_sequence(color_sequence.id);
        }
    }

    auto color_sequences = ColorSequenceDB::fetch_color_sequences(scene_id);
    if (color_sequences.has_value()) {
        for (const auto& color_sequence : color_sequences.value()) {
            ColorSequenceDB::add_color_sequence(color_sequence.id, color_sequence.name, color_sequence.description, 
                                              color_sequence.selection, color_sequence.color_amount);
        }
    }

    // Handle Colors
    auto workspace_colors = ColorDB::fetch_colors(scene_id);
    if (!workspace_colors.empty()) {
        for (const auto& color : workspace_colors) {
            ColorDB::remove_color(color.id);
        }
    }

    auto colors = ColorDB::fetch_colors(scene_id);
    for (const auto& color : colors) {
        ColorDB::add_color(color.id, color.color_sequence_id, color.red, color.green,
                         color.blue, color.position);
    }

    // Handle SectionDB Animations
    std::vector<std::map<std::string, int>> workspace_section_animations = SectionAnimationDB::fetch_section_animations(scene_id);
    if (!workspace_section_animations.empty()) {
        for (const auto& section_animation : workspace_section_animations) {
            SectionAnimationDB::remove_section_animation(section_animation.at("section_id"), section_animation.at("animation_id"));
        }
    }

    auto section_animations = SectionAnimationDB::fetch_section_animations(scene_id);
    for (const auto& section_animation : section_animations) {
        SectionAnimationDB::add_section_animation(section_animation.at("id"), section_animation.at("section_id"), 
                                                 section_animation.at("color_sequence_id"), section_animation.at("animation_id"));
    }

    return true;
}

// Save a scene with all its workspace data
bool SceneDB::save_scene(int scene_id) {
    bool success = false;

    // Handle SectionDB Animations
    auto section_animations = SectionAnimationDB::fetch_section_animations(scene_id);
    for (const auto& section_animation : section_animations) {
        SectionAnimationDB::remove_section_animation(section_animation.at("section_id"), section_animation.at("animation_id"));
    }

    // Handle Sections
    auto sections = SectionDB::fetch_sections(scene_id);
    for (const auto& section : sections) {
        SectionDB::remove_section(std::get<int>(section.at("id")));
    }

    auto workspace_sections = SectionDB::fetch_sections(-1); // Workspace is scene with id = -1
    for (const auto& section : workspace_sections) {
        SectionDB::add_section(std::get<int>(section.at("id")), std::get<std::string>(section.at("name")), 
                              std::get<int>(section.at("start_led")), std::get<int>(section.at("end_led")), scene_id);

        auto workspace_section_animations = SectionAnimationDB::fetch_section_animations(scene_id);
        for (const auto& section_animation : workspace_section_animations) {
            SectionAnimationDB::add_section_animation(section_animation.at("section_id"), section_animation.at("animation_id"), scene_id);
        }
    }

    // Handle ColorDB Sequences
    auto color_sequences = ColorSequenceDB::fetch_color_sequences(scene_id);
    if (!color_sequences.has_value()) {
        for (const auto& color_sequence : color_sequences.value()) {
            ColorSequenceDB::remove_color_sequence(color_sequence.id);
        }
    }

    auto workspace_color_sequences = ColorSequenceDB::fetch_color_sequences(-1);
    if (workspace_color_sequences.has_value()) {
        for (const auto& color_sequence : workspace_color_sequences.value()) {
            ColorSequenceDB::add_color_sequence(color_sequence.id, color_sequence.name, color_sequence.description, 
                                              color_sequence.selection, color_sequence.color_amount, scene_id);
        }
    }

    // Handle Colors
    auto colors = ColorDB::fetch_colors(scene_id);
    for (const auto& color : colors) {
        ColorDB::remove_color(color.id);
    }

    auto workspace_colors = ColorDB::fetch_colors(-1);
    for (const auto& color : workspace_colors) {
        ColorDB::add_color(color.id, color.color_sequence_id, color.position, color.red, color.green, color.blue, scene_id);
    }

    return true;
}
