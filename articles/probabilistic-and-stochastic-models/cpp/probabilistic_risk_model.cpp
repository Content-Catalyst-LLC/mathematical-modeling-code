#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <numeric>
#include <random>
#include <stdexcept>
#include <string>
#include <vector>

struct Scenario {
    std::string name;
    double demand_mu;
    double demand_sigma;
    double supply_mean;
    double supply_sd;
    double reserve;
    int simulations;
    unsigned int seed;
};

double quantile(std::vector<double> values, double p) {
    std::sort(values.begin(), values.end());
    const auto idx = static_cast<std::size_t>(std::round(p * static_cast<double>(values.size() - 1)));
    return values.at(std::min(idx, values.size() - 1));
}

int main() {
    Scenario scenario{"cpp_baseline", 4.50, 0.25, 95.0, 8.0, 5.0, 5000, 101};

    if (scenario.simulations < 100) throw std::invalid_argument("simulations must be at least 100");

    std::mt19937 rng(scenario.seed);
    std::normal_distribution<double> demand_noise(0.0, 1.0);
    std::normal_distribution<double> supply_dist(scenario.supply_mean, scenario.supply_sd);

    std::vector<double> shortages;
    shortages.reserve(static_cast<std::size_t>(scenario.simulations));
    int shortage_events = 0;

    for (int i = 0; i < scenario.simulations; ++i) {
        const double demand = std::exp(scenario.demand_mu + scenario.demand_sigma * demand_noise(rng));
        const double supply = std::max(0.0, supply_dist(rng));
        const double shortage = std::max(0.0, demand - (supply + scenario.reserve));
        shortages.push_back(shortage);
        if (shortage > 0.0) ++shortage_events;
    }

    const double expected_shortage = std::accumulate(shortages.begin(), shortages.end(), 0.0) / shortages.size();
    const double shortage_probability = static_cast<double>(shortage_events) / shortages.size();

    std::cout << std::fixed << std::setprecision(6)
              << "cpp shortage_probability=" << shortage_probability
              << " expected_shortage=" << expected_shortage
              << " q95=" << quantile(shortages, 0.95)
              << " max_shortage=" << *std::max_element(shortages.begin(), shortages.end())
              << "\n";
    return 0;
}
