#pragma once

#include <map>
#include <vector>
#include <string>

class SectionAnimationDB {
public:
    // Section Animation CRUD Operations
    static bool add_section_animations(int section_id, int scene_id = -1);
    static bool add_section_animation(int section_id, int animation_id, int scene_id = -1, 
                                      int variation = 0, int direction = 0, int offset = 0);
    static bool remove_section_animation(int section_id, int animation_id, int scene_id = -1);
    static bool update_section_animation(int section_id, int animation_id, int variation, int direction, 
                                         int offset, int scene_id = -1);
    static std::map<std::string, int> fetch_section_animation(int section_id, int animation_id, int scene_id = -1);
    static std::vector<std::map<std::string, int>> fetch_section_animations(int section_id, int scene_id = -1);

private:
    // Helper function to recreate a section animation from data
    static std::map<std::string, int> recreate_section_animation(const std::vector<std::string>& section_animation_data);
};
