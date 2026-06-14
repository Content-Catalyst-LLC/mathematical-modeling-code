#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct PopulationScenario {
    std::string key;
    double growth_rate;
    double carrying_capacity;
    double initial_population;
    int years;
};

double logistic_final(const PopulationScenario& scenario) {
    double population = scenario.initial_population;
    for (int year = 0; year < scenario.years; ++year) {
        population = population + scenario.growth_rate * population * (1.0 - population / scenario.carrying_capacity);
    }
    return population;
}

int main() {
    std::vector<PopulationScenario> scenarios = {
        {"baseline", 0.28, 500.0, 40.0, 20},
        {"lower_growth", 0.18, 500.0, 40.0, 20},
        {"higher_growth", 0.38, 500.0, 40.0, 20},
        {"lower_capacity", 0.28, 350.0, 40.0, 20},
        {"higher_capacity", 0.28, 700.0, 40.0, 20}
    };

    std::cout << "key,growth_rate,carrying_capacity,initial_population,years,final_population,crosses_capacity_midpoint\n";
    for (const auto& scenario : scenarios) {
        const double final_population = logistic_final(scenario);
        const bool crosses = final_population >= scenario.carrying_capacity / 2.0;
        std::cout << std::fixed << std::setprecision(6)
                  << scenario.key << "," << scenario.growth_rate << "," << scenario.carrying_capacity << ","
                  << scenario.initial_population << "," << scenario.years << "," << final_population << ","
                  << (crosses ? "true" : "false") << "\n";
    }

    return 0;
}
