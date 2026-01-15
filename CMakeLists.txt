cmake_minimum_required(VERSION 3.10)
project(LEDAnimationtool)

set(CMAKE_CXX_STANDARD 17)

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}/src
    ${CMAKE_SOURCE_DIR}
    ${CMAKE_SOURCE_DIR}/src/animation
    ${CMAKE_SOURCE_DIR}/src/util/configuration
    ${CMAKE_SOURCE_DIR}/src/util/database
    ${CMAKE_SOURCE_DIR}/src/util/database/sql
    ${CMAKE_SOURCE_DIR}/src/udp
    /usr/local/include/ws2811
)

# Source files
set(SOURCES
    src/main.cpp
    src/Color.cpp
    src/ColorSequence.cpp
    src/FrequencyColors.cpp
    src/Scene.cpp
    src/Section.cpp
    src/Strip.cpp

    src/animation/Animation.cpp
    src/animation/Strobe.cpp

    src/util/database/AnimationDB.cpp
    src/util/database/ColorDB.cpp
    src/util/database/ColorSequenceDB.cpp
    src/util/database/Database.cpp
    src/util/database/DetectionDB.cpp
    src/util/database/FrequencyColorDB.cpp
    src/util/database/InitializeDB.cpp
    src/util/database/SceneAnimationDB.cpp
    src/util/database/SceneDB.cpp
    src/util/database/SectionAnimationDB.cpp
    src/util/database/SectionDB.cpp

    src/util/configuration/AnimationData.cpp

    src/util/udp/ArtNetPacket.cpp
    src/util/udp/UDP.cpp
)

set(BUILD_TEST OFF CACHE BOOL "Disable rpi_ws281x test binary" FORCE)
add_subdirectory(rpi_ws281x)

# Add the executable
add_executable(LEDAnimationtool ${SOURCES})

# Find and link nlohmann_json (header-only dependency)
find_package(nlohmann_json CONFIG QUIET)
if(nlohmann_json_FOUND)
    target_link_libraries(LEDAnimationtool
        PRIVATE
        nlohmann_json::nlohmann_json
    )
else()
    find_path(NLOHMANN_JSON_INCLUDE_DIR nlohmann/json.hpp)
    if(NOT NLOHMANN_JSON_INCLUDE_DIR)
        message(FATAL_ERROR "nlohmann_json headers not found. Install nlohmann-json-dev or provide nlohmann/json.hpp.")
    endif()
    target_include_directories(LEDAnimationtool
        PRIVATE
        ${NLOHMANN_JSON_INCLUDE_DIR}
    )
endif()

# Find and link SQLite3
find_package(SQLite3 REQUIRED)
target_link_libraries(LEDAnimationtool
    PRIVATE
    SQLite::SQLite3
)

find_package(Threads REQUIRED)

# Link against ws2811 and stdc++fs
target_link_libraries(LEDAnimationtool
    PRIVATE
    Threads::Threads
    ws2811
    stdc++fs
)
