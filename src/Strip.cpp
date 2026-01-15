#include "Strip.hpp"

#include "Animation.hpp"
#include "Color.hpp"
#include "ColorSequence.hpp"
#include "FrequencyColors.hpp"
#include "Scene.hpp"
#include "Section.hpp"
#include "util/configuration/AnimationData.hpp"
#include "util/database/AnimationDB.hpp"
#include "util/database/ColorDB.hpp"
#include "util/database/ColorSequenceDB.hpp"
#include "util/database/SceneAnimationDB.hpp"
#include "util/database/SceneDB.hpp"
#include "util/database/SectionDB.hpp"
#include "util/udp/ArtNetPacket.hpp"
#include "util/udp/UDP.hpp"
#include <algorithm>
#include <chrono>
#include <cmath>
#include <cstring>
#include <fstream>
#include <iostream>
#include <optional>
#include <sstream>
#include <thread>

// #include "animation/MonoColor.hpp"
// #include "animation/Shooter.hpp"
// #include "animation/Flow.hpp"
#include "animation/Strobe.hpp"
// #include "animation/Squeeze.hpp"

#define ANIMATION_STEPS 30
#define CONFIG_FILE "config.json"

using namespace std;

Strip::Strip() : artnet_animation(nullptr) {
  config = fetch_config();

  brightness = config.value("brightness", 1.0f);
  led_count = config.value("led_count", 60);
  frequency = config.value("frequency", 800000);
  bpm = config.value("bpm", 128);

  data_received.store(false);
  color_sequence_id = 0;
  pending_artnet_state.reset();
  last_artnet_state.reset();

  artnet_color_sequence = std::make_shared<ColorSequence>();
  artnet_color_sequence->id = -1;
  artnet_color_sequence->name = "ArtNet Runtime";
  artnet_color_sequence->description = "Runtime colors provided via Art-Net";
  artnet_color_sequence->selection = 0;
  artnet_color_sequence->color_amount = 0;

  stop.store(false);
  animating = nullptr;
  show_strip.store(false);

  led_string = {};
  initialize_artnet_settings();

  // Load sections
  auto section_data = SectionDB::fetch_sections();
  for (const auto &sec : section_data) {
    auto get_int = [&](const std::string &key) -> std::optional<int> {
      auto it = sec.find(key);
      if (it != sec.end()) {
        if (std::holds_alternative<int>(it->second)) {
          return std::get<int>(it->second);
        }
      }
      return std::nullopt;
    };

    auto get_str = [&](const std::string &key) -> std::optional<std::string> {
      auto it = sec.find(key);
      if (it != sec.end()) {
        if (std::holds_alternative<std::string>(it->second)) {
          return std::get<std::string>(it->second);
        }
      }
      return std::nullopt;
    };

    sections.push_back(Section(get_int("id"), get_str("name"),
                               get_int("start_led"), get_int("end_led")));
  }

  // Load color sequences
  auto sequence_data = ColorSequenceDB::fetch_color_sequences().value_or(
      std::vector<ColorSequenceDB>());
  for (const auto &seq : sequence_data) {
    color_sequences.push_back(ColorSequence(seq.id, seq.name, seq.description,
                                            seq.selection, seq.color_amount));
  }

  // Frequency Color Sequences (Scene ID -1 = workspace)
  frequency_colors = FrequencyColors(-1);

  // Load scenes
  auto scenes_data = SceneDB::fetch_scenes();
  for (const auto &sc : scenes_data) {
    scenes.push_back(Scene(std::make_optional(std::stoi(sc.at("id"))),
                           std::make_optional(sc.at("name")),
                           std::make_optional(sc.at("description"))));
  }

  active_scene = -1;
  udp_server = new UDP(artnet_settings.port);

  create_animations();
  init_strip();
  initialize_artnet_settings();

  if (ws2811_init(&led_string) != WS2811_SUCCESS) {
    std::cout << "ws2811_init failed!" << std::endl;
  } else {
    std::cout << "Strip initialized with " << led_count << " LEDs."
              << std::endl;
  }

  if (artnet_settings.debug) {
    std::cout << "Art-Net listening on port " << artnet_settings.port
              << ", universe " << artnet_settings.universe << ", start address "
              << artnet_settings.start_address << ", LED range ["
              << artnet_settings.strip_start_led << ", "
              << artnet_settings.strip_end_led << "]" << std::endl;
  }

  if (!animating) {
    animating = new std::thread(&Strip::animate, this,
                                [this]() { return stop.load(); });
  }
}

