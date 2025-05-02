#include <algorithm>

#include "ColorSequence.hpp"
#include "Color.hpp"

#include "util/database/ColorSequenceDB.hpp"
#include "util/database/ColorDB.hpp"
#include "util/database/Database.hpp"

ColorSequence::ColorSequence(std::optional<int> id,
                             std::optional<std::string> name,
                             std::optional<std::string> description,
                             std::optional<int> selection,
                             std::optional<int> color_amount)
                             : id(id.value_or(0)), color_list({})
{
    if (name && description && selection && color_amount) {
        this->name = name.value();
        this->description = description.value();
        this->selection = selection.value();
        this->color_amount = color_amount.value();
    }
    else if (id) {
        auto cs_data = ColorSequenceDB::fetch_color_sequence(id.value());

        if (cs_data.has_value()) {
            this->name = cs_data->name;
            this->description = cs_data->description;
            this->selection = cs_data->selection;
            this->color_amount = cs_data->color_amount;
        }
    }
}

bool ColorSequence::sync_changes_to_db(bool is_new) {
    if (is_new) {
        auto response = Database::fetchone_from_db("SELECT MAX(id) FROM color_sequences;", {});

        if (!response.empty()) {  
            int max_id = -1;
            if (response[0] != "NULL") {
                max_id = std::stoi(response[0]);
            }

            if (max_id < 0) {
                max_id = -1;
            }
            this->id = max_id + 1;
        } else {
            this->id = 0; // Start from 0 if no color sequences exist
        }

        return ColorSequenceDB::add_color_sequence(this->id,
                                                    this->name,
                                                    this->description,
                                                    this->selection,
                                                    this->color_amount);
    }

    return ColorSequenceDB::update_color_sequence(this->id,
                                                  this->name,
                                                  this->description,
                                                  this->selection,
                                                  this->color_amount);
}

std::vector<Color>& ColorSequence::colors() {
    if (!color_list.empty()) {
        return color_list;
    }

    auto colors_data = ColorDB::fetch_colors_from_sequence(this->id);

    for (const auto& data : colors_data) {
        color_list.emplace_back(Color(-1,
                                    data.color_sequence_id,
                                    data.position,
                                    data.red,
                                    data.green,
                                    data.blue));
    }

    return color_list;
}

void ColorSequence::update_colors() {
    color_list.clear();
    this->colors();  // Re-fetch
}

bool ColorSequence::add_color(Color color) {
    auto& current_colors = colors();

    color.position = static_cast<int>(current_colors.size());

    if (!color.sync_changes_to_db(true)) {
        return false;
    }

    color_list.push_back(color);
    return true;
}

bool ColorSequence::remove_color(int id) {
    auto it = remove_if(color_list.begin(), color_list.end(),
                             [id](const Color& color) { return color.id == id; });

    if (it != color_list.end()) {
        color_list.erase(it, color_list.end());
        ColorDB::remove_color(id);
        return true;
    }

    return false;
}
