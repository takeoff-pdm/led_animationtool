#pragma once

#include <map>
#include <vector>

class SceneAnimationDB {
public:
    static bool add_scene_animation(int scene_id, int animation_id, int section_id, int color_sequence_id);
    static bool remove_scene_animations(int scene_id);
    static bool remove_scene_animation(int scene_id, int animation_id);
    static bool update_scene_animation(int scene_id, int animation_id, int section_id, int color_sequence_id);
    static std::vector<std::map<std::string, int>> fetch_scene_animations();
    static std::vector<std::map<std::string, int>> fetch_scene_animations_from_scene(int scene_id);
    static std::map<std::string, int> fetch_scene_animation(int scene_id, int animation_id);

private:
    static std::map<std::string, int> recreate_scene_animation(const std::vector<std::string>& scene_animation_data);
};
