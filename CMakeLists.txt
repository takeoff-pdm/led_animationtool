cmake_minimum_required(VERSION 3.10)
project(LEDAnimationtool)

set(CMAKE_CXX_STANDARD 17)

# Include directories
include_directories(
    ${CMAKE_SOURCE_DIR}/src
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

    src/util/udp/UDP.cpp
)

# Add the executable
add_executable(LEDAnimationtool ${SOURCES})

# Find Boost
set(BOOST_ROOT "/usr/local/include/")
set(Boost_NO_SYSTEM_PATHS FALSE)
find_package(Boost 1.88 REQUIRED COMPONENTS system thread)
include_directories(${Boost_INCLUDE_DIRS})

# Link Boost libraries
target_link_libraries(LEDAnimationtool
    PRIVATE
    ${Boost_LIBRARIES}
)

# Find and link SQLite3
find_package(SQLite3 REQUIRED)
target_link_libraries(LEDAnimationtool
    PRIVATE
    SQLite::SQLite3
)

# Link against ws2811 and stdc++fs
target_link_libraries(LEDAnimationtool
    PRIVATE
    ws2811
    stdc++fs
)
