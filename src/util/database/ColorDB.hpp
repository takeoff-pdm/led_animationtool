#pragma once

#include <unordered_map>
#include <vector>

class ColorDB {
public:
    int id;
    int color_sequence_id;
    int position;
    int red;
    int green;
    int blue;
    
    // ColorDB(int id, int color_sequence_id, int position, int red, int green, int blue)
    //     : id(id), color_sequence_id(color_sequence_id), position(position), red(red), green(green), blue(blue) {}

    static ColorDB recreate_color(const std::vector<std::string>& color_data);
    static bool add_color(int id, int color_sequence_id, int position, int red, int green, int blue, int scene_id = -1);
    static bool remove_color(int id, int scene_id = -1);
    static bool update_color(int id, int color_sequence_id, int position, int red, int green, int blue, int scene_id = -1);
    static std::vector<ColorDB> fetch_colors(int scene_id = -1);
    static std::vector<ColorDB> fetch_colors_from_sequence(int id, int scene_id = -1);
    static ColorDB fetch_color(int id, int scene_id = -1);
};
