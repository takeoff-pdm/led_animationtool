#include "FrequencyColorDB.hpp"
#include "Database.hpp"
#include <iostream>
#include <string>
#include <vector>

// Helper function to recreate a FrequencyColorDB object from the database result
FrequencyColorDB FrequencyColorDB::recreate_frequency_color(const std::vector<std::string>& frequency_color_data) {
    return FrequencyColorDB(
        std::stoi(frequency_color_data[0]), // scene_id
        std::stoi(frequency_color_data[1]), // color_sequence_id_1
        std::stoi(frequency_color_data[2]), // color_sequence_id_2
        std::stoi(frequency_color_data[3])  // color_sequence_id_3
    );
}

// Add a new frequency color to the database
bool FrequencyColorDB::add_frequency_color(int scene_id, int color_sequence_id_1, int color_sequence_id_2, int color_sequence_id_3) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"scene_id", scene_id},
        {"color_sequence_id_1", color_sequence_id_1},
        {"color_sequence_id_2", color_sequence_id_2},
        {"color_sequence_id_3", color_sequence_id_3}
    };

    return Database::push_to_db(
        "INSERT INTO frequency_colors VALUES(:scene_id, :color_sequence_id_1, :color_sequence_id_2, :color_sequence_id_3)", data);
}

// Remove a frequency color from the database
bool FrequencyColorDB::remove_frequency_color(int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {{"scene_id", scene_id}};
    
    return Database::push_to_db("DELETE FROM frequency_colors WHERE scene_id = :scene_id", data);
}

// Update a frequency color in the database
bool FrequencyColorDB::update_frequency_color(int scene_id, int color_sequence_id_1, int color_sequence_id_2, int color_sequence_id_3) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"scene_id", scene_id},
        {"color_sequence_id_1", color_sequence_id_1},
        {"color_sequence_id_2", color_sequence_id_2},
        {"color_sequence_id_3", color_sequence_id_3}
    };

    return Database::push_to_db(
        "UPDATE frequency_colors SET scene_id = :scene_id, color_sequence_id_1 = :color_sequence_id_1, \
         color_sequence_id_2 = :color_sequence_id_2, color_sequence_id_3 = :color_sequence_id_3 WHERE scene_id = :scene_id", data);
}

// Fetch all frequency colors for a given scene
std::vector<FrequencyColorDB> FrequencyColorDB::fetch_frequency_colors(int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {{"scene_id", scene_id}};
    
    auto frequency_colors_data = Database::fetchall_from_db(
        "SELECT scene_id, color_sequence_id_1, color_sequence_id_2, color_sequence_id_3 FROM frequency_colors WHERE scene_id = :scene_id", data);
    
    if (frequency_colors_data.empty()) {
        return {}; // return empty vector if no frequency colors found
    }

    std::vector<FrequencyColorDB> frequency_colors;
    for (const auto& frequency_color_data : frequency_colors_data) {
        frequency_colors.push_back(recreate_frequency_color(frequency_color_data));
    }

    return frequency_colors;
}

// Fetch a single frequency color by scene_id
FrequencyColorDB FrequencyColorDB::fetch_frequency_color(int id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {{"scene_id", scene_id}};
    
    auto frequency_color_data = Database::fetchone_from_db(
        "SELECT scene_id, color_sequence_id_1, color_sequence_id_2, color_sequence_id_3 FROM frequency_colors WHERE scene_id = :scene_id", data);
    
    if (frequency_color_data.empty()) {
        return FrequencyColorDB(-1, -1, -1, -1); // return an invalid frequency color if not found
    }

    return recreate_frequency_color(frequency_color_data);
}
