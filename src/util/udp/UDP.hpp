#pragma once

#include <string>
#include <functional>
#include <thread>
#include <atomic>

class UDP {
public:
    UDP(int port);
    ~UDP();

    void receive(const std::function<bool()>& stop, const std::function<void(const std::vector<char>&)>& set_data);
    void close();

private:
    int sock;
    int port;
    std::thread receiver_thread;
    std::atomic<bool> running;
};
