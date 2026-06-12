#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <limits>
#include <vector>

struct Observation {
    double stock;
    double extraction;
};

double score(double growth_rate, double carrying_capacity, const std::vector<Observation>& data) {
    double stock = data.front().stock;
    double sse = 0.0;

    for (std::size_t i = 0; i < data.size(); ++i) {
        double predicted = stock;
        if (i > 0) {
            const auto& previous = data[i - 1];
            const double growth = growth_rate * stock * (1.0 - stock / carrying_capacity);
            predicted = std::max(0.0, stock + growth - previous.extraction);
            stock = predicted;
        }
        const double residual = data[i].stock - predicted;
        sse += residual * residual;
    }

    return sse;
}

int main() {
    std::vector<Observation> data = {
        {70.0, 5.5}, {72.8, 5.8}, {74.1, 6.2}, {75.0, 6.4}, {75.5, 6.8},
        {75.2, 7.0}, {74.7, 7.1}, {73.8, 7.4}, {72.6, 7.6}, {71.2, 7.8}
    };

    double best_sse = std::numeric_limits<double>::infinity();
    double best_g = 0.0;
    double best_k = 0.0;

    for (double g = 0.08; g <= 0.2600001; g += 0.01) {
        for (double k = 85.0; k <= 125.0001; k += 5.0) {
            const double sse = score(g, k, data);
            if (sse < best_sse) {
                best_sse = sse;
                best_g = g;
                best_k = k;
            }
        }
    }

    std::cout << "best_growth_rate,best_carrying_capacity,sse\n";
    std::cout << std::fixed << std::setprecision(6) << best_g << "," << best_k << "," << best_sse << "\n";
    return 0;
}
