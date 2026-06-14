#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct ComplexityScenario {
    std::string key;
    std::string scenario_name;
    double stress_level;
    double interdependence_level;
    double uncertainty_level;
    double resilience_score;
    double equity_score;
    double adaptability_score;
};

double fragility_score(const ComplexityScenario& s) {
    return 0.35 * s.stress_level +
           0.30 * s.interdependence_level +
           0.25 * s.uncertainty_level +
           0.10 * (1.0 - s.adaptability_score);
}

double robust_value(const ComplexityScenario& s) {
    const double f = fragility_score(s);
    return 0.40 * s.resilience_score +
           0.30 * s.equity_score +
           0.30 * s.adaptability_score -
           0.20 * f;
}

int main() {
    std::vector<ComplexityScenario> scenarios = {
        {"baseline", "Baseline stress", 0.35, 0.45, 0.40, 0.72, 0.68, 0.65},
        {"compound_shock", "Compound shock", 0.78, 0.70, 0.72, 0.48, 0.52, 0.55},
        {"cascading_failure", "Cascading failure", 0.88, 0.86, 0.75, 0.32, 0.40, 0.42},
        {"adaptive_pathway", "Adaptive pathway", 0.65, 0.68, 0.70, 0.66, 0.70, 0.82}
    };

    std::cout << "key,stress_level,interdependence_level,uncertainty_level,resilience_score,equity_score,adaptability_score,fragility_score,robust_value\n";
    for (const auto& scenario : scenarios) {
        std::cout << std::fixed << std::setprecision(6)
                  << scenario.key << ","
                  << scenario.stress_level << ","
                  << scenario.interdependence_level << ","
                  << scenario.uncertainty_level << ","
                  << scenario.resilience_score << ","
                  << scenario.equity_score << ","
                  << scenario.adaptability_score << ","
                  << fragility_score(scenario) << ","
                  << robust_value(scenario) << "\n";
    }

    return 0;
}
