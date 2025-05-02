#include "Section.hpp"
#include "util/database/SectionDB.hpp"
#include "util/database/Database.hpp"
#include <variant>

Section::Section(std::optional<int> id, 
                 std::optional<std::string> name, 
                 std::optional<int> start_led, 
                 std::optional<int> end_led) {
    if (id) {
        auto section_data = SectionDB::fetch_section(id.value());

        if (!section_data.empty()) {
            // Use std::get<int/string> to extract from variant
            if (section_data.count("id") && std::holds_alternative<int>(section_data["id"])) {
                this->id = std::get<int>(section_data["id"]);
            }

            if (section_data.count("name") && std::holds_alternative<std::string>(section_data["name"])) {
                this->name = std::get<std::string>(section_data["name"]);
            }

            if (section_data.count("start_led") && std::holds_alternative<int>(section_data["start_led"])) {
                this->start_led = std::get<int>(section_data["start_led"]);
            }

            if (section_data.count("end_led") && std::holds_alternative<int>(section_data["end_led"])) {
                this->end_led = std::get<int>(section_data["end_led"]);
            }
        }
    } else if (name && start_led && end_led) {
        this->name = name.value();
        this->start_led = start_led.value();
        this->end_led = end_led.value();
    }
}

bool Section::sync_changes_to_db(bool is_new) {
    if (is_new) {
        auto response = Database::fetchone_from_db("SELECT MAX(id) FROM sections;", {});
        
        if (!response.empty()) {
            int max_id = -1;
            if (response[0] != "NULL") {
                max_id = std::stoi(response[0]);
            }

            if (max_id < 0) {
                max_id = 0;
            }
            this->id = max_id + 1;
        } else {
            this->id = 0;
        }
        
        return SectionDB::add_section(this->id, this->name, this->start_led, this->end_led);
    } else {
        return SectionDB::update_section(this->id, this->name, this->start_led, this->end_led);
    }
}
