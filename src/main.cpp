#include <atomic>
#include <csignal>
#include <chrono>
#include <iostream>
#include <thread>

#include "Strip.hpp"
#include "util/database/InitializeDB.hpp"

namespace {
std::atomic<bool> g_should_exit{false};

void handle_signal(int) {
    g_should_exit.store(true);
}
}  // namespace

int main() {
    InitializeDB::create_database(true);

    Strip strip;

    std::signal(SIGINT, handle_signal);
    std::signal(SIGTERM, handle_signal);

    std::cout << "Art-Net input ready. Waiting for packets..." << std::endl;

    while (!g_should_exit.load()) {
        std::this_thread::sleep_for(std::chrono::milliseconds(200));
    }

    strip.stop.store(true);
    std::this_thread::sleep_for(std::chrono::milliseconds(200));

    return 0;
}
