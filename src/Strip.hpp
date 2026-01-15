#include <vector>
#include <string>
#include <functional>
#include <thread>
#include <atomic>
#include <cstdint>
#include <optional>
#include <memory>
#include <utility>
#include <mutex>
#include <nlohmann/json.hpp>
#if __has_include(<ws2811.h>)
#include <ws2811.h>
#elif __has_include("rpi_ws281x/ws2811.h")
#include "rpi_ws281x/ws2811.h"
#else
#error "ws2811.h header not found. Ensure rpi_ws281x is available."
#endif
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
    bool set_brightness(int brightness, bool persist = true);
    bool set_led_count(int led_count);
    bool set_bpm(int bpm, bool persist = true);
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
    std::atomic<bool> data_received;
    int color_sequence_id;
    std::thread* animating;
    UDP* udp_server;
    std::vector<Animation*> running_animations;
    int active_scene;
    float brightness;
    int led_count;
    int frequency;    
    FrequencyColors frequency_colors;
    std::mutex led_mutex;

private:
    struct ArtNetSettings {
        int port;
        uint16_t universe;
        uint16_t start_address;
        int strip_start_led;
        int strip_end_led;
        bool debug;
    };

    struct ArtNetState {
        uint8_t alpha;
        uint8_t red;
        uint8_t green;
        uint8_t blue;
        uint8_t bpm;
        uint8_t animation;
        uint8_t sequence;
    };

    void apply_artnet_state(const ArtNetState& state);
    void apply_static_color(const ArtNetState& state);
    void ensure_artnet_animation(const ArtNetState& state);
    void clear_running_animations();
    std::pair<int, int> artnet_led_range() const;
    std::size_t artnet_required_channels() const;
    void initialize_artnet_settings();

    ArtNetSettings artnet_settings;
    std::optional<ArtNetState> pending_artnet_state;
    std::optional<ArtNetState> last_artnet_state;
    std::shared_ptr<ColorSequence> artnet_color_sequence;
    Animation* artnet_animation;
    std::mutex artnet_mutex;
};