void Strip::update_config(const std::string &key, const nlohmann::json &value) {
  auto config = fetch_config();
  config[key] = value;
  std::ofstream file(CONFIG_FILE);
  file << config.dump(4);
}

void Strip::initialize_artnet_settings() {
  nlohmann::json artnet_cfg;
  if (config.count("artnet") != 0) {
    artnet_cfg = config["artnet"];
  } else {
    artnet_cfg = nlohmann::json::object();
  }

  artnet_settings.port = artnet_cfg.value("port", 6454);
  artnet_settings.universe =
      static_cast<uint16_t>(artnet_cfg.value("universe", 0));

  const uint16_t configured_start =
      static_cast<uint16_t>(std::max(1, artnet_cfg.value("start_address", 1)));
  artnet_settings.start_address = configured_start;

  const int max_led_index = std::max(0, led_count - 1);
  artnet_settings.strip_start_led =
      std::clamp(artnet_cfg.value("strip_start_led", 0), 0, max_led_index);
  artnet_settings.strip_end_led =
      std::clamp(artnet_cfg.value("strip_end_led", max_led_index),
                 artnet_settings.strip_start_led, max_led_index);
  artnet_settings.debug = artnet_cfg.value("debug", true);
}

void Strip::init_strip() {
  config = fetch_config();

  ws2811_channel_t channels[2]{};

  channels[0].gpionum = static_cast<int>(config["pin"]);
  channels[0].invert = static_cast<int>(config["led_invert"]);
  channels[0].count = static_cast<int>(config["led_count"]);
  channels[0].brightness = 255;
  channels[0].strip_type = WS2811_STRIP_GRB;

  led_string.freq = static_cast<int>(config["frequency"]);
  led_string.dmanum = static_cast<int>(config["dma"]);
  led_string.channel[0] = channels[0];
  led_string.channel[1] = channels[1];

  for (auto &anim : running_animations) {
    anim->strip = this;
  }
}

nlohmann::json Strip::fetch_config() {
  std::ifstream file(CONFIG_FILE);
  nlohmann::json config;
  file >> config;
  return config;
}

void Strip::restart_strip() {
  stop.store(true);
  std::this_thread::sleep_for(
      std::chrono::milliseconds(static_cast<int>(sleep_time() * 2100)));

  init_strip();
  initialize_artnet_settings();
  if (ws2811_init(&led_string) != WS2811_SUCCESS) {
    std::cout << "ws2811_init failed!" << std::endl;
  }
  stop.store(false);
  animating =
      new std::thread(&Strip::animate, this, [this]() { return stop.load(); });
}

void Strip::set_pixel_color(int pixel, int red, int green, int blue) {
  const double scale = (double)brightness / 100.0;
  auto scale_component = [scale](int value) -> int {
    return std::clamp(static_cast<int>(std::round(value * scale)), 0, 255);
  };

  const int scaled_red = scale_component(red);
  const int scaled_green = scale_component(green);
  const int scaled_blue = scale_component(blue);

  if (pixel < 0 || pixel >= led_count)
    return;
  if (!led_string.channel[0].leds)
    return;

  int packed_color = (scaled_red << 16) | (scaled_green << 8) | scaled_blue;

  std::lock_guard<std::mutex> lock(led_mutex);
  led_string.channel[0].leds[pixel] = packed_color;
}

