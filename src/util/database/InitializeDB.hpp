#pragma once

#include <string>
#include <sqlite3.h>

class InitializeDB {
public:
    static bool create_database(bool overwrite);
    static bool create_tables(sqlite3* db);

private:
    static std::string get_db_file_path();
};
