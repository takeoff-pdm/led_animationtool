#pragma once

#include <unordered_map>
#include <vector>
#include <string>

class FrequencyColorDB {
public:
    int scene_id;
    int color_sequence_id_1;
    int color_sequence_id_2;
    int color_sequence_id_3;
    
    FrequencyColorDB(int scene_id, int color_sequence_id_1, int color_sequence_id_2, int color_sequence_id_3)
        : scene_id(scene_id), color_sequence_id_1(color_sequence_id_1), color_sequence_id_2(color_sequence_id_2), color_sequence_id_3(color_sequence_id_3) {}

    static FrequencyColorDB recreate_frequency_color(const std::vector<std::string>& frequency_color_data);
    static bool add_frequency_color(int scene_id, int color_sequence_id_1, int color_sequence_id_2, int color_sequence_id_3);
    static bool remove_frequency_color(int scene_id = -1);
    static bool update_frequency_color(int scene_id, int color_sequence_id_1, int color_sequence_id_2, int color_sequence_id_3);
    static std::vector<FrequencyColorDB> fetch_frequency_colors(int scene_id = -1);
    static FrequencyColorDB fetch_frequency_color(int id, int scene_id = -1);
};
