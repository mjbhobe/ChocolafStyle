//
// Created by manis on 07-May-26.
//

#ifndef __STL_LOGGING_HPP__
#define __STL_LOGGING_HPP__

#include <string>
#include <spdlog/common.h> // Required for spdlog::level::level_enum

void setup_logger(
    std::string pattern = "%^[%l] [%s] [%T] %v%$",
    spdlog::level::level_enum level = spdlog::level::debug,
    bool log_to_file = false
);

#endif //__STL_LOGGING_HPP__