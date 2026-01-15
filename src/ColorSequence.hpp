#pragma once
#include <string>
#include <vector>
#include <optional>
#include "Color.hpp"

class ColorSequence {
public:
    int id;
    std::string name;
    std::string description;
    int selection;
    int color_amount;

    ColorSequence(std::optional<int> id = std::nullopt,
                  std::optional<std::string> name = std::nullopt,
                  std::optional<std::string> description = std::nullopt,
                  std::optional<int> selection = std::nullopt,
                  std::optional<int> color_amount = std::nullopt);

    bool sync_changes_to_db(bool is_new = false);
    std::vector<Color>& colors();
    void update_colors();
    bool add_color(Color color);
    bool remove_color(int id);
    void set_runtime_colors(std::vector<Color> colors);

private:
    std::vector<Color> color_list;
};