void Strip::create_animations() {
  std::cout << "create_animations() called!" << std::endl;
  std::cout << "ANIMATION_DATA size = " << get_animations().size() << std::endl;

  for (auto &animation_dat : get_animations()) {
    std::cout << "Checking animation id = " << animation_dat.id << std::endl;

    auto anim = AnimationDB::fetch_animation(animation_dat.id);
    if (anim.has_value()) {
      std::cout << "Animation with ID " << animation_dat.id
                << " already exists in database." << std::endl;
      continue;
    }

    bool success =
        Database::push_to_db("INSERT INTO animations (id, name, description) "
                             "VALUES(:id, :name, :description)",
                             {{"id", animation_dat.id},
                              {"name", animation_dat.name},
                              {"description", animation_dat.description}});

    if (!success) {
      std::cout << "Failed to insert animation with ID: " << animation_dat.id
                << std::endl;
    } else {
      std::cout << "Inserted animation with ID: " << animation_dat.id
                << std::endl;
    }
  }
}

bool Strip::update_animation(int id, int section_id, const std::string &name,
                             const std::string &description, int variation,
                             int direction, int offset) {
  for (auto &animation : running_animations) {
    if (animation->id == id && animation->section_id == section_id) {
      animation->name = name;
      animation->description = description;
      animation->variation = variation;
      animation->direction = direction;
      animation->offset = offset;

      return animation->sync_changes_to_db(false);
    }
  }
  return false; // Animation not found
}

bool Strip::set_brightness(int brightness, bool persist) {
  if (brightness < 0) {
    return false;
  }
  if (brightness > 255) {
    brightness = 255;
  }

  this->brightness = std::clamp(brightness, 0, 100);

  if (persist) {
    // HELL NAH
    // update_config("brightness", this->brightness);
  } else {
    // TODO: no-risk config
    // config["brightness"] = this->brightness;
  }
  return true;
}

bool Strip::set_led_count(int led_count) {
  if (led_count < 0)
    return false;
  this->led_count = led_count;
  update_config("led_count", led_count);
  initialize_artnet_settings();
  restart_strip();
  return true;
}

bool Strip::set_bpm(int bpm, bool persist) {
  if (bpm < 1)
    return false;
  this->bpm = bpm;
  if (persist) {
    update_config("bpm", bpm);
  } else {
    config["bpm"] = bpm;
  }
  return true;
}

// Sections
bool Strip::add_section(const string &name, int start_led, int end_led) {
  // if (SectionDB::fetch_section(name).id != -1) return false;  // What is
  // this? :3

  Section section(std::nullopt, name, start_led, end_led);
  if (!section.sync_changes_to_db(true))
    return false;

  sections.push_back(section);
  return true;
}

bool Strip::remove_section(int id) {
  // Check if Section is currently used in animations
  for (auto &animation : running_animations) {
    if (animation->section_id == id) {
      return false; // Section is in use, cannot remove
    }
  }

  return SectionDB::remove_section(id);
}

bool Strip::update_section(int id, const string &name, int start_led,
                           int end_led) {
  for (auto &section : sections) {
    if (section.id == id) {
      section.name = name;
      section.start_led = start_led;
      section.end_led = end_led;
      return section.sync_changes_to_db(false);
    }
  }
  return false;
}

// bool Strip::update_section(int id, int start_led, int end_led) {
//     for (auto& section : sections) {
//         if (section.id == id) {
//             section.start_led = start_led;
//             section.end_led = end_led;
//             return section.sync_changes_to_db(false);
//         }
//     }
//     return false;
// }

// Color Sequence
bool Strip::add_color_sequence(const std::string &name,
                               const std::string &description, int selection,
                               int color_amount) {
  // if (ColorSequenceDB::fetch_color_sequence(name).id != -1) return false;

  ColorSequence color_sequence(std::nullopt, name, description, selection,
                               color_amount);
  if (!color_sequence.sync_changes_to_db(true))
    return false;

  color_sequences.push_back(color_sequence);
  return true;
}

bool Strip::remove_color_sequence(int id) {
  auto it = remove_if(color_sequences.begin(), color_sequences.end(),
                      [id](const ColorSequence &color_sequence) {
                        return color_sequence.id == id;
                      });

  if (it != color_sequences.end()) {
    color_sequences.erase(it, color_sequences.end());
    ColorSequenceDB::remove_color_sequence(id);
    return true;
  }

  return false;
}

