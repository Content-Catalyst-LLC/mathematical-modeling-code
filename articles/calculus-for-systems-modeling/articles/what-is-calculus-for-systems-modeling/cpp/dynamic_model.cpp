#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    double initial_state;
    double rate;
    double capacity;
    double dt;
    int steps;
};

double simulate(const Scenario& s) {
    double state = s.initial_state;
    for (int i = 0; i < s.steps; ++i) {
        const double derivative = s.rate * state * (1.0 - state / s.capacity);
        state = std::max(0.0, state + derivative * s.dt);
    }
    return state;
}

int main() {
    std::vector<Scenario> scenarios = {
        {"baseline", 10.0, 0.20, 100.0, 0.1, 300},
        {"slow_adjustment", 10.0, 0.10, 100.0, 0.1, 300},
        {"high_capacity", 10.0, 0.20, 140.0, 0.1, 300}
    };

    std::cout << "scenario,final_state\n";
    for (const auto& s : scenarios) {
        std::cout << s.name << "," << std::fixed << std::setprecision(6) << simulate(s) << "\n";
    }
    return 0;
}
