#pragma once

#include <string>
#include <queue>
#include <thread>
#include <atomic>
#include <condition_variable>
#include <sqlite3.h>
#include <unordered_map>
#include <variant>

class Database {
public:
    Database(bool manual = false);
    ~Database();

    // Database operation functions
    static bool push_to_db(const std::string& sql_command, const std::unordered_map<std::string, std::variant<int, std::string>>& sql_data);
    static std::vector<std::string> fetchone_from_db(const std::string& sql_command, const std::unordered_map<std::string, std::variant<int, std::string>>& sql_data);
    static std::vector<std::vector<std::string>> fetchall_from_db(const std::string& sql_command, const std::unordered_map<std::string, std::variant<int, std::string>>& sql_data);
    
    bool start();
    bool stop();
    bool restart();

private:
    // Helper methods for handling SQLite operations
    static std::variant<
        std::string,
        std::vector<std::string>,
        std::vector<std::vector<std::string>>
    > execute_sql(
        sqlite3* db,
        const std::string& sql_command,
        const std::unordered_map<std::string, std::variant<int, std::string>>& executing_args,
        const std::string& fetch
    );
    
    void database_handler();
    
    // Queue and thread for asynchronous database operations
    std::queue<std::tuple<std::string, std::unordered_map<std::string, std::variant<int, std::string>>, std::string>> db_q;
    std::thread db_thread;
    std::atomic<bool> stop_event;
    std::mutex queue_mutex;
    std::condition_variable cv;
    
    bool db_thread_running;
};
