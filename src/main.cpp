#include <boost/beast/core.hpp>
#include <boost/beast/http.hpp>
#include <boost/asio/ip/tcp.hpp>
#include <boost/asio/strand.hpp>
#include <boost/config.hpp>
#include <nlohmann/json.hpp>
#include <iostream>
#include <memory>
#include <string>
#include <thread>
#include <unordered_map>
#include <mutex>

#include "Strip.hpp"
#include "util/database/Database.hpp"
#include "util/database/InitializeDB.hpp"
#include "util/database/SectionDB.hpp"
#include "util/database/ColorDB.hpp"
#include "util/database/ColorSequenceDB.hpp"
#include "util/database/AnimationDB.hpp"
#include "util/database/SceneDB.hpp"
#include "util/database/SectionAnimationDB.hpp"

namespace beast = boost::beast;
namespace http  = beast::http;
namespace net   = boost::asio;
using tcp       = net::ip::tcp;
using json      = nlohmann::json;

Strip strip = Strip(); // Global application state

//------------------------------------------------------------------------------
// Report a failure
//------------------------------------------------------------------------------

void fail(beast::error_code ec, char const* what) {
    std::cerr << what << ": " << ec.message() << std::endl;
}

template <class Response>
void add_cors_headers(Response& res) {
    res.set(beast::http::field::access_control_allow_origin, "http://localhost:3000");
    res.set(beast::http::field::access_control_allow_credentials, "true");
    res.set(http::field::access_control_allow_headers, "Content-Type");
    res.set(beast::http::field::access_control_allow_methods, "GET, POST, OPTIONS");
}

//------------------------------------------------------------------------------
// Handles an HTTP request and produces a response
//------------------------------------------------------------------------------

