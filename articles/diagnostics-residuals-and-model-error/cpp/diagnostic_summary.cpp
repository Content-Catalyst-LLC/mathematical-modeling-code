#include <algorithm>
#include <cmath>
#include <iomanip>
#include <iostream>
#include <string>
#include <vector>

struct Observation {
    int time;
    std::string group;
    double observed;
    double predicted;
    double threshold;
};

int main() {
    std::vector<Observation> data = {
        {1, "baseline", 82.0, 81.5, 70.0},
        {2, "baseline", 79.5, 80.2, 70.0},
        {3, "baseline", 77.0, 78.4, 70.0},
        {4, "baseline", 74.3, 75.6, 70.0},
        {5, "threshold", 71.5, 72.8, 70.0},
        {6, "threshold", 69.2, 71.0, 70.0},
        {7, "threshold", 67.8, 69.8, 70.0},
        {8, "stress", 65.5, 68.0, 70.0},
        {9, "stress", 63.0, 66.4, 70.0},
        {10, "stress", 61.1, 65.2, 70.0}
    };

    double sum_abs = 0.0;
    double sum_sq = 0.0;
    double bias = 0.0;
    double max_abs = 0.0;
    int disagreements = 0;

    for (const auto& item : data) {
        const double residual = item.observed - item.predicted;
        const double abs_error = std::abs(residual);
        sum_abs += abs_error;
        sum_sq += residual * residual;
        bias += residual;
        max_abs = std::max(max_abs, abs_error);

        const bool observed_below = item.observed < item.threshold;
        const bool predicted_below = item.predicted < item.threshold;
        if (observed_below != predicted_below) {
            disagreements++;
        }
    }

    const double n = static_cast<double>(data.size());

    std::cout << "mean_error,mae,rmse,max_abs_error,decision_disagreements\n";
    std::cout << std::fixed << std::setprecision(6)
              << bias / n << ","
              << sum_abs / n << ","
              << std::sqrt(sum_sq / n) << ","
              << max_abs << ","
              << disagreements << "\n";

    return 0;
}
