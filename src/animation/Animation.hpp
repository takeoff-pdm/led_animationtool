#pragma once

#include "../util/database/SectionAnimationDB.hpp"
#include "../util/database/AnimationDB.hpp"
#include "../util/database/Database.hpp"
#include "../Color.hpp"
#include "../ColorSequence.hpp"

#define ANIMATION_STEPS 30

class Strip;

class Animation {
public:
    int id;
    int section_id;
    std::string name;
    std::string description;
    int variation;
    int direction;
    int offset;
    int bpm;
    int start_led;
    int end_led;
    float brightness;
    std::shared_ptr<ColorSequence> color_sequence;
    Strip* strip;

    Animation(int id = -1, int section_id = 0, std::string name = "", std::string description = "", int variation = 0, int direction = 0, int offset = 0);

    bool sync_changes_to_db(bool is_new = false);

    float sleep_time() const;

    void set_pixel_color(int pixel, int red, int green, int blue);

    void color_wipe(Color color);

    Color wheel(int pos);

    std::vector<Color> select_colors(int beat);

    std::vector<int> color_transition(int color, int next_color);

    Color black();

    virtual void animate(int beat, int step);
};