bool Strip::update_color_sequence(int id, const string &name,
                                  const string &description, int selection,
                                  int color_amount) {
  for (auto &color_sequence : color_sequences) {
    if (color_sequence.id == id) {
      color_sequence.name = name;
      color_sequence.description = description;
      color_sequence.selection = selection;
      color_sequence.color_amount = color_amount;
      return color_sequence.sync_changes_to_db(false);
    }
  }
  return false;
}

// Colors
bool Strip::add_color(int color_sequence_id, int red, int green, int blue) {
  for (auto &color_sequence : color_sequences) {
    if (color_sequence.id == color_sequence_id) {
      return color_sequence.add_color(
          Color(std::nullopt, color_sequence_id, -1, red, green, blue));
    }
  }
  return false;
}

bool Strip::remove_color(int id) {
  Color color(id);
  if (!color.sync_changes_to_db(false))
    return false;

  // Also remove from color_sequence cache
  for (auto &color_sequence : color_sequences) {
    if (color_sequence.id == color.color_sequence_id) {
      color_sequence.remove_color(id);

      for (auto &animation : running_animations) {
        if (animation->color_sequence->id == color_sequence.id) {
          animation->color_sequence =
              std::make_shared<ColorSequence>(color_sequence);
        }
      }
    }
  }
  return true;
}

bool Strip::update_color(int id, int color_sequence_id, int position, int red,
                         int green, int blue) {
  Color color(id, color_sequence_id, position, red, green, blue);
  if (!color.sync_changes_to_db(false))
    return false;

  for (auto &color_sequence : color_sequences) {
    if (color_sequence.id == color_sequence_id) {
      color_sequence.update_colors();
      return true;
    }
  }
  return false;
}

bool Strip::update_frequency_color_sequences(int scene_id,
                                             int color_sequence_id_1,
                                             int color_sequence_id_2,
                                             int color_sequence_id_3) {
  frequency_colors.color_sequence_id_1 = color_sequence_id_1;
  frequency_colors.color_sequence_id_2 = color_sequence_id_2;
  frequency_colors.color_sequence_id_3 = color_sequence_id_3;

  return frequency_colors.sync_changes_to_db(false);
}

float Strip::sleep_time() const { return 60.0f / static_cast<float>(bpm); }

void Strip::color_wipe(int color) {
  for (int i = 0; i < led_count; ++i) {
    this->set_pixel_color(i, color, color, color);
  }
  ws2811_render(&led_string);
}

void Strip::color_wipe(Color color) {
  for (int i = 0; i < led_count; ++i) {
    this->set_pixel_color(i, color.red, color.green, color.blue);
  }
  ws2811_render(&led_string);
}

void Strip::add_animation(Animation *animation, Section section,
                          ColorSequence color_sequence) {
  animation->bpm = bpm;
  animation->section_id = section.id;
  animation->start_led = section.start_led;
  animation->end_led = section.end_led;

  animation->color_sequence = std::make_shared<ColorSequence>(color_sequence);
  animation->strip = this;
  animation->brightness = brightness;

  running_animations.push_back(animation);
}

void Strip::set_data(const std::vector<char> &new_data) {
  const auto parsed = parse_artnet_dmx(new_data);
  if (!parsed.has_value()) {
    return;
  }

  const auto &frame = parsed->frame;
  if (frame.universe != artnet_settings.universe) {
    if (artnet_settings.debug) {
      std::cout << "[ArtNet] Ignored packet for universe " << frame.universe
                << std::endl;
    }
    return;
  }

  if (frame.data.size() < artnet_required_channels()) {
    if (artnet_settings.debug) {
      std::cout << "[ArtNet] Frame length " << frame.data.size()
                << " shorter than required " << artnet_required_channels()
                << std::endl;
    }
    return;
  }

  const std::size_t offset =
      static_cast<std::size_t>(artnet_settings.start_address - 1);

  ArtNetState state{};
  state.sequence = frame.sequence;
  state.alpha = frame.data[offset];
  state.red = frame.data[offset + 1];
  state.green = frame.data[offset + 2];
  state.blue = frame.data[offset + 3];
  state.bpm = frame.data[offset + 4];
  state.animation = frame.data[offset + 5];

  {
    std::lock_guard<std::mutex> lock(artnet_mutex);
    pending_artnet_state = state;
  }
  data_received.store(true);

  if (artnet_settings.debug) {
    std::cout << "[ArtNet] " << parsed->debug_message
              << " | alpha=" << static_cast<int>(state.alpha)
              << " r=" << static_cast<int>(state.red)
              << " g=" << static_cast<int>(state.green)
              << " b=" << static_cast<int>(state.blue)
              << " bpm=" << static_cast<int>(state.bpm)
              << " anim=" << static_cast<int>(state.animation) << std::endl;
  }
}

