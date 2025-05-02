#include "InitializeDB.hpp"
#include <iostream>
#include <fstream>
#include <filesystem>
#include <sqlite3.h>

static const std::string DATABASE_FILE = "db.db";

// Function to create tables from the SQL file
bool InitializeDB::create_tables(sqlite3* db) {
    std::string sql_file_path = std::filesystem::current_path().string() + "/util/database/sql/db.sql";

    // Read the SQL script from the file
    std::ifstream sql_file(sql_file_path);
    if (!sql_file.is_open()) {
        std::cerr << "Error: Could not open SQL file at " << sql_file_path << std::endl;
        return false;
    }

    std::string sql_script((std::istreambuf_iterator<char>(sql_file)),
                           std::istreambuf_iterator<char>());

    // Execute the script
    char* err_msg = nullptr;
    int rc = sqlite3_exec(db, sql_script.c_str(), nullptr, nullptr, &err_msg);
    if (rc != SQLITE_OK) {
        std::cerr << "SQL error: " << err_msg << std::endl;
        sqlite3_free(err_msg);
        return false;
    }

    return true;
}

// Function to create the database file and required tables
bool InitializeDB::create_database(bool overwrite) {
    // Check if the database already exists
    if (std::filesystem::exists(DATABASE_FILE) && !overwrite) {
        std::cout << "Database already exists, not overwriting" << std::endl;
        return false;
    }

    // Create a new database connection
    sqlite3* db;
    int rc = sqlite3_open(DATABASE_FILE.c_str(), &db);
    if (rc) {
        std::cerr << "Cannot open database: " << sqlite3_errmsg(db) << std::endl;
        return false;
    }

    // Create the tables
    if (!create_tables(db)) {
        sqlite3_close(db);
        return false;
    }

    // Commit and close the database connection
    sqlite3_close(db);
    return true;
}
