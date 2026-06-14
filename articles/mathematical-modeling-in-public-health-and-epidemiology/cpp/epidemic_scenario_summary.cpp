#include <algorithm>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct EpidemicScenario {
    std::string key;
    std::string scenario_name;
    double population;
    double initial_infectious;
    double initial_recovered;
    double beta;
    double gamma;
    int days;
    double hospital_capacity;
    double hospitalization_rate;
};

struct Evaluation {
    double r0_simple;
    double peak_infectious;
    double peak_hospital_demand;
    double capacity_margin;
    bool capacity_breach;
};

Evaluation evaluate(const EpidemicScenario& scenario) {
    double susceptible = scenario.population - scenario.initial_infectious - scenario.initial_recovered;
    double infectious = scenario.initial_infectious;
    double recovered = scenario.initial_recovered;
    double peak_infectious = infectious;
    double peak_hospital_demand = infectious * scenario.hospitalization_rate;

    for (int day = 0; day < scenario.days; ++day) {
        const double new_infections = scenario.beta * susceptible * infectious / scenario.population;
        const double new_recoveries = scenario.gamma * infectious;
        susceptible = std::max(0.0, susceptible - new_infections);
        infectious = std::max(0.0, infectious + new_infections - new_recoveries);
        recovered = std::min(scenario.population, recovered + new_recoveries);
        peak_infectious = std::max(peak_infectious, infectious);
        peak_hospital_demand = std::max(peak_hospital_demand, infectious * scenario.hospitalization_rate);
    }

    return {
        scenario.beta / scenario.gamma,
        peak_infectious,
        peak_hospital_demand,
        scenario.hospital_capacity - peak_hospital_demand,
        peak_hospital_demand > scenario.hospital_capacity
    };
}

int main() {
    std::vector<EpidemicScenario> scenarios = {
        {"baseline", "Baseline transmission", 100000.0, 120.0, 4000.0, 0.32, 0.12, 120, 850.0, 0.045},
        {"moderate_intervention", "Moderate intervention", 100000.0, 120.0, 4000.0, 0.24, 0.12, 120, 850.0, 0.045},
        {"strong_intervention", "Strong intervention", 100000.0, 120.0, 4000.0, 0.18, 0.12, 120, 850.0, 0.045},
        {"vaccination_plus_intervention", "Vaccination plus intervention", 100000.0, 120.0, 22000.0, 0.20, 0.12, 120, 850.0, 0.030}
    };

    std::cout << "key,r0_simple,peak_infectious,peak_hospital_demand,capacity_margin,capacity_breach\n";
    for (const auto& scenario : scenarios) {
        const Evaluation eval = evaluate(scenario);
        std::cout << std::fixed << std::setprecision(6)
                  << scenario.key << "," << eval.r0_simple << ","
                  << eval.peak_infectious << "," << eval.peak_hospital_demand << ","
                  << eval.capacity_margin << ","
                  << (eval.capacity_breach ? "true" : "false") << "\n";
    }

    return 0;
}
