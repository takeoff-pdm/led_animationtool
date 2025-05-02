#include "SectionDB.hpp"
#include "Database.hpp"
#include "SectionAnimationDB.hpp"

// Helper function to recreate a section from raw data
std::map<std::string, std::variant<std::string, int>> SectionDB::recreate_section(const std::vector<std::string>& section_data) {
    return {
        {"id", std::stoi(section_data[0])},
        {"name", section_data[1]},
        {"start_led", std::stoi(section_data[2])},
        {"end_led", std::stoi(section_data[3])}
    };
}

// Add a section to the database
bool SectionDB::add_section(int id, const std::string& name, int start_led, int end_led, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"scene_id", scene_id},
        {"id", id},
        {"name", name}, // Store the name as an int for simplicity, this may need a different data type
        {"start_led", start_led},
        {"end_led", end_led}
    };

    std::string sql = "INSERT INTO sections VALUES(:scene_id, :id, :name, :start_led, :end_led)";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    // Add section animations
    if (!SectionAnimationDB::add_section_animations(id, scene_id)) {
        return false;
    }

    return true;
}

// Remove a section from the database
bool SectionDB::remove_section(int id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"id", id},
        {"scene_id", scene_id}
    };

    std::string sql = "DELETE FROM sections WHERE scene_id = :scene_id AND id = :id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Update a section in the database
bool SectionDB::update_section(int id, const std::string& name, int start_led, int end_led, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"id", id},
        {"name", name},
        {"start_led", start_led},
        {"end_led", end_led},
        {"scene_id", scene_id}
    };

    std::string sql = "UPDATE sections SET name = :name, start_led = :start_led, end_led = :end_led \
                       WHERE scene_id = :scene_id AND id = :id";

    if (!Database::push_to_db(sql, params)) {
        return false;
    }

    return true;
}

// Fetch a section from the database
std::map<std::string, std::variant<std::string, int>> SectionDB::fetch_section(int id, int scene_id) {
    std::unordered_map<std::string, std::variant<int, std::string>> params = {
        {"id", id},
        {"scene_id", scene_id}
    };

    std::string sql = "SELECT id, name, start_led, end_led FROM sections WHERE scene_id = :scene_id AND id = :id";

    auto section_data = Database::fetchone_from_db(sql, params);

    if (section_data.empty()) {
        return {};
    }

    return recreate_section(section_data);
}

// Fetch all sections from the database for a specific scene
std::vector<std::map<std::string, std::variant<std::string, int>>> SectionDB::fetch_sections(int scene_id) {
    std::vector<std::map<std::string, std::variant<std::string, int>>> sections;

    std::unordered_map<std::string, std::variant<int, std::string>> params = {{"scene_id", scene_id}};
    std::string sql = "SELECT id, name, start_led, end_led FROM sections WHERE scene_id = :scene_id";

    auto sections_data = Database::fetchall_from_db(sql, params);

    if (sections_data.empty()) {
        return sections;
    }

    for (const auto& section_data : sections_data) {
        sections.push_back(recreate_section(section_data));
    }

    return sections;
}
