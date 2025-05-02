#include <vector>
#include <string>
#include <functional>
#include <thread>
#include <atomic>
#include <nlohmann/json.hpp>
#include <ws2811.h>
#include "util/udp/UDP.hpp"
#include "util/database/ColorDB.hpp"
#include "util/database/SectionDB.hpp"
#include "util/database/SceneDB.hpp"
#include "util/database/ColorSequenceDB.hpp"
#include "util/database/SceneAnimationDB.hpp"
#include "util/database/AnimationDB.hpp"
#include "Animation.hpp"
#include "Color.hpp"
#include "ColorSequence.hpp"
#include "Section.hpp"
#include "Scene.hpp"
#include "FrequencyColors.hpp"
// #include "animation/MonoColor.hpp"
// #include "animation/Flow.hpp"
// #include "animation/Shooter.hpp"
#include "animation/Strobe.hpp"
// #include "animation/Squeeze.hpp"

// Class definition for Strip
class Strip {
public:
    Strip();
    
    // Public methods
    void init_strip();
    void restart_strip();
    void create_animations();
    float sleep_time() const;
    void color_wipe(Color color);
    void color_wipe(int color);
    void set_data(const std::vector<char>& new_data);
    void animate(std::function<bool()> stop);
    nlohmann::json fetch_config();
    void update_config(const std::string& key, const nlohmann::json& value);
    void show_strip_handler(std::function<bool()> stop);
    bool set_brightness(int brightness);
    bool set_led_count(int led_count);
    bool set_bpm(int bpm);
    bool add_section(const std::string& name, int start_led, int end_led);
    bool remove_section(int section_id);
    bool update_section(int section_id, const std::string& name, int start_led, int end_led);
    bool add_color_sequence(const std::string& name, const std::string& description, 
                            int selection, int color_amount);
    bool remove_color_sequence(int id);
    bool update_color_sequence(int id, const std::string& name, const std::string& description, 
                               int selection, int color_amount);
    bool add_color(int color_sequence_id, int red, int green, int blue);
    bool remove_color(int id);
    bool update_color(int id, int color_sequence_id, int position, int red, int green, int blue);
    bool update_frequency_color_sequences(int scene_id, int color_sequence_id_1, 
                                          int color_sequence_id_2, int color_sequence_id_3);
    void add_animation(Animation* animation, Section section, ColorSequence color_sequence);
    bool update_animation(int id, int section_id, const std::string& name, const std::string& description,
                          int variation, int direction, int offset);
    bool start_animate(int color_sequence_id, std::optional<Animation*> animation, 
                       int section_id, std::optional<int> animation_id);
    bool stop_animate(int section_id, bool start_new);
    bool add_scene(const std::string& name, const std::string& description);
    bool remove_scene(int scene_id);
    bool update_scene(int id, const std::string& name, const std::string& description);
    bool save_scene(int scene_id);
    bool load_scene(int scene_id);
    nlohmann::json get_frequency_color_sequences() const;
    void set_pixel_color(int pixel, int red, int green, int blue);

    ws2811_t led_string;
    nlohmann::json config;
    std::vector<Section> sections;
    std::vector<ColorSequence> color_sequences;
    std::vector<Scene> scenes;
    std::atomic<bool> stop;
    std::atomic<bool> show_strip;
    int bpm;
    bool data_received;
    bool bpm_detection;
    int color_sequence_id;
    std::string data;
    std::thread* animating;
    UDP* udp_server;
    std::vector<Animation*> running_animations;
    int active_scene;
    float brightness;
    int led_count;
    int frequency;    
    FrequencyColors frequency_colors;
    std::mutex led_mutex;
};