void Strip::show_strip_handler(std::function<bool()> stop) {
  while (!stop()) {
    if (show_strip.exchange(false)) {
      if (!led_string.channel[0].leds) {
        continue;
      }
      std::lock_guard<std::mutex> lock(led_mutex); // protect rendering
      int status = ws2811_render(&led_string);
      if (status != WS2811_SUCCESS) {
        std::cout << "Render failed: "
                  << ws2811_get_return_t_str((ws2811_return_t)status)
                  << std::endl;
      }
    }
    std::this_thread::sleep_for(
        std::chrono::milliseconds(30)); // avoid busy loop
  }
}

void Strip::animate(function<bool()> stop) {
  std::thread(&Strip::show_strip_handler, this, stop).detach();

  const auto receiver = [this](const std::vector<char> &data) {
    this->set_data(data);
  };

  std::thread udp_thread(
      [this, &stop, receiver]() { udp_server->receive(stop, receiver); });
  udp_thread.detach();

  auto loop_start = chrono::steady_clock::now();
  int step = 0;
  int beat = 0;

  while (!stop()) {
    if (data_received.exchange(false)) {
      std::optional<ArtNetState> state_copy;
      {
        std::lock_guard<std::mutex> lock(artnet_mutex);
        state_copy = pending_artnet_state;
      }
      if (state_copy.has_value()) {
        apply_artnet_state(state_copy.value());
      }
    }

    for (auto *animation : running_animations) {
      animation->bpm = bpm;
      animation->brightness = brightness;
      animation->animate(beat + animation->offset, step);
    }

    const auto elapsed =
        chrono::duration<double>(chrono::steady_clock::now() - loop_start)
            .count();
    const double target_interval =
        running_animations.empty()
            ? 0.05
            : std::max(0.0, static_cast<double>(sleep_time()) /
                                static_cast<double>(ANIMATION_STEPS));
    const double sleep_time_adjusted = target_interval - elapsed;

    if (sleep_time_adjusted > 0.0) {
      this_thread::sleep_for(chrono::duration<double>(sleep_time_adjusted));
    }

    loop_start = chrono::steady_clock::now();

    if (!running_animations.empty()) {
      show_strip.store(true);
      step = (step + 1) % ANIMATION_STEPS;
      if (step == 0) {
        beat = (beat + 1) % 16;
      }
    } else {
      step = 0;
      beat = 0;
    }
  }

  clear_running_animations();
  apply_static_color(ArtNetState{0, 0, 0, 0, 0, 0, 0});
  show_strip.store(true);
}

void Strip::apply_artnet_state(const ArtNetState &state) {
  bool brightness_changed = false;

  const auto current_brightness_percent =
      static_cast<int>(std::round(brightness * 100.0f));
  const int target_brightness_percent = static_cast<int>(
      std::round(static_cast<float>(state.alpha) / 255.0f * 100.0f));
  if (target_brightness_percent != current_brightness_percent) {
    brightness_changed = true;
    set_brightness(target_brightness_percent, false);
  }

  if (state.bpm > 0) {
    const int mapped_bpm = std::clamp(
        static_cast<int>(std::round(40.0 + (state.bpm / 255.0f) * 200.0f)), 40,
        240);
    if (bpm != mapped_bpm) {
      set_bpm(mapped_bpm, false);
    }
  }

  if (state.animation == 0) {
    const bool color_changed = !last_artnet_state.has_value() ||
                               last_artnet_state->red != state.red ||
                               last_artnet_state->green != state.green ||
                               last_artnet_state->blue != state.blue ||
                               last_artnet_state->animation != state.animation;
    if (color_changed || brightness_changed || artnet_animation != nullptr) {
      clear_running_animations();
      apply_static_color(state);
    }
  } else {
    ensure_artnet_animation(state);
  }

  last_artnet_state = state;
}

