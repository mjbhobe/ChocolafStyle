// -------------------------------------------------------


#define SPDLOG_ACTIVE_LEVEL SPDLOG_LEVEL_DEBUG
#include "logging.h"
#include <spdlog/spdlog.h>
#include <spdlog/sinks/ansicolor_sink.h>
#include <spdlog/sinks/basic_file_sink.h>
#include <filesystem>
#include <chrono>
#include <format>
#include <vector>

// Windows-specific header for console mode
#ifdef _WIN32
#include <windows.h>
#endif

void setup_logger(
    std::string pattern /*= "%^[%l] [%s] [%T] %v%$"*/,
    spdlog::level::level_enum level /*= spdlog::level::debug*/,
    bool log_to_file /*= false*/
)
{
  // --- Windows ANSI Support Initialization ---
#ifdef _WIN32
  HANDLE hOut = GetStdHandle(STD_OUTPUT_HANDLE);
  if (hOut != INVALID_HANDLE_VALUE) {
    DWORD dwMode = 0;
    if (GetConsoleMode(hOut, &dwMode)) {
      dwMode |= ENABLE_VIRTUAL_TERMINAL_PROCESSING;
      SetConsoleMode(hOut, dwMode);
    }
  }
#endif

  std::vector<spdlog::sink_ptr> sinks;

  // 1. Console Sink (ANSI)
  auto console_sink = std::make_shared<spdlog::sinks::ansicolor_stdout_sink_mt>();
  console_sink->set_color(spdlog::level::debug, "\033[32m");
  console_sink->set_color(spdlog::level::info,  "\033[34m");
  console_sink->set_color(spdlog::level::warn,  "\033[38;5;210m");
  console_sink->set_color(spdlog::level::err,   "\033[38;5;205m");
  sinks.push_back(console_sink);

  // 2. File Sink
  if (log_to_file) {
    std::filesystem::create_directory("logs");
    auto now = std::chrono::system_clock::now();
    std::string filename = std::format("logs/log_{:%Y%m%d_%H%M%S}.log", now);
    auto file_sink = std::make_shared<spdlog::sinks::basic_file_sink_mt>(filename, true);
    sinks.push_back(file_sink);
  }

  // 3. Global Configuration
  auto logger = std::make_shared<spdlog::logger>("multi_sink", sinks.begin(), sinks.end());
  spdlog::set_default_logger(logger);
  spdlog::set_pattern(pattern);
  spdlog::set_level(level);
  spdlog::flush_on(spdlog::level::trace);
}



/** Usage examples ----
int main() {
  setup_logger();

  spdlog::debug("System scan complete. No threats found.");
  spdlog::info("Application started on Windows/Linux port.");
  spdlog::warn("Memory usage is higher than 80%.");
  spdlog::error("Failed to write to config.json!");
  spdlog::critical("Kernel panic simulated!");

  // NOTE: if you want your logging format to ALSO include file
  // name from where the logging message originated then ALWAYS
  // use these macros to log
  SPDLOG_DEBUG("This is green and shows the filename.");
  SPDLOG_INFO("This is blue.");
  SPDLOG_WARN("This is light pink.");
  SPDLOG_ERROR("This is salmon red.");

  return 0;
}
*/