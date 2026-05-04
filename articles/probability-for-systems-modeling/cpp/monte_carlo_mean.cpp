#include <iostream>
#include <random>

int main() {
    const int n = 10000;
    std::mt19937 rng(42);
    std::uniform_real_distribution<double> exposure_dist(0.2, 1.0);
    std::uniform_real_distribution<double> vulnerability_dist(0.0, 1.0);

    double total = 0.0;

    for (int i = 0; i < n; ++i) {
        double exposure = exposure_dist(rng);
        double vulnerability = vulnerability_dist(rng);
        double loss = exposure * vulnerability;
        total += loss;
    }

    std::cout << "Monte Carlo mean loss estimate: " << total / n << "\n";

    return 0;
}
