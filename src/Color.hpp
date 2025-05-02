// Color.hpp
#pragma once

#include <optional>
#include "util/database/ColorDB.hpp"

class Color {
public:
    Color(std::optional<int> id = std::nullopt, 
          std::optional<int> color_sequence_id = std::nullopt, 
          std::optional<int> position = std::nullopt, 
          std::optional<int> red = std::nullopt, 
          std::optional<int> green = std::nullopt, 
          std::optional<int> blue = std::nullopt);

    bool sync_changes_to_db(bool is_new = false);

    int id;
    int color_sequence_id;
    int position;
    int red;
    int green;
    int blue;
};
