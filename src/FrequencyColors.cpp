#pragma once

#include "FrequencyColors.hpp"

#include "util/database/FrequencyColorDB.hpp"
#include "util/database/Database.hpp"

FrequencyColors::FrequencyColors(std::optional<int> scene_id,
                                 std::optional<int> color_sequence_id_1,
                                 std::optional<int> color_sequence_id_2,
                                 std::optional<int> color_sequence_id_3)
    : scene_id(scene_id.value_or(-1))
{
    if (scene_id && color_sequence_id_1 && color_sequence_id_2 && color_sequence_id_3) {
        this->color_sequence_id_1 = color_sequence_id_1.value();
        this->color_sequence_id_2 = color_sequence_id_2.value();
        this->color_sequence_id_3 = color_sequence_id_3.value();
    }
    else if (scene_id) {
        auto freq_color_data = FrequencyColorDB::fetch_frequency_color(scene_id.value());

        this->color_sequence_id_1 = 0;
        this->color_sequence_id_2 = 0;
        this->color_sequence_id_3 = 0;
        this->sync_changes_to_db(true);
    }
}

bool FrequencyColors::sync_changes_to_db(bool is_new) {
    if (is_new) {
        return FrequencyColorDB::add_frequency_color(this->scene_id,
                                                     this->color_sequence_id_1,
                                                     this->color_sequence_id_2,
                                                     this->color_sequence_id_3);
    }

    return FrequencyColorDB::update_frequency_color(this->scene_id,
                                                    this->color_sequence_id_1,
                                                    this->color_sequence_id_2,
                                                    this->color_sequence_id_3);
}
