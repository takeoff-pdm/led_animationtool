#include "Database.hpp"
#include "InitializeDB.hpp"
#include <iostream>
#include <chrono>
#include <thread>
#include <sqlite3.h>

#define DATABASE_FILE "db.db"

// Constructor
Database::Database(bool manual) : stop_event(false), db_thread_running(false) {
    // Initialize the database file and create tables if necessary
    InitializeDB::create_database(false);
    
    if (!manual) {
        db_thread_running = start();
    }
}

// Destructor
Database::~Database() {
    stop();
    if (db_thread.joinable()) {
        db_thread.join();
    }
}

// Push SQL command to the database
bool Database::push_to_db(const std::string& sql_command, const std::unordered_map<std::string, std::variant<int, std::string>>& sql_data) {
    sqlite3* db;
    sqlite3_open(DATABASE_FILE, &db);

    // Print SQL command for debugging
    // std::cout << "[Database::push_to_db] SQL Command: " << sql_command << "\n";
    // std::cout << "[Database::push_to_db] SQL Data:\n";
    for (const auto& pair : sql_data) {
        // std::cout << pair.first << ": " 
        //          << (std::holds_alternative<int>(pair.second) ? std::to_string(std::get<int>(pair.second)) : std::get<std::string>(pair.second)) 
        //          << "\n";
    }

    try {
        execute_sql(db, sql_command, sql_data, "");
    } catch (...) {
        // std::cout << "[Database] Error while pushing to the database." << std::endl;
        sqlite3_close(db);
        return false;
    }

    sqlite3_close(db);
    return true;
}

// Fetch one row from the database
std::vector<std::string> Database::fetchone_from_db(
    const std::string& sql_command,
    const std::unordered_map<std::string, std::variant<int, std::string>>& sql_data) 
{
    sqlite3* db;
    sqlite3_open(DATABASE_FILE, &db);

    // Print SQL command for debugging
    // std::cout << "[Database::fetchone_from_db] SQL Command: " << sql_command << "\n";
    // std::cout << "[Database::fetchone_from_db] SQL Data:\n";
    for (const auto& pair : sql_data) {
        // std::cout << pair.first << ": " 
        //          << (std::holds_alternative<int>(pair.second) ? std::to_string(std::get<int>(pair.second)) : std::get<std::string>(pair.second)) 
        //          << "\n";
    }
    // std::cout << "[Database::fetchone_from_db] Fetch Type: one\n";

    auto result = execute_sql(db, sql_command, sql_data, "one");

    sqlite3_close(db);

    if (std::holds_alternative<std::vector<std::string>>(result)) {
        // std::cout << "[Database::fetchone_from_db] Response (one):\n";
        for (const auto& col : std::get<std::vector<std::string>>(result)) {
            // std::cout << col << " ";
        }
        // std::cout << "\n";
        return std::get<std::vector<std::string>>(result);
    } 
    else if (std::holds_alternative<std::vector<std::vector<std::string>>>(result)) {
        // std::cout << "[Database::fetchone_from_db] Response (multi):\n";
        const auto& allRows = std::get<std::vector<std::vector<std::string>>>(result);
        for (const auto& row : allRows) {
            for (const auto& col : row) {
                // std::cout << col << " ";
            }
            // std::cout << "\n";
        }
        return allRows.empty() ? std::vector<std::string>{} : allRows[0];
    } 
    else if (std::holds_alternative<std::string>(result)) {
        // std::cout << "[Database::fetchone_from_db] Error: " << std::get<std::string>(result) << "\n";
        return {};
    } 
    else {
        // std::cout << "[Database::fetchone_from_db] Unexpected result type.\n";
        return {};
    }
}


std::vector<std::vector<std::string>> Database::fetchall_from_db(
    const std::string& sql_command,
    const std::unordered_map<std::string, std::variant<int, std::string>>& sql_data) 
{
    sqlite3* db;
    sqlite3_open(DATABASE_FILE, &db);

    // Print SQL command for debugging
    // std::cout << "[Database::fetchone_from_db] SQL Command: " << sql_command << "\n";
    // std::cout << "[Database::fetchone_from_db] SQL Data: \n";
    for (const auto& pair : sql_data) {
        // std::cout << pair.first << ": " << (std::holds_alternative<int>(pair.second) ? std::to_string(std::get<int>(pair.second)) : std::get<std::string>(pair.second)) << "\n";
    }
    // std::cout << "[Database::fetchone_from_db] Fetch Type: all\n";

    auto result = execute_sql(db, sql_command, sql_data, "all");

    sqlite3_close(db);

    if (std::holds_alternative<std::vector<std::vector<std::string>>>(result)) {
        // Print response for debugging
        // std::cout << "[Database::fetchall_from_db] Response (multi): \n";
        for (const auto& row : std::get<std::vector<std::vector<std::string>>>(result)) {
            for (const auto& col : row) {
                // std::cout << col << " ";
            }
            // std::cout << "\n";
        }
        return std::get<std::vector<std::vector<std::string>>>(result);
    } else if (std::holds_alternative<std::vector<std::string>>(result)) {
        // Print response for debugging
        // std::cout << "[Database::fetchall_from_db] Response (one): \n";
        for (const auto& col : std::get<std::vector<std::string>>(result)) {
            // std::cout << col << " ";
        }
        // std::cout << "\n";
        return { std::get<std::vector<std::string>>(result) };  // Wrap single row in a vector
    } else if (std::holds_alternative<std::string>(result)) {
        // std::cout << "[Database::fetchall_from_db] Error: " << std::get<std::string>(result) << "\n";
        return {};  // or throw
    } else {
        // std::cout << "[Database::fetchall_from_db] Unexpected result type.\n";
        return {};  // or throw
    }
}

