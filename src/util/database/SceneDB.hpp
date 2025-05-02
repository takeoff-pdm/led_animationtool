#pragma once

#include <map>
#include <vector>

class SceneDB {
public:
    // SceneDB CRUD Operations
    static bool add_scene(int id, const std::string& name, const std::string& description);
    static bool remove_scene(int id);
    static bool update_scene(int id, const std::string& name, const std::string& description);
    static std::vector<std::map<std::string, std::string>> fetch_scenes();
    static std::map<std::string, std::string> fetch_scene(int id);

    // SceneDB Management Methods
    static bool load_scene(int scene_id);
    static bool save_scene(int scene_id);

private:
    // Helper function to recreate a scene from data
    static std::map<std::string, std::string> recreate_scene(const std::vector<std::string>& scene_data);
};
