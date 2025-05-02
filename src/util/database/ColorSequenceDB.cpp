#include "ColorSequenceDB.hpp"
#include <iostream>

ColorSequenceDB ColorSequenceDB::recreate_color_sequence(const std::vector<std::string>& color_sequence_data) {

    /// Check if the data is valid
    if (color_sequence_data.size() < 5) {
        std::cout << "[ColorSequenceDB] Error: Invalid data size." << std::endl;
        return ColorSequenceDB{}; // Return an empty object or handle the error as needed
    }

    // Check if ints can be converted from strings
    for (size_t i = 0; i < color_sequence_data.size(); ++i) {
        if (i == 0 || i == 3 || i == 4 || i == 5) { // Assuming these are the indices for int values
            try {
                std::stoi(color_sequence_data[i]);
            } catch (const std::invalid_argument&) {
                std::cout << "[ColorSequenceDB] Error: Invalid integer conversion." << std::endl;
                return ColorSequenceDB{}; // Return an empty object or handle the error as needed
            }
        }
    }

    ColorSequenceDB color_sequence;
    color_sequence.id = std::stoi(color_sequence_data[0]);
    color_sequence.name = color_sequence_data[1];
    color_sequence.description = color_sequence_data[2];
    color_sequence.selection = std::stoi(color_sequence_data[3]);
    color_sequence.color_amount = std::stoi(color_sequence_data[4]);
    // color_sequence.scene_id = std::stoi(color_sequence_data[5]);

    // Print all values for debugging
    std::cout << "[ColorSequenceDB] Recreated ColorSequenceDB: " << std::endl;
    std::cout << "ID: " << color_sequence.id << std::endl;
    std::cout << "Name: " << color_sequence.name << std::endl;
    std::cout << "Description: " << color_sequence.description << std::endl;
    std::cout << "Selection: " << color_sequence.selection << std::endl;
    std::cout << "Color Amount: " << color_sequence.color_amount << std::endl;

    return color_sequence;
}

bool ColorSequenceDB::add_color_sequence(int id, const std::string& name, const std::string& description,
                                       int selection, int color_amount, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"name", name},
        {"description", description},
        {"selection", selection},
        {"color_amount", color_amount},
        {"scene_id", scene_id}
    };
    return Database::push_to_db("INSERT INTO color_sequences VALUES(:scene_id, :id, :name, :description, :selection, :color_amount)", data);
}

bool ColorSequenceDB::remove_color_sequence(int id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"scene_id", scene_id}
    };
    return Database::push_to_db("DELETE FROM color_sequences WHERE scene_id = :scene_id AND id = :id", data);
}

bool ColorSequenceDB::update_color_sequence(int id, const std::string& name, const std::string& description,
                                          int selection, int color_amount, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"name", name},
        {"description", description},
        {"selection", selection},
        {"color_amount", color_amount},
        {"scene_id", scene_id}
    };
    return Database::push_to_db("UPDATE color_sequences SET name = :name, description = :description, \
                                selection = :selection, color_amount = :color_amount WHERE scene_id = :scene_id AND id = :id", data);
}

std::optional<std::vector<ColorSequenceDB>> ColorSequenceDB::fetch_color_sequences(int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"scene_id", scene_id}
    };
    auto color_sequences_data = Database::fetchall_from_db("SELECT id, name, description, selection, color_amount FROM color_sequences WHERE scene_id = :scene_id", data);

    if (color_sequences_data.empty()) return std::nullopt;

    std::vector<ColorSequenceDB> color_sequences;
    for (const auto& color_sequence_data : color_sequences_data) {
        color_sequences.push_back(recreate_color_sequence(color_sequence_data));
    }
    return color_sequences;
}

std::optional<ColorSequenceDB> ColorSequenceDB::fetch_color_sequence(int id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"scene_id", scene_id}
    };
    auto color_sequence_data = Database::fetchone_from_db("SELECT id, name, description, selection, color_amount, scene_id FROM color_sequences WHERE scene_id = :scene_id AND id = :id", data);

    if (color_sequence_data.empty()) return std::nullopt;

    return recreate_color_sequence(color_sequence_data);
}
