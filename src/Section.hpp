#pragma once

#include <string>
#include <optional>
#include "util/database/SectionDB.hpp"

class Section {
public:
    int id;
    std::string name;
    int start_led;
    int end_led;

    Section(std::optional<int> id = std::nullopt, 
            std::optional<std::string> name = std::nullopt, 
            std::optional<int> start_led = std::nullopt, 
            std::optional<int> end_led = std::nullopt);

    bool sync_changes_to_db(bool is_new = false);
};
