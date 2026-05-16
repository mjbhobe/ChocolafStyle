#pragma once
#include "loguru.hpp"

void setup_logging(int argc, char *argv[], bool log_to_file = false);

#define LOG_DEBUG(...) LOG_F(1, __VA_ARGS__)
#define LOG_INFO(...) LOG_F(INFO, __VA_ARGS__)
#define LOG_WARN(...) LOG_F(WARNING, __VA_ARGS__)
#define LOG_ERROR(...) LOG_F(ERROR, __VA_ARGS__)
#define LOG_CRITICAL(...) LOG_F(FATAL, __VA_ARGS__)


/*
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
*/
