#include <iomanip>
#include <iostream>
#include <string>
#include <vector>
#include <algorithm>

struct ResourceScenario {
    std::string key;
    std::string scenario_name;
    double initial_stock;
    double growth_rate;
    double carrying_capacity;
    double extraction;
    double climate_stress;
    int years;
    double minimum_stock;
};

struct Evaluation {
    double final_stock;
    double minimum_observed_stock;
    double minimum_resilience_margin;
    bool threshold_breach;
};

Evaluation evaluate(const ResourceScenario& scenario) {
    double stock = scenario.initial_stock;
    const double effective_growth = scenario.growth_rate * (1.0 - scenario.climate_stress);
    double min_stock = stock;
    double min_margin = stock - scenario.minimum_stock;

    for (int year = 0; year < scenario.years; ++year) {
        const double regeneration = effective_growth * stock * (1.0 - stock / scenario.carrying_capacity);
        stock = std::max(0.0, stock + regeneration - scenario.extraction);
        min_stock = std::min(min_stock, stock);
        min_margin = std::min(min_margin, stock - scenario.minimum_stock);
    }

    return {stock, min_stock, min_margin, min_stock < scenario.minimum_stock};
}

int main() {
    std::vector<ResourceScenario> scenarios = {
        {"baseline", "Baseline managed use", 420.0, 0.24, 800.0, 36.0, 0.04, 25, 250.0},
        {"high_extraction", "High extraction pressure", 420.0, 0.24, 800.0, 64.0, 0.04, 25, 250.0},
        {"climate_stress", "Climate stress with lower regeneration", 420.0, 0.24, 800.0, 42.0, 0.22, 25, 250.0},
        {"restoration_pathway", "Restoration and reduced extraction", 420.0, 0.28, 860.0, 24.0, 0.03, 25, 250.0},
        {"adaptive_management", "Adaptive use with monitoring trigger", 420.0, 0.25, 820.0, 32.0, 0.08, 25, 250.0}
    };

    std::cout << "key,final_stock,minimum_observed_stock,minimum_resilience_margin,threshold_breach\n";
    for (const auto& scenario : scenarios) {
        const Evaluation eval = evaluate(scenario);
        std::cout << std::fixed << std::setprecision(6)
                  << scenario.key << "," << eval.final_stock << ","
                  << eval.minimum_observed_stock << ","
                  << eval.minimum_resilience_margin << ","
                  << (eval.threshold_breach ? "true" : "false") << "\n";
    }

    return 0;
}
