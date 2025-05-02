#include "AnimationDB.hpp"
#include <iostream>
#include <map>
#include <optional>
#include <variant>

AnimationDB AnimationDB::recreate_animation(const std::vector<std::string>& animation_data) {
    // return {std::stoi(animation_data[0]), animation_data[1], animation_data[2]};
    AnimationDB animation;
    animation.id = std::stoi(animation_data[0]);
    animation.name = animation_data[1];
    animation.description = animation_data[2];

    return animation;
}

bool AnimationDB::add_animation(int id, const std::string& name, const std::string& description) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"name", name},
        {"description", description}
    };

    return Database::push_to_db("INSERT INTO animations VALUES(:id, :name, :description)", data);
}

bool AnimationDB::remove_animation(int id) {
    // Use unordered_map instead of map
    std::unordered_map<std::string, std::variant<int, std::string>> data = {{"id", id}};
    return Database::push_to_db("DELETE FROM animations WHERE id = :id", data);
}

bool AnimationDB::update_animation(int id, const std::string& name, const std::string& description) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"name", name},
        {"description", description}
    };
    return Database::push_to_db("UPDATE animations SET name = :name, description = :description WHERE id = :id", data);
}

std::optional<std::vector<AnimationDB>> AnimationDB::fetch_animations() {
    std::vector<std::vector<std::string>> animations_data = Database::fetchall_from_db("SELECT id, name, description FROM animations", {});

    if (animations_data.empty()) return std::nullopt;

    std::vector<AnimationDB> animations;
    for (const auto& animation_data : animations_data) {
        animations.push_back(recreate_animation(animation_data));
    }
    return animations;
}

std::optional<AnimationDB> AnimationDB::fetch_animation(int id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {{"id", id}};
    std::vector<std::string> animation_data = Database::fetchone_from_db("SELECT id, name, description FROM animations WHERE id = :id", data);

    if (animation_data.empty()) return std::nullopt;

    return recreate_animation(animation_data);
}
