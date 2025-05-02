#pragma once

#include "Database.hpp"
#include <string>
#include <vector>
#include <optional>
#include <map>
#include <variant>

class ColorSequenceDB {
public:
    int id;
    std::string name;
    std::string description;
    int selection;
    int color_amount;
    int scene_id;

    // Public methods to interact with the database
    static bool add_color_sequence(int id, const std::string& name, const std::string& description,
                                   int selection, int color_amount, int scene_id = -1);
    static bool remove_color_sequence(int id, int scene_id = -1);
    static bool update_color_sequence(int id, const std::string& name, const std::string& description,
                                      int selection, int color_amount, int scene_id = -1);
    static std::optional<std::vector<ColorSequenceDB>> fetch_color_sequences(int scene_id = -1);
    static std::optional<ColorSequenceDB> fetch_color_sequence(int id, int scene_id = -1);

private:
    // Private helper method to convert raw data into a ColorSequenceDB structure
    static ColorSequenceDB recreate_color_sequence(const std::vector<std::string>& color_sequence_data);
};
