#pragma once

#include <string>
#include <vector>
#include <optional>
#include <tuple>

#include "util/database/SceneDB.hpp"
#include "util/database/SceneAnimationDB.hpp"

class Scene {
public:
    int id;
    std::string name;
    std::string description;
    std::vector<std::map<std::string, int>> scene_animations;  // or a custom struct if needed

    Scene(std::optional<int> id = std::nullopt,
          std::optional<std::string> name = std::nullopt,
          std::optional<std::string> description = std::nullopt,
          std::optional<std::vector<std::map<std::string, int>>> scene_animations = {});

    bool sync_changes_to_db(bool is_new = false);
    std::optional<std::vector<std::map<std::string, int>>> load();
    bool save(const std::vector<std::map<std::string, int>>& running_animations);
};
