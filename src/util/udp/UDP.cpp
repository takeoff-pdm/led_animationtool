#include "UDP.hpp"
#include <iostream>
#include <cstring>
#include <netinet/in.h>
#include <unistd.h>
#include <vector>

// Constructor to initialize UDP socket and bind it to the specified port
UDP::UDP(int port) : port(port), running(false) {
    sock = socket(AF_INET, SOCK_DGRAM, 0);
    if (sock < 0) {
        std::cerr << "Error opening socket" << std::endl;
        exit(1);
    }

    struct sockaddr_in server_addr;
    memset(&server_addr, 0, sizeof(server_addr));

    server_addr.sin_family = AF_INET;
    server_addr.sin_addr.s_addr = INADDR_ANY;
    server_addr.sin_port = htons(port);

    if (bind(sock, (struct sockaddr*)&server_addr, sizeof(server_addr)) < 0) {
        std::cerr << "Error binding socket to port" << std::endl;
        exit(1);
    }
}

// Destructor to close the socket
UDP::~UDP() {
    close();
}

// Method to receive UDP data in a separate thread
void UDP::receive(const std::function<bool()>& stop, const std::function<void(const std::vector<char>&)>& set_data) {
    running = true;

    while (!stop()) {  // Call stop as a function (stop() is a std::function<bool()>)
        std::vector<char> buffer(512);

        ssize_t received = recvfrom(sock, buffer.data(), buffer.size(), 0, nullptr, nullptr);
        if (received > 0) {
            buffer.resize(received);  // Adjust the buffer size to the actual data received
            set_data(buffer);
        }
    }
}

// Method to close the UDP socket
void UDP::close() {
    if (running) {
        running = false;
        if (receiver_thread.joinable()) {
            receiver_thread.join();
        }
    }
    ::close(sock);
}
