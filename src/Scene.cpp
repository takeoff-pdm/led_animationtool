#include "Scene.hpp"

#include "util/database/SceneDB.hpp"
#include "util/database/SceneAnimationDB.hpp"
#include "util/database/Database.hpp"
#include "animation/Animation.hpp"

Scene::Scene(std::optional<int> id,
             std::optional<std::string> name,
             std::optional<std::string> description,
             std::optional<std::vector<std::map<std::string, int>>> scene_animations)
    : id(id.value_or(-1)), 
      scene_animations(scene_animations ? 
                       *scene_animations 
                       : std::vector<std::map<std::string, int>>())
{
    if (name.has_value() && description.has_value()) {
        this->name = name.value_or("");;
        this->description = description.value_or("");;
    } else if (id) {
        auto scene_data = SceneDB::fetch_scene(id.value());

        this->name = scene_data["name"];
        this->description = scene_data["description"];
    }

    if (this->scene_animations.empty() && this->id >= 0) {
        auto animations = SceneAnimationDB::fetch_scene_animations_from_scene(this->id);
        
        this->scene_animations = animations;
    }
}

bool Scene::sync_changes_to_db(bool is_new) {
    if (is_new) {
        auto response = Database::fetchone_from_db("SELECT MAX(id) FROM scenes;", {});
        
        if (!response.empty()) {
            int max_id = std::stoi(response[0]);

            if (max_id < 0) {
                max_id = 0;
            }
            this->id = max_id + 1;
        } else {
            this->id = 0; // Start from 0 if no scenes exist
        }

        return SceneDB::add_scene(this->id, this->name, this->description);
    }

    return SceneDB::update_scene(this->id, this->name, this->description);
}

std::optional<std::vector<std::map<std::string, int>>> Scene::load() {
    if (!SceneDB::load_scene(this->id)) {
        return std::nullopt;
    }

    return std::optional{this->scene_animations};
}

bool Scene::save(const std::vector<std::map<std::string, int>>& running_animations) {
    SceneAnimationDB::remove_scene_animations(this->id);

    for (const auto& animation : running_animations) {
        SceneAnimationDB::add_scene_animation(
            this->id,
            animation.at("id"),
            animation.at("section_id"),
            animation.at("color_sequence_id")
        );
    }

    if (this->scene_animations.empty()) {
        auto animations = SceneAnimationDB::fetch_scene_animations_from_scene(this->id);
        this->scene_animations = animations;
    }

    return SceneDB::save_scene(this->id);
}
