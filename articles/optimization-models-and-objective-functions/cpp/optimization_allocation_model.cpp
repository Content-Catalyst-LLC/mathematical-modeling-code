#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Program {
    std::string name;
    double benefit;
    double cost;
    int lower;
    int upper;
};

struct Scenario {
    std::string name;
    double budget;
    int equity_floor;
};

int main() {
    const std::vector<Program> programs = {
        {"housing", 11.0, 7.0, 0, 8},
        {"health", 13.0, 8.0, 0, 8},
        {"transport", 8.0, 5.0, 0, 8},
        {"resilience", 10.0, 6.0, 0, 8}
    };

    const Scenario scenario{"cpp_baseline", 75.0, 1};

    double best_benefit = -1.0;
    std::vector<int> best_allocation;
    int feasible_count = 0;
    int candidate_count = 0;

    for (int a = 0; a <= 8; ++a) {
        for (int b = 0; b <= 8; ++b) {
            for (int c = 0; c <= 8; ++c) {
                for (int d = 0; d <= 8; ++d) {
                    const std::vector<int> x = {a, b, c, d};
                    double total_cost = 0.0;
                    double total_benefit = 0.0;
                    bool equity_ok = true;

                    for (std::size_t i = 0; i < programs.size(); ++i) {
                        total_cost += x[i] * programs[i].cost;
                        total_benefit += x[i] * programs[i].benefit;
                        if (x[i] < scenario.equity_floor) {
                            equity_ok = false;
                        }
                    }

                    ++candidate_count;
                    const bool feasible = total_cost <= scenario.budget && equity_ok;

                    if (feasible) {
                        ++feasible_count;
                        if (total_benefit > best_benefit) {
                            best_benefit = total_benefit;
                            best_allocation = x;
                        }
                    }
                }
            }
        }
    }

    std::cout << std::fixed << std::setprecision(2)
              << "cpp candidates=" << candidate_count
              << " feasible=" << feasible_count
              << " best_benefit=" << best_benefit
              << " best_allocation=[";

    for (std::size_t i = 0; i < best_allocation.size(); ++i) {
        if (i > 0) std::cout << ",";
        std::cout << best_allocation[i];
    }

    std::cout << "]\n";
    return 0;
}
