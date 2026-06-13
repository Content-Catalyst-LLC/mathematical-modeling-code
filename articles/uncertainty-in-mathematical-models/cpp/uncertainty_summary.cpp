#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <random>
#include <string>
#include <vector>

struct Parameter {
    std::string name;
    double low;
    double high;
};

double projection(double initial_stock, double growth_rate, double carrying_capacity, double extraction_rate, double shock_intensity) {
    double stock = initial_stock;
    for (int year = 0; year < 10; ++year) {
        const double growth = growth_rate * stock * (1.0 - stock / carrying_capacity);
        const double extraction = extraction_rate * stock;
        const double shock = shock_intensity * stock;
        stock = std::max(0.0, stock + growth - extraction - shock);
    }
    return stock;
}

double quantile(std::vector<double> values, double p) {
    std::sort(values.begin(), values.end());
    const auto index = static_cast<std::size_t>(p * static_cast<double>(values.size() - 1));
    return values[index];
}

int main() {
    std::mt19937 rng(42);
    std::vector<Parameter> params = {
        {"initial_stock", 72.0, 88.0},
        {"growth_rate", 0.04, 0.12},
        {"carrying_capacity", 100.0, 140.0},
        {"extraction_rate", 0.08, 0.18},
        {"shock_intensity", 0.00, 0.08}
    };

    std::vector<double> outputs;
    int threshold_count = 0;

    for (int i = 0; i < 1000; ++i) {
        std::vector<double> values;
        for (const auto& p : params) {
            std::uniform_real_distribution<double> dist(p.low, p.high);
            values.push_back(dist(rng));
        }
        const double y = projection(values[0], values[1], values[2], values[3], values[4]);
        outputs.push_back(y);
        if (y < 45.0) {
            threshold_count++;
        }
    }

    double sum = 0.0;
    for (double y : outputs) {
        sum += y;
    }

    std::cout << "mean,p05,p95,threshold_probability\n";
    std::cout << std::fixed << std::setprecision(6)
              << sum / static_cast<double>(outputs.size()) << ","
              << quantile(outputs, 0.05) << ","
              << quantile(outputs, 0.95) << ","
              << static_cast<double>(threshold_count) / static_cast<double>(outputs.size()) << "\n";

    return 0;
}
