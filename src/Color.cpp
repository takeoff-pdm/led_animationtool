#include "Color.hpp"
#include "util/database/ColorDB.hpp"
#include "util/database/Database.hpp"

Color::Color(std::optional<int> id, 
             std::optional<int> color_sequence_id, 
             std::optional<int> position, 
             std::optional<int> red, 
             std::optional<int> green, 
             std::optional<int> blue) {
    if (id) {
        auto color_data = ColorDB::fetch_color(id.value());  // From ColorDB
        
        // Might be a problem here
        this->id = color_data.id;
        this->color_sequence_id = color_data.color_sequence_id;
        this->position = color_data.position;
        this->red = color_data.red;
        this->green = color_data.green;
        this->blue = color_data.blue;
    } else if (color_sequence_id && red && green && blue) {
        this->color_sequence_id = color_sequence_id.value();
        this->red = red.value();
        this->green = green.value();
        this->blue = blue.value();
    }
}

bool Color::sync_changes_to_db(bool is_new) {
    if (is_new) {
        auto response = Database::fetchone_from_db("SELECT MAX(id) FROM color_sequence_colors;", {});
        if (!response.empty()) {
            int max_id = std::stoi(response[0]);

            if (max_id < 0) {
                max_id = 0;
            }
            this->id = max_id + 1;
        } else {
            this->id = 0; // Start from 0 if no colors exist
        }
        
        return ColorDB::add_color(this->id, this->color_sequence_id, this->position, this->red, this->green, this->blue);
    } else {
        return ColorDB::update_color(this->id, this->color_sequence_id, this->position, this->red, this->green, this->blue);
    }
}
