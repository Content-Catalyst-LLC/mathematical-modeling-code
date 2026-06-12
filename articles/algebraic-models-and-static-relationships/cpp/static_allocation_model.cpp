#include <iomanip>
#include <iostream>
#include <stdexcept>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    double budget;
    double cost_a;
    double cost_b;
    double benefit_a;
    double benefit_b;
    double allocation_a;
    double allocation_b;
    double capacity_a;
    double capacity_b;
};

struct Result {
    double total_cost;
    double total_benefit;
    double benefit_per_cost;
    double budget_slack;
    bool feasible;
};

Result evaluate(const Scenario& s) {
    if (s.budget <= 0.0) throw std::invalid_argument("budget must be positive");
    if (s.cost_a <= 0.0 || s.cost_b <= 0.0) throw std::invalid_argument("costs must be positive");

    const double total_cost = s.cost_a * s.allocation_a + s.cost_b * s.allocation_b;
    const double total_benefit = s.benefit_a * s.allocation_a + s.benefit_b * s.allocation_b;
    const double budget_slack = s.budget - total_cost;
    const bool feasible = budget_slack >= 0.0
        && s.capacity_a - s.allocation_a >= 0.0
        && s.capacity_b - s.allocation_b >= 0.0;

    return {
        total_cost,
        total_benefit,
        total_cost > 0.0 ? total_benefit / total_cost : 0.0,
        budget_slack,
        feasible
    };
}

int main() {
    std::vector<Scenario> scenarios = {
        {"cpp_balanced_feasible", 100.0, 4.0, 5.0, 8.0, 11.0, 10.0, 8.0, 20.0, 15.0},
        {"cpp_capacity_stress", 120.0, 4.0, 5.0, 8.0, 11.0, 25.0, 5.0, 20.0, 15.0}
    };

    for (const auto& scenario : scenarios) {
        const auto result = evaluate(scenario);
        std::cout << std::fixed << std::setprecision(6)
                  << scenario.name
                  << " total_cost=" << result.total_cost
                  << " total_benefit=" << result.total_benefit
                  << " benefit_per_cost=" << result.benefit_per_cost
                  << " budget_slack=" << result.budget_slack
                  << " feasible=" << (result.feasible ? "true" : "false")
                  << "\n";
    }

    return 0;
}