void Strip::apply_static_color(const ArtNetState &state) {
  const auto [start_led, end_led] = artnet_led_range();
  for (int led = start_led; led <= end_led; ++led) {
    set_pixel_color(led, state.red, state.green, state.blue);
  }
  show_strip.store(true);
}

void Strip::ensure_artnet_animation(const ArtNetState &state) {
  const auto [start_led, end_led] = artnet_led_range();

  if (!artnet_animation) {
    auto *strobe = new Strobe();
    strobe->section_id = -1;
    strobe->start_led = start_led;
    strobe->end_led = end_led;
    strobe->variation = 0;
    strobe->direction = 0;
    strobe->offset = 0;
    strobe->strip = this;
    strobe->bpm = bpm;
    strobe->brightness = brightness;
    strobe->color_sequence = artnet_color_sequence;
    running_animations.push_back(strobe);
    artnet_animation = strobe;
  }

  auto *strobe = dynamic_cast<Strobe *>(artnet_animation);
  if (strobe) {
    const uint8_t index =
        static_cast<uint8_t>(state.animation > 0 ? state.animation - 1 : 0);
    strobe->variation = index % 3;
    strobe->direction = (index / 3) % 4;
    strobe->start_led = start_led;
    strobe->end_led = end_led;
    strobe->bpm = bpm;
    strobe->brightness = brightness;
    strobe->color_sequence = artnet_color_sequence;
  }

  Color runtime_color;
  runtime_color.id = -1;
  runtime_color.color_sequence_id = -1;
  runtime_color.position = 0;
  runtime_color.red = state.red;
  runtime_color.green = state.green;
  runtime_color.blue = state.blue;
  artnet_color_sequence->selection = 0;
  artnet_color_sequence->color_amount = 1;
  artnet_color_sequence->set_runtime_colors({runtime_color});

  show_strip.store(true);
}

void Strip::clear_running_animations() {
  if (!artnet_animation) {
    return;
  }

  running_animations.erase(std::remove(running_animations.begin(),
                                       running_animations.end(),
                                       artnet_animation),
                           running_animations.end());
  delete artnet_animation;
  artnet_animation = nullptr;
}

std::pair<int, int> Strip::artnet_led_range() const {
  if (artnet_settings.strip_start_led > artnet_settings.strip_end_led) {
    return {0, std::max(0, led_count - 1)};
  }
  return {artnet_settings.strip_start_led, artnet_settings.strip_end_led};
}

std::size_t Strip::artnet_required_channels() const {
  return static_cast<std::size_t>(artnet_settings.start_address - 1 + 6);
}

bool Strip::start_animate(int color_sequence_id,
                          std::optional<Animation *> animation, int section_id,
                          std::optional<int> animation_id) {
  auto section_data = SectionDB::fetch_section(section_id);

  // Check if section exists
  if (section_data.empty()) {
    return false; // Section not found
  }

  Section section(std::get<int>(section_data.at("id")),
                  std::get<std::string>(section_data.at("name")),
                  std::get<int>(section_data.at("start_led")),
                  std::get<int>(section_data.at("end_led")));

  stop_animate(section_id, true); // Stop current animation if there is one

  // Find out which color sequence is meant
  auto optional_color_data =
      ColorSequenceDB::fetch_color_sequence(color_sequence_id);
  if (!optional_color_data.has_value()) {
    return false;
  }

  auto color_data = optional_color_data.value();

  ColorSequence color_sequence(color_data.id, color_data.name,
                               color_data.description, color_data.selection,
                               color_data.color_amount);

  if (!animation.has_value()) {
    // Find out which animation is meant
    switch (animation_id.value_or(-1)) {
    // case 0:
    //     animation = new MonoColor(0, section.id);
    //     break;
    // case 1:
    //     animation = new Flow(1, section.id);
    //     break;
    // case 2:
    //     animation = new Shooter(2, section.id);
    //     break;
    case 3:
      animation = new Strobe(3, section_id);
      break;
      // case 4:
      //     animation = new Squeeze(4, section.id);
      break;
    default:
      return false; // Invalid animation ID
    }
  }

  add_animation(animation.value(), section, color_sequence);

  if (!animating) {
    animating =
        new std::thread(&Strip::animate, this, [&]() { return stop.load(); });
  }

  return true;
}

