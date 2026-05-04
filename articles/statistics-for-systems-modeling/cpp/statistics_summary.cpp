#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>

int main() {
    std::vector<double> values = {18.4, 36.7, 62.1, 28.9, 64.8, 13.7, 43.5, 29.8, 79.4, 30.2};

    double mean = std::accumulate(values.begin(), values.end(), 0.0) / values.size();

    double ss = 0.0;
    for (double value : values) {
        ss += (value - mean) * (value - mean);
    }

    double variance = ss / (values.size() - 1);
    double sd = std::sqrt(variance);

    std::cout << "Mean: " << mean << "\n";
    std::cout << "Sample variance: " << variance << "\n";
    std::cout << "Sample standard deviation: " << sd << "\n";

    return 0;
}
