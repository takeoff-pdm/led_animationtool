#include "Animation.hpp"
#include "../Strip.hpp"
#include "../util/database/SectionAnimationDB.hpp"
#include "../util/database/AnimationDB.hpp"
#include "../util/database/Database.hpp"
#include "Color.hpp"
#include "ColorSequence.hpp"

#define ANIMATION_STEPS 30

Animation::Animation(int id, int section_id, std::string name, std::string description, int variation, int direction, int offset)
    : id(id), section_id(section_id), name(name), description(description), variation(variation), direction(direction), offset(offset), 
      bpm(1), start_led(0), end_led(0), brightness(255), color_sequence(nullptr), strip(nullptr) {
    if (!description.empty()) {
        this->name = name;
        this->description = description;
        this->variation = variation;
        this->direction = direction;
        this->offset = offset;
    } 
    else if (this->id != -1) {
        auto animation_data = AnimationDB::fetch_animation(this->id);

        if (animation_data.has_value()) {
            this->name = animation_data->name;
            this->description = animation_data->description;
        }

        auto section_animation_data = SectionAnimationDB::fetch_section_animation(section_id, this->id);
        
        this->variation = section_animation_data.at("variation");
        this->direction = section_animation_data.at("direction");
        this->offset = section_animation_data.at("offset");
    }
}

bool Animation::sync_changes_to_db(bool is_new) {
    if (is_new) {
        std::vector<std::string> max_id_res = Database::fetchone_from_db("SELECT MAX(id) FROM animations", {});
        this->id = max_id_res.empty() ? 0 : std::stoi(max_id_res[0]) + 1;
        return AnimationDB::add_animation(this->id, this->name, this->description); // <-- Adjusted to match the function signature
    }

    if (!AnimationDB::update_animation(this->id, this->name, this->description)) {
        return false;
    }

    return SectionAnimationDB::update_section_animation(this->section_id, this->id, this->variation, this->direction, this->offset);
}

float Animation::sleep_time() const {
    return 60.0f / static_cast<float>(bpm);
}

void Animation::set_pixel_color(int pixel, int red, int green, int blue) {
    if (strip) {
        strip->set_pixel_color(pixel, red, green, blue);
    }
}

void Animation::color_wipe(Color color) {
    for (int i = start_led; i <= end_led; i++) {
        if (strip) {
            strip->set_pixel_color(i, color.red, color.green, color.blue);
        }
    }
}

Color Animation::wheel(int pos) {
    if (pos < 85) {
        return Color(pos * 3, 255 - pos * 3, 0);
    } else if (pos < 170) {
        pos -= 85;
        return Color(255 - pos * 3, 0, pos * 3);
    } else {
        pos -= 170;
        return Color(0, pos * 3, 255 - pos * 3);
    }
}

std::vector<Color> Animation::select_colors(int beat) {
    std::vector<Color> colors;

    if (color_sequence == nullptr || color_sequence->colors().empty()) {
        return colors;
    }
    
    // Print colors() list
    for (const auto& color : color_sequence->colors()) {
        std::cout << "Color: " << color.red << ", " << color.green << ", " << color.blue << std::endl;
    }


    for (int x = 0; x < color_sequence->color_amount; x++) {
        int index = color_sequence->selection == 0 
            ? (x + beat * color_sequence->color_amount) % color_sequence->colors().size()
            : (x + beat * color_sequence->selection) % color_sequence->colors().size();

        colors.emplace_back(color_sequence->colors()[index]);
    }

    if (colors.empty()) {
        return { black() };
    }

    return colors;
}

std::vector<int> Animation::color_transition(int color, int next_color) {
    std::vector<int> transition;

    if (color < next_color) {
        int step = std::max((next_color - color) / ANIMATION_STEPS, 1);
        for (int i = color; i < next_color; i += step) {
            transition.push_back(i);
        }
    } else {
        int step = std::max((color - next_color) / ANIMATION_STEPS, 1);
        for (int i = color; i > next_color; i -= step) {
            transition.push_back(i);
        }
    }

    return transition;
}

Color Animation::black() {
    return Color(std::nullopt, std::nullopt, std::nullopt, 0, 0, 0);
}

void Animation::animate(int beat, int step) {}
