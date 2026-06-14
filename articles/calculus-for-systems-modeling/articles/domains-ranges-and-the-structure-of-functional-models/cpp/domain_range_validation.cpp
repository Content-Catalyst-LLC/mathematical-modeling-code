#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Scenario { std::string name; double initial_state; double rate; double capacity; double time_horizon; };

std::string validate_domain(const Scenario& s) {
    if (s.initial_state < 0.0) return "initial_state must be nonnegative";
    if (s.rate < 0.0) return "rate must be nonnegative";
    if (s.capacity <= 0.0) return "capacity must be positive";
    if (s.time_horizon < 0.0) return "time_horizon must be nonnegative";
    if (s.initial_state > s.capacity) return "initial_state exceeds capacity";
    return "";
}

double bounded_growth(const Scenario& s) {
    return s.capacity / (1.0 + ((s.capacity - s.initial_state) / s.initial_state) * std::exp(-s.rate * s.time_horizon));
}

int main() {
    std::vector<Scenario> scenarios = {
        {"baseline", 10.0, 0.20, 100.0, 20.0},
        {"near_capacity", 95.0, 0.20, 100.0, 20.0},
        {"invalid_negative_state", -5.0, 0.20, 100.0, 20.0},
        {"outside_capacity", 120.0, 0.20, 100.0, 20.0}
    };
    std::cout << "scenario,status,value_or_issue\n";
    for (const auto& s : scenarios) {
        auto issue = validate_domain(s);
        if (!issue.empty()) std::cout << s.name << ",domain_review," << issue << "\n";
        else std::cout << s.name << ",ok," << std::fixed << std::setprecision(6) << bounded_growth(s) << "\n";
    }
}
