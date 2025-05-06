#include "ColorDB.hpp"
#include "Database.hpp"
#include <iostream>
#include <string>
#include <vector>

// Helper function to recreate a color object from the database result
ColorDB ColorDB::recreate_color(const std::vector<std::string>& color_data) {
    // return ColorDB(
    //     std::stoi(color_data[0]), // id
    //     std::stoi(color_data[1]), // color_sequence_id
    //     std::stoi(color_data[2]), // position
    //     std::stoi(color_data[3]), // red
    //     std::stoi(color_data[4]), // green
    //     std::stoi(color_data[5])  // blue
    // );

    ColorDB color;
    color.id = std::stoi(color_data[0]);
    color.color_sequence_id = std::stoi(color_data[1]);
    color.position = std::stoi(color_data[2]);
    color.red = std::stoi(color_data[3]);
    color.green = std::stoi(color_data[4]);
    color.blue = std::stoi(color_data[5]);
    return color;
}

// Add a new color to the database
bool ColorDB::add_color(int id, int color_sequence_id, int position, int red, int green, int blue, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"color_sequence_id", color_sequence_id},
        {"position", position},
        {"red", red},
        {"green", green},
        {"blue", blue},
        {"scene_id", scene_id}
    };

    return Database::push_to_db("INSERT INTO colors VALUES(:scene_id, :id, :color_sequence_id, :position, :red, :green, :blue)", data);
}

// Remove a color from the database
bool ColorDB::remove_color(int id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"scene_id", scene_id}
    };

    return Database::push_to_db("DELETE FROM colors WHERE scene_id = :scene_id AND id = :id", data);
}

// Update a color in the database
bool ColorDB::update_color(int id, int color_sequence_id, int position, int red, int green, int blue, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"id", id},
        {"color_sequence_id", color_sequence_id},
        {"position", position},
        {"red", red},
        {"green", green},
        {"blue", blue},
        {"scene_id", scene_id}
    };

    return Database::push_to_db(
        "UPDATE colors SET color_sequence_id = :color_sequence_id, position = :position, red = :red, green = :green, blue = :blue WHERE scene_id = :scene_id AND id = :id", data);
}

// Fetch all colors for a given scene
std::vector<ColorDB> ColorDB::fetch_colors(int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {{"scene_id", scene_id}};
    auto colors_data = Database::fetchall_from_db("SELECT id, color_sequence_id, position, red, green, blue FROM colors WHERE scene_id = :scene_id", data);

    if (colors_data.empty()) {
        return {}; // return empty vector if no colors found
    }

    std::vector<ColorDB> colors;
    for (const auto& color_data : colors_data) {
        colors.push_back(recreate_color(color_data));
    }

    return colors;
}

// Fetch colors from a specific color sequence
std::vector<ColorDB> ColorDB::fetch_colors_from_sequence(int id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {
        {"color_sequence_id", id},
        {"scene_id", scene_id}
    };

    auto colors_data = Database::fetchall_from_db(
        "SELECT id, color_sequence_id, position, red, green, blue FROM colors WHERE scene_id = :scene_id AND color_sequence_id = :color_sequence_id", data);

    if (colors_data.empty()) {
        return {}; // return empty vector if no colors found
    }

    std::vector<ColorDB> colors;
    for (const auto& color_data : colors_data) {
        colors.push_back(recreate_color(color_data));
    }

    return colors;
}

// Fetch a single color by id
ColorDB ColorDB::fetch_color(int id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> data = {{"id", id}, {"scene_id", scene_id}};
    auto color_data = Database::fetchone_from_db(
        "SELECT id, color_sequence_id, position, red, green, blue FROM colors WHERE scene_id = :scene_id OR scene_id = -1 AND id = :id", data);

    if (color_data.empty()) {
        ColorDB color;
        color.id = -1; // Set an invalid id to indicate not found
        color.color_sequence_id = -1; // Set an invalid color_sequence_id to indicate not found
        color.position = -1; // Set an invalid position to indicate not found
        color.red = -1; // Set an invalid red value to indicate not found
        color.green = -1; // Set an invalid green value to indicate not found
        color.blue = -1; // Set an invalid blue value to indicate not found

        return color; // return an invalid color if not found
    }

    return recreate_color(color_data);
}
