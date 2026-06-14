#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct DecisionOption {
    std::string key;
    std::string name;
    double expected_stock;
    double lower_bound;
    double upper_bound;
    double burden;
    double consequence_if_wrong;
};

double decision_score(const DecisionOption& option) {
    const double threshold_penalty = option.lower_bound < 45.0 ? 8.0 : 0.0;
    return option.expected_stock - 0.8 * option.burden - 1.2 * option.consequence_if_wrong - threshold_penalty;
}

int main() {
    std::vector<DecisionOption> options = {
        {"no_action", "No immediate action", 52.0, 38.0, 66.0, 1.0, 9.0},
        {"monitoring", "Formal monitoring", 54.0, 42.0, 68.0, 3.0, 6.0},
        {"moderate_intervention", "Moderate intervention", 60.0, 50.0, 72.0, 5.0, 4.0},
        {"strong_intervention", "Strong intervention", 68.0, 58.0, 78.0, 8.0, 2.0}
    };

    std::cout << "key,option_name,decision_score,threshold_margin,robustness_class\n";
    for (const auto& option : options) {
        const std::string robustness_class = option.lower_bound >= 45.0 ? "robust" : "fragile";
        std::cout << std::fixed << std::setprecision(3)
                  << option.key << "," << option.name << "," << decision_score(option) << ","
                  << option.expected_stock - 45.0 << "," << robustness_class << "\n";
    }

    return 0;
}