template<class Body, class Allocator>
http::response<http::string_body> handle_req(http::request<Body, http::basic_fields<Allocator>>&& req) {
    http::response<http::string_body> res{http::status::ok, req.version()};
    res.set(http::field::server, "Beast");
    res.set(http::field::content_type, "application/json");
    res.keep_alive(req.keep_alive());

    try {
        if (req.method() == http::verb::options) {
            res.result(http::status::ok);
            res.body() = "";
            add_cors_headers(res);
            res.prepare_payload();
            return res;
        }

        const std::string target = std::string(req.target());

        // Print for debugging
        std::cout << "[HTTP] Request: " << target << "\n";

        if (target == "/api/get/sections") {
            std::vector<std::map<std::string, std::variant<std::string, int>>> sections_data = SectionDB::fetch_sections(-1);

            json sections = json::array();
            for (const auto& section_data : sections_data) {
                json section = {
                    {"id", std::get<int>(section_data.at("id"))},
                    {"name", std::get<std::string>(section_data.at("name"))},
                    {"start_led", std::get<int>(section_data.at("start_led"))},
                    {"end_led", std::get<int>(section_data.at("end_led"))}
                };
                sections.push_back(section);
            }

            res.body() = json({{"sections", sections}}).dump();
        }
        else if (target == "/api/get/settings") {
            json config = strip.fetch_config();
            config["brightness"] = config["brightness"].get<float>() * 100;
            res.body() = config.dump();
        }
        else if (target.find("/api/update/brightness") != std::string::npos ) { // && req.method() == http::verb::post
            auto body = json::parse(req.body());
            bool success = strip.set_brightness(body["value"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/get/section") { //  && req.method() == http::verb::get
            json body = json::parse(req.body());
            std::map<std::string, std::variant<std::string, int>> section_data = SectionDB::fetch_section(body["id"], -1);
            json section = {
                {"id", std::get<int>(section_data["id"])}, 
                {"name", std::get<std::string>(section_data["name"])}, 
                {"start_led", std::get<int>(section_data["start_led"])}, 
                {"end_led", std::get<int>(section_data["end_led"])}
            };

            res.body() = json({{"section", section}}).dump();
        }
        else if (target == "/api/add/section" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.add_section(body["name"], body["start_led"], body["end_led"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/remove/section" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.remove_section(body["id"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/update/section" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.update_section(body["id"], body["name"], body["start_led"], body["end_led"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/running_animation" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            
            for (auto& animation : strip.running_animations) {
                if (animation->section_id == body["id"]) {
                    res.body() = json({{"animation_id", animation->id}, 
                                      {"color_sequence_id", animation->color_sequence->id}}).dump();
                    break;
                }
            }

            res.body() = json({{"animation_id", false}, {"color_sequence_id", false}}).dump();
        }
        else if (target == "/api/get/color_sequences") { //  && req.method() == http::verb::get
            std::optional<std::vector<ColorSequenceDB>> color_sequences_data = ColorSequenceDB::fetch_color_sequences(-1);

            // if (!color_sequences_data.has_value()) {
            //     res.result(http::status::internal_server_error);
            //     res.body() = json({{"error", "Failed to fetch color sequences"}}).dump();
            //     res.prepare_payload();
            //     return res;
            // }
            
            json color_sequences = json::array();
            if (color_sequences_data.has_value()) {
                for (const auto& color_sequence : color_sequences_data.value()) {
                    json cs = {
                        {"id", color_sequence.id},
                        {"name", color_sequence.name},
                        {"description", color_sequence.description},
                        {"selection", color_sequence.selection},
                        {"color_amount", color_sequence.color_amount}
                    };
                    color_sequences.push_back(cs);
                }
            }

            res.body() = json({{"color_sequences", color_sequences}}).dump();
        }
        else if (target == "/api/get/color_sequence") { //  && req.method() == http::verb::get
            json body = json::parse(req.body());
            std::optional<ColorSequenceDB> color_sequence_data = ColorSequenceDB::fetch_color_sequence(body["id"], -1);

            if (!color_sequence_data.has_value()) {
                res.result(http::status::internal_server_error);
                res.body() = json({{"error", "Failed to fetch color sequence"}}).dump();
                res.prepare_payload();
                return res;
            }

            json color_sequence = {
                {"id", color_sequence_data.value().id},
                {"name", color_sequence_data.value().name},
                {"description", color_sequence_data.value().description},
                {"selection", color_sequence_data.value().selection},
                {"color_amount", color_sequence_data.value().color_amount}
            };

            res.body() = json({{"color_sequence", color_sequence}}).dump();
        }
        else if (target == "/api/add/color_sequence" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.add_color_sequence(body["name"], body["description"], body["selection"], body["color_amount"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/remove/color_sequence" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.remove_color_sequence(body["id"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/update/color_sequence") { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.update_color_sequence(
                body["id"],
                body["name"],
                body["description"],
                body["selection"],
                std::stoi(body["color_amount"].get<std::string>())
            );
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/get/colors") { // && req.method() == http::verb::get
            std::vector<ColorDB> colors_data = ColorDB::fetch_colors(-1);
            json colors = json::array();
            for (const auto& color : colors_data) {
                json cs = {
                    {"id", color.id},
                    {"color_sequence_id", color.color_sequence_id},
                    {"position", color.position},
                    {"red", color.red},
                    {"green", color.green},
                    {"blue", color.blue}
                };
                colors.push_back(cs);
            }

            res.body() = json({{"colors", colors}}).dump();
        }
        else if (target == "/api/get/colors_from_sequence" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            std::vector<ColorDB> colors = ColorDB::fetch_colors_from_sequence(body["id"], -1);

            json color_sequence = json::array();
            for (const auto& color : colors) {
                json cs = {
                    {"id", color.id},
                    {"color_sequence_id", color.color_sequence_id},
                    {"position", color.position},
                    {"red", color.red},
                    {"green", color.green},
                    {"blue", color.blue}
                };
                color_sequence.push_back(cs);
            }

            res.body() = json({{"colors", color_sequence}}).dump();
        }
        else if (target == "/api/get/color" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            ColorDB color_data = ColorDB::fetch_color(body["id"], -1);

            json color = {
                {"id", color_data.id},
                {"color_sequence_id", color_data.color_sequence_id},
                {"position", color_data.position},
                {"red", color_data.red},
                {"green", color_data.green},
                {"blue", color_data.blue}
            };

            res.body() = json({{"color", color}}).dump();
        }
        else if (target == "/api/add/color" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.add_color(body["color_sequence_id"], body["red"], body["green"], body["blue"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/remove/color" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.remove_color(body["id"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/update/color" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.update_color(body["id"], body["color_sequence_id"], 
                                              body["position"], body["red"], body["green"], body["blue"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/get/animations") { // && req.method() == http::verb::get
            // Fetch all animations from the database
            std::optional<std::vector<AnimationDB>> animations_data = AnimationDB::fetch_animations();
            if (!animations_data.has_value()) {
                res.result(http::status::internal_server_error);
                res.body() = json({{"error", "Failed to fetch animations"}}).dump();
                res.prepare_payload();
                return res;
            }

            json animations = json::array();
            for (const auto& animation : animations_data.value()) {
                json anim = {
                    {"id", animation.id},
                    {"name", animation.name},
                    {"description", animation.description}
                };
                animations.push_back(anim);
            }
            res.body() = json({{"animations", animations}}).dump();
        }
        else if (target == "/api/get/animation" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            std::optional<AnimationDB> animation_data = AnimationDB::fetch_animation(body["id"]);
            
            if (!animation_data.has_value()) {
                res.result(http::status::internal_server_error);
                res.body() = json({{"error", "Failed to fetch animation"}}).dump();
                res.prepare_payload();
                return res;
            }

            json animation = {
                {"id", animation_data.value().id},
                {"name", animation_data.value().name},
                {"description", animation_data.value().description}
            };

            res.body() = json({{"animation", animation}}).dump();
        }
        else if (target == "/api/get/section_animations" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            std::vector<std::map<std::string, int>> section_animations = SectionAnimationDB::fetch_section_animations(body["id"], -1);
            json animations = json::array();
            for (const auto& section_animation : section_animations) {
                json anim = {
                    {"section_id", section_animation.at("section_id")},
                    {"animation_id", section_animation.at("animation_id")},
                    {"variation", section_animation.at("variation")},
                    {"direction", section_animation.at("direction")},
                    {"offset", section_animation.at("offset")}
                };
                animations.push_back(anim);
            }

            res.body() = json({{"animations", animations}}).dump();
        }
        else if (target == "/api/get/section_animation" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            std::map<std::string, int> section_animation = SectionAnimationDB::fetch_section_animation(body["section_id"], body["animation_id"], -1);
            json animation = {
                {"section_id", section_animation["section_id"]},
                {"animation_id", section_animation["animation_id"]},
                {"variation", section_animation["variation"]},
                {"direction", section_animation["direction"]},
                {"offset", section_animation["offset"]}
            };

            res.body() = json({{"animation", animation}}).dump();
        }
        else if (target == "/api/update/animation" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.update_animation(body["id"], body["section_id"], body["name"], body["description"],
                                                  body["variation"], body["direction"], body["offset"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/start/animate" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.start_animate(
                body["color_sequence_id"],
                std::nullopt,
                body["section_id"],
                body["animation_id"]
            );
            
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/stop/animate" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.stop_animate(body["id"], false);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/get/scenes") { //  && req.method() == http::verb::get
            std::vector<std::map<std::string, std::string>> scenes_data = SceneDB::fetch_scenes();
            json scenes = json::array();
            for (const auto& scene_data : scenes_data) {
                json scene = {
                    {"id", scene_data.at("id")},
                    {"name", scene_data.at("name")},
                    {"description", scene_data.at("description")}
                };
                scenes.push_back(scene);
            }

            res.body() = json({{"scenes", scenes}}).dump();
        }
        else if (target == "/api/get/scene" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            std::map<std::string, std::string> scene_data = SceneDB::fetch_scene(body["id"]);
            json scene = {
                {"id", scene_data["id"]},
                {"name", scene_data["name"]},
                {"description", scene_data["description"]}
            };

            res.body() = json({{"scene", scene}}).dump();
        }
        else if (target == "/api/get/active_scene") { //  && req.method() == http::verb::get
            res.body() = json({{"id", strip.active_scene}}).dump();
        }
        else if (target == "/api/add/scene" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.add_scene(body["name"], body["description"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/remove/scene" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.remove_scene(body["id"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/update/scene" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.update_scene(body["id"], body["name"], body["description"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/load/scene" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.load_scene(body["id"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/save/scene" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.save_scene(body["id"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/get/frequency-color-sequences") { //  && req.method() == http::verb::get
            json color_sequences = strip.get_frequency_color_sequences();

            // if (color_sequences.empty()) {
            //     res.result(http::status::internal_server_error);
            //     res.body() = json({{"error", "Failed to fetch frequency color sequences"}}).dump();
            //     res.prepare_payload();
            //     return res;
            // }

            res.body() = json({{"color_sequences", color_sequences}}).dump();
        } else if (target == "/api/update/frequency-color-sequences") { //  && req.method() == http::verb::get
            json body = json::parse(req.body());
            bool success = strip.update_frequency_color_sequences(-1, body["color_sequence_id_1"], 
                                                                  body["color_sequence_id_2"], 
                                                                  body["color_sequence_id_3"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/update/led-count" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.set_led_count(body["value"]);
            res.body() = json({{"success", success}}).dump();
        }
        else if (target == "/api/update/bpm" ) { // && req.method() == http::verb::post
            json body = json::parse(req.body());
            bool success = strip.set_bpm(body["value"]);
            res.body() = json({{"success", success}}).dump();
        }
        else {
            res.result(http::status::not_found);
            res.body() = json({{"error", "Not found"}}).dump();
        }

    } catch (const std::exception& e) {
        res.result(http::status::internal_server_error);
        res.body() = json({{"error", e.what()}}).dump();
    }

    // Print for debugging
    std::cout << "[HTTP] Response: " << res.body() << "\n";

    res.prepare_payload();
    add_cors_headers(res);
    return res;
}

//------------------------------------------------------------------------------
// Session: per-connection state
//------------------------------------------------------------------------------

class session : public std::enable_shared_from_this<session> {
    beast::tcp_stream stream_;
    beast::flat_buffer buffer_;
    http::request<http::string_body> req_;
    std::shared_ptr<std::string const> doc_root_;
public:
    session(tcp::socket&& socket, std::shared_ptr<std::string const> const& doc_root)
        : stream_(std::move(socket))
        , doc_root_(doc_root) {}

    void run() {
        net::dispatch(stream_.get_executor(),
            beast::bind_front_handler(&session::do_read, shared_from_this()));
    }

private:
    void do_read() {
        req_ = {};
        stream_.expires_after(std::chrono::seconds(30));
        http::async_read(stream_, buffer_, req_,
            beast::bind_front_handler(&session::on_read, shared_from_this()));
    }

    void on_read(beast::error_code ec, std::size_t bytes_transferred) {
        boost::ignore_unused(bytes_transferred);
        if(ec == http::error::end_of_stream) {
            do_close();
            return;
        }
        if(ec) {
            fail(ec, "read");
            return;
        }
        auto res = handle_req(std::move(req_));
        send_response(std::move(res));
    }

    void send_response(http::response<http::string_body>&& msg) {
        bool keep_alive = msg.keep_alive();
        auto sp = std::make_shared<http::response<http::string_body>>(std::move(msg));
        http::async_write(stream_, *sp,
            beast::bind_front_handler(&session::on_write, shared_from_this(), keep_alive, sp));
    }

    void on_write(bool keep_alive, std::shared_ptr<http::response<http::string_body>> sp,
                  beast::error_code ec, std::size_t bytes_transferred) {
        boost::ignore_unused(bytes_transferred);
        if(ec) {
            fail(ec, "write");
            return;
        }
        if(!keep_alive) {
            do_close();
            return;
        }
        do_read();
    }

    void do_close() {
        beast::error_code ec;
        stream_.socket().shutdown(tcp::socket::shutdown_send, ec);
    }
};

//------------------------------------------------------------------------------
// Listener: accepts incoming connections
//------------------------------------------------------------------------------

class listener : public std::enable_shared_from_this<listener> {
    net::io_context& ioc_;
    tcp::acceptor acceptor_;
    std::shared_ptr<std::string const> doc_root_;
public:
    listener(net::io_context& ioc, tcp::endpoint endpoint, std::shared_ptr<std::string const> const& doc_root)
        : ioc_(ioc)
        , acceptor_(net::make_strand(ioc))
        , doc_root_(doc_root)
    {
        beast::error_code ec;
        acceptor_.open(endpoint.protocol(), ec);
        acceptor_.set_option(net::socket_base::reuse_address(true), ec);
        acceptor_.bind(endpoint, ec);
        acceptor_.listen(net::socket_base::max_listen_connections, ec);
    }

    void run() {
        do_accept();
    }

private:
    void do_accept() {
        acceptor_.async_accept(
            net::make_strand(ioc_),
            beast::bind_front_handler(&listener::on_accept, shared_from_this()));
    }

    void on_accept(beast::error_code ec, tcp::socket socket) {
        if(!ec) {
            std::make_shared<session>(std::move(socket), doc_root_)->run();
        }
        do_accept();
    }
};

//------------------------------------------------------------------------------
// Main: set up server and run
//------------------------------------------------------------------------------

int main() {
    InitializeDB::create_database(true);

    try {
        auto const address = net::ip::make_address("0.0.0.0");
        auto const port    = static_cast<unsigned short>(8000);
        auto const doc_root = std::make_shared<std::string>("/var/www");

        net::io_context ioc{1};
        std::make_shared<listener>(ioc, tcp::endpoint{address,port}, doc_root)->run();
        ioc.run();
    }
    catch(std::exception const& e) {
        std::cerr << "Fatal: " << e.what() << std::endl;
    }
    return 0;
}
