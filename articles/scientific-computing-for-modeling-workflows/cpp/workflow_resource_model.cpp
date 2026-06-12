#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    double initial_stock;
    double growth_rate;
    double carrying_capacity;
    double extraction;
    int steps;
};

double simulate(const Scenario& s) {
    double stock = s.initial_stock;
    for (int step = 0; step < s.steps; ++step) {
        const double growth = s.growth_rate * stock * (1.0 - stock / s.carrying_capacity);
        stock = std::max(0.0, stock + growth - s.extraction);
    }
    return stock;
}

int main() {
    std::vector<Scenario> scenarios = {
        {"baseline", 70.0, 0.18, 100.0, 6.0, 50},
        {"stress", 70.0, 0.15, 100.0, 9.0, 50},
        {"recovery_policy", 70.0, 0.18, 100.0, 5.0, 50}
    };

    std::cout << "scenario,final_stock\n";
    for (const auto& scenario : scenarios) {
        std::cout << scenario.name << "," << std::fixed << std::setprecision(6)
                  << simulate(scenario) << "\n";
    }

    return 0;
}
