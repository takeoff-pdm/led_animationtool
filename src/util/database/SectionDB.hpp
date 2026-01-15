#pragma once

#include <map>
#include <vector>
#include <string>
#include <variant>

class SectionDB {
public:
    // SectionDB CRUD Operations
    static bool add_section(int id, const std::string& name, int start_led, int end_led, int scene_id = -1);
    static bool remove_section(int id, int scene_id = -1);
    static bool update_section(int id, const std::string& name, int start_led, int end_led, int scene_id = -1);
    static std::map<std::string, std::variant<std::string, int>> fetch_section(int id, int scene_id = -1);
    static std::vector<std::map<std::string, std::variant<std::string, int>>> fetch_sections(int scene_id = -1);

private:
    // Helper function to recreate a section from data
    static std::map<std::string, std::variant<std::string, int>> recreate_section(const std::vector<std::string>& section_data);
};
