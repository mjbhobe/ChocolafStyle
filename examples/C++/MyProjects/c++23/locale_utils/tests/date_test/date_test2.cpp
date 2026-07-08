// tests/date_test/date_test2.cpp
#include <chrono>
#include <iostream>
#include <locale>

int main() {
    using namespace std::chrono;
    auto tp = sys_days{2026y / July / 8};

    for (const auto &locale_name : {"en_US.utf8", "fr_FR.utf8", "ru_RU.utf8", "de_DE.utf8"}) {
        std::locale loc(locale_name);
        std::cout << locale_name
                   << " -> %x=" << std::format(loc, "{:%x}", tp)
                   << " %A=" << std::format(loc, "{:%A}", tp)
                   << " %B=" << std::format(loc, "{:%B}", tp) << '\n';
    }
    return 0;
}
