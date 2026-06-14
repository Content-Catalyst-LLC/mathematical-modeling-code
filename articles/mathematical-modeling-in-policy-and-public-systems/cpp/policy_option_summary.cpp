#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct PolicyOption {
    std::string key;
    std::string option_name;
    double projected_benefit;
    double total_cost;
    double feasibility;
    double equity_score;
    double uncertainty_width;
    double public_risk;
};

double public_value_score(const PolicyOption& option) {
    const double budget_penalty = option.total_cost > 40.0 ? 14.0 : 0.0;
    return option.projected_benefit
        + 18.0 * option.feasibility
        + 24.0 * option.equity_score
        - option.total_cost
        - 0.22 * option.uncertainty_width
        - 30.0 * option.public_risk
        - budget_penalty;
}

int main() {
    std::vector<PolicyOption> options = {
        {"baseline", "Maintain current services", 42.0, 18.0, 0.86, 0.52, 18.0, 0.42},
        {"targeted_prevention", "Targeted prevention program", 68.0, 32.0, 0.74, 0.78, 22.0, 0.30},
        {"broad_expansion", "Broad service expansion", 81.0, 49.0, 0.58, 0.69, 28.0, 0.34},
        {"adaptive_pathway", "Adaptive pathway with monitoring triggers", 73.0, 38.0, 0.70, 0.82, 16.0, 0.24}
    };

    std::cout << "key,projected_benefit,total_cost,equity_score,public_risk,public_value_score,budget_violation\n";
    for (const auto& option : options) {
        std::cout << std::fixed << std::setprecision(6)
                  << option.key << "," << option.projected_benefit << "," << option.total_cost << ","
                  << option.equity_score << "," << option.public_risk << ","
                  << public_value_score(option) << ","
                  << (option.total_cost > 40.0 ? "true" : "false") << "\n";
    }

    return 0;
}
