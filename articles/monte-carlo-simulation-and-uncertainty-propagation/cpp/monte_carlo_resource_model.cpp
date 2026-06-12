#include <algorithm>
#include <iomanip>
#include <iostream>
#include <random>
#include <vector>

double uniform(std::mt19937_64& rng, double min_value, double max_value) {
    std::uniform_real_distribution<double> dist(min_value, max_value);
    return dist(rng);
}

double run_once(std::mt19937_64& rng) {
    double stock = uniform(rng, 65.0, 75.0);
    const double growth_rate = uniform(rng, 0.14, 0.22);
    const double extraction = uniform(rng, 5.0, 8.0);
    const double shock_probability = uniform(rng, 0.02, 0.08);
    const double shock_fraction = 0.12;
    const double capacity = 100.0;

    for (int step = 0; step < 50; ++step) {
        const double growth = growth_rate * stock * (1.0 - stock / capacity);
        const double shock = uniform(rng, 0.0, 1.0) < shock_probability ? stock * shock_fraction : 0.0;
        stock = std::max(0.0, stock + growth - extraction - shock);
    }

    return stock;
}

int main() {
    std::mt19937_64 rng(20260612);
    const int replications = 1000;
    double sum = 0.0;
    int depleted = 0;

    for (int i = 0; i < replications; ++i) {
        const double final_stock = run_once(rng);
        sum += final_stock;
        if (final_stock <= 10.0) {
            depleted += 1;
        }
    }

    std::cout << "replications,mean_final_stock,depletion_probability\n";
    std::cout << replications << ","
              << std::fixed << std::setprecision(6)
              << sum / replications << ","
              << static_cast<double>(depleted) / replications << "\n";

    return 0;
}
