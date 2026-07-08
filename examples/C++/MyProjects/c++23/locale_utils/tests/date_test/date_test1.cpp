// tests/date_test/date_test1.cpp
#include <chrono>
#include <iostream>

int main() {
    using namespace std::chrono;
    // A fixed, known instant so every reader sees the same numbers.
    auto tp = sys_days{2026y / July / 8};

    std::cout << "Date: " << tp << '\n';
    return 0;
}
