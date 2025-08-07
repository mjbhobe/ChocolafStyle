cmake_minimum_required(VERSION 3.31)
project(list_widget)

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

include_directories(
    "/home/mjbhobe/code/git-projects/ChocolafStyle/chocolaf/common_files/"
    "/home/mjbhobe/code/git-projects/ChocolafStyle/chocolaf/common_files/argparse"
    "/home/mjbhobe/code/git-projects/ChocolafStyle/chocolaf/common_files/QtAwesome"
)

add_executable(list_widget main.cpp list_widget.cpp qactionpushbtn.cpp)
target_link_libraries(list_widget
    Qt::Core
    Qt::Gui
    Qt::Widgets
)