std::variant<
        std::string,
        std::vector<std::string>,
        std::vector<std::vector<std::string>>
    > Database::execute_sql(
        sqlite3* db,
        const std::string& sql_command,
        const std::unordered_map<std::string, std::variant<int, std::string>>& executing_args,
        const std::string& fetch) {
    sqlite3_stmt* stmt;
    int rc = sqlite3_prepare_v2(db, sql_command.c_str(), -1, &stmt, nullptr);
    if (rc != SQLITE_OK) {
        return "Failed to prepare statement: " + std::string(sqlite3_errmsg(db));
    }

    // Bind named parameters
    for (const auto& pair : executing_args) {
        const std::string& name = pair.first;
        int idx = sqlite3_bind_parameter_index(stmt, (":" + name).c_str());

        if (idx == 0) {
            std::cerr << "Warning: parameter name not found in SQL: " << name << "\n";
            continue;
        }

        if (std::holds_alternative<int>(pair.second)) {
            sqlite3_bind_int(stmt, idx, std::get<int>(pair.second));
        } else {
            sqlite3_bind_text(stmt, idx, std::get<std::string>(pair.second).c_str(), -1, SQLITE_STATIC);
        }
    }

    // Execute and handle fetch
    std::vector<std::string> singleRow;
    std::vector<std::vector<std::string>> allRows;

    int stepResult = sqlite3_step(stmt);

    if (fetch == "one") {
        if (stepResult == SQLITE_ROW) {
            int cols = sqlite3_column_count(stmt);
            for (int i = 0; i < cols; ++i) {
                const char* colText = reinterpret_cast<const char*>(sqlite3_column_text(stmt, i));
                singleRow.push_back(colText ? colText : "NULL");
            }
        }
    } else if (fetch == "all") {
        while (stepResult == SQLITE_ROW) {
            std::vector<std::string> row;
            int cols = sqlite3_column_count(stmt);
            for (int i = 0; i < cols; ++i) {
                const char* colText = reinterpret_cast<const char*>(sqlite3_column_text(stmt, i));
                row.push_back(colText ? colText : "NULL");
            }
            allRows.push_back(row);
            stepResult = sqlite3_step(stmt);
        }
    }

    sqlite3_finalize(stmt);
    sqlite3_exec(db, "COMMIT;", nullptr, nullptr, nullptr);

    // Return based on fetch
    if (fetch == "one") return singleRow;
    if (fetch == "all") return allRows;
    return {};  // No fetch — return empty result
}

// Database handler for the worker thread
void Database::database_handler() {
    sqlite3* db;
    sqlite3_open(DATABASE_FILE, &db);

    while (!stop_event.load()) {
        std::unique_lock<std::mutex> lock(queue_mutex);
        cv.wait(lock, [this] { return !db_q.empty() || stop_event.load(); });

        if (stop_event.load()) {
            break;
        }

        auto sql_data = db_q.front();
        db_q.pop();

        // Execute the SQL operation from the queue
        execute_sql(db, std::get<0>(sql_data), std::get<1>(sql_data), std::get<2>(sql_data));

        // Handle callback or further operations if required

        lock.unlock();
    }

    sqlite3_close(db);
}

// Start the database thread
bool Database::start() {
    if (db_thread_running) {
        return false;
    }

    stop_event.store(false);
    db_thread = std::thread(&Database::database_handler, this);
    db_thread_running = true;
    return true;
}

// Stop the database thread
bool Database::stop() {
    if (!db_thread_running) {
        return false;
    }

    stop_event.store(true);
    cv.notify_all();

    if (db_thread.joinable()) {
        db_thread.join();
    }

    db_thread_running = false;
    return true;
}

// Restart the database thread
bool Database::restart() {
    if (stop()) {
        return start();
    }
    return false;
}