bool Strip::stop_animate(int section_id, bool start_new) {
  std::map<std::string, std::variant<std::string, int>> section_data =
      SectionDB::fetch_section(section_id);

  if (section_data.empty()) {
    return false; // Section not found
  }

  Section section(std::get<int>(section_data.at("id")),
                  std::get<std::string>(section_data.at("name")),
                  std::get<int>(section_data.at("start_led")),
                  std::get<int>(section_data.at("end_led")));

  // Find running animation and stop it
  for (auto &animation : running_animations) {
    if (animation->section_id == section.id) {
      running_animations.erase(remove(running_animations.begin(),
                                      running_animations.end(), animation),
                               running_animations.end());
    }
  }

  std::this_thread::sleep_for(
      std::chrono::milliseconds(static_cast<int>(sleep_time() * 1100)));

  if (!start_new) {
    color_wipe(Color(0, 0, 0)); // Turn part of strip off
  }

  return true;
}

bool Strip::add_scene(const string &name, const string &description) {
  Scene scene(std::nullopt, name, description);
  if (!scene.sync_changes_to_db(true))
    return false;
  scenes.push_back(scene);
  return true;
}

bool Strip::remove_scene(int scene_id) {
  auto it =
      remove_if(scenes.begin(), scenes.end(), [scene_id](const Scene &scene) {
        return scene.id == scene_id;
      });

  if (it != scenes.end()) {
    scenes.erase(it, scenes.end());
    SceneDB::remove_scene(scene_id);
    SceneAnimationDB::remove_scene_animations(scene_id);
    return true;
  }

  return false;
}

bool Strip::update_scene(int id, const string &name,
                         const string &description) {
  for (auto &scene : scenes) {
    if (scene.id == id) {
      scene.name = name;
      scene.description = description;
      return scene.sync_changes_to_db(false);
    }
  }
  return false;
}

bool Strip::save_scene(int scene_id) {
  for (auto &scene : scenes) {
    if (scene.id == scene_id) {
      std::vector<std::map<std::string, int>> animations_data_to_save;
      for (auto &animation : running_animations) {
        animations_data_to_save.push_back(
            {{"scene_id", scene.id},
             {"animation_id", animation->id},
             {"section_id", animation->section_id},
             {"color_sequence_id", animation->color_sequence->id}});
      }

      return scene.save(animations_data_to_save);
    }
  }
  return false;
}

bool Strip::load_scene(int scene_id) {
  for (auto &scene : scenes) {
    if (scene.id == scene_id) {
      auto animations_data_to_run = scene.load(); // Load scene into workspace
      running_animations.clear();                 // Stop all running animations

      if (!animations_data_to_run.has_value()) {
        return false; // No animations found for this scene
      }

      if (!animations_data_to_run.value().empty()) {
        for (const auto &animation_data : animations_data_to_run.value()) {
          start_animate(animation_data.at("color_sequence_id"), std::nullopt,
                        animation_data.at("section_id"), std::nullopt);
        }
      }

      active_scene = scene_id;
      return true;
    }
  }
  return false;
}

nlohmann::json Strip::get_frequency_color_sequences() const {
  return {{"color_sequence_id_1", frequency_colors.color_sequence_id_1},
          {"color_sequence_id_2", frequency_colors.color_sequence_id_2},
          {"color_sequence_id_3", frequency_colors.color_sequence_id_3}};
}
