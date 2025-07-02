cmake_minimum_required(VERSION 3.31)
project(hello)

set(CMAKE_CXX_STANDARD 20)
set(CMAKE_AUTOMOC ON)
set(CMAKE_AUTORCC ON)
set(CMAKE_AUTOUIC ON)

set(CMAKE_PREFIX_PATH "/home/mjbhobe/Qt/6.8.1")

find_package(Qt6 COMPONENTS
        Core
        Gui
        Widgets
        REQUIRED)

add_executable(sysmets main.cpp SysmetsModel.cpp)
target_link_libraries(sysmets
        Qt::Core
        Qt::Gui
        Qt::Widgets
)

